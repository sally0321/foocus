from collections import deque
from datetime import datetime, timedelta
import uuid

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget,  QMessageBox, QDialog, QHBoxLayout
from PySide6.QtCore import QTimer, Qt, QObject, Signal, QUrl
from PySide6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput
from PySide6.QtGui import QImage, QPixmap, QCursor
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision
import joblib 
import sklearn
import cv2
import pandas as pd
from requests.exceptions import ConnectionError

from views.attention_detector_widget import AttentionDetectorWidget
from utils.eye_landmarks_utils import *
from utils.gaze_utils import *
from utils.sessiondb_utils import *
from utils.cloud_sessiondb_utils import *
from models.data import *
from models.login_session import LoginSession
from utils.utils import resource_path

FACE_LANDMARKER_TASK_PATH = resource_path("resources/models/face_landmarker.task") 
SVC_MODEL_PATH = resource_path("resources/models/svc_ear_model.joblib")
NUMBER_OF_EAR= 15 # Number of EAR values to consider for SVC prediction
PREDICTION_INTERVAL_FRAME = 5 # Make a prediction every 5 frames
DEFAULT_PREDICTION_TEXT = "" # Default eye state classification text for display to user
RULE_1_WINDOW_SEC = 5 # Evaluate Rule 1 every 5 seconds
RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS = 5 # Number of consecutive long blinks to trigger Rule 1
RULE_2_WINDOW_SEC = 60 # The window size for Rule 2 evaluation in seconds
RULE_2_EVALUATION_INTERVAL_SEC = 5 # Evaluate Rule 2 every 5 seconds
DEFAULT_FPS = 10.0 # Default FPS for the camera feed after considering processing overhead

# Define the eye states
EYE_OPEN = 0
EYE_BLINK = 1
EYE_CLOSED = 2

class AttentionDetectorWidgetController(QObject):
    latest_ear_value = Signal(float) # Signal to indicate the latest EAR value
    is_notification_start = Signal() # Signal to indicate a notification is starting for the focus zone page controller to pause the timer during the notification pop up
    is_notification_end = Signal() # Signal to indicate a notification has ended for the focus zone page controller to continue the tiemr
    page_selected = Signal(str) # Signal to notify the main window controller about page changes
    is_stop = Signal() # Signal to indicate the attention detector has stopped for the focus zone page controller to stop the timer and reset the focus tracker

    def __init__(self):
        super().__init__()

        self.view = AttentionDetectorWidget()
        
        # Timer setup
        self.timer = QTimer()   
        self.timer.timeout.connect(self.update_frame) # Connect timeout signal to the update_frame method so the frame is updated automatically at each time interval

        # Load MediaPipe Face Landmarker and SVC model
        self.detector = self._initialize_face_landmarker()
        self.svc_model = self._load_svc_model()

        # Session metadata
        self.session_id = str(uuid.uuid4())
        self._is_running = False
        self.start_time = None
        self.end_time = None
        self.pause_intervals = [] # List of tuples (start_time, end_time) for each pause interval
        self.current_pause_start_time= None # Start time of the current pause interval
        self.notification_timestamps = [] # List of times when notifications were triggered
        
        # Webcam and frame processing
        self.cap = None
        self.actual_fps = DEFAULT_FPS
        self.frame_count = 0 # Counts the number of frames processed
        
        # EAR Data and Classification Setup
        self.ear_values = deque(maxlen=NUMBER_OF_EAR) # Store the last N EAR values
        self.all_ear_values = [] # Stores all ear values
        self.all_svc_predictions = [] # Stores all SVC prediction labels (e.g., 0, 1, 2)
        self.last_svc_trigger_index = 0 # Index of the last processed SVC prediction that triggered a rule evaluation to avoid re-evaluating the same sequence
        self.current_prediction = DEFAULT_PREDICTION_TEXT # Current eye state classification text for display
        
        # Default looking direction
        self.current_looking_direction = ("LEFT", "UP") 

        # Initialize sound effect
        self.drowsiness_notification_sound_effect = QSoundEffect(source=QUrl.fromLocalFile(resource_path("resources/audio/noti_sound_effect.wav")))
        # Initialize the audio output and media player for sound effects
        self.audio_output = QAudioOutput()
        self.completion_notification_sound_player = QMediaPlayer()
        self.completion_notification_sound_player.setAudioOutput(self.audio_output)
        self.completion_notification_sound_player.setSource(QUrl.fromLocalFile(resource_path("resources/audio/completion_noti_sound_effect.wav")))
    
    def _initialize_face_landmarker(self):
        """Initializes and returns the MediaPipe Face Landmarker."""

        try:
            base_options = mp_tasks.BaseOptions(model_asset_path=FACE_LANDMARKER_TASK_PATH)
            options = vision.FaceLandmarkerOptions(
                base_options=base_options,
                output_face_blendshapes=True, 
                output_facial_transformation_matrixes=True, 
                num_faces=1 # Detect only one face
            )
            detector = vision.FaceLandmarker.create_from_options(options)
            return detector
        
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to initialize Face Landmarker:\n{e}\nCheck the path: {FACE_LANDMARKER_TASK_PATH}")
            return None 

    def _load_svc_model(self):
        """Loads the trained SVC model."""

        try:
            model = joblib.load(SVC_MODEL_PATH)
            return model
        except FileNotFoundError:
            QMessageBox.warning(self.view, "Warning", f"SVC Model file not found:\n{SVC_MODEL_PATH}\n\nReal-time classification will be disabled.")
            return None
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to load SVC model:\n{e}")
            return None

    def _reset_state(self):
        """Resets frame count, EAR values, prediction text, and drowsiness detection state."""
        
        # Frame processing
        self.frame_count = 0
        self.actual_fps = DEFAULT_FPS 
        
        # Session metadata
        self.session_id = str(uuid.uuid4())
        self.start_time = None
        self.end_time = None
        self.pause_intervals.clear()
        self.current_pause_start_time = None
        self.notification_timestamps.clear()

        # EAR and SVC state
        self.ear_values.clear()
        self.all_ear_values.clear()
        self.all_svc_predictions.clear()
        self.last_svc_trigger_index = 0
        self.current_prediction = DEFAULT_PREDICTION_TEXT

        self.current_looking_direction = ("LEFT", "UP")

    def start_camera(self):
        """Starts the camera and begins capturing frames."""

        # If the camera is not initialized yet, i.e. the user just started the focus session, reset the state 
        if not self.cap:
            self._reset_state()
            self.timer.setInterval(33)
            self.actual_fps = DEFAULT_FPS
        
        # Use the default camera
        self.cap = cv2.VideoCapture(0)

        # Show error message if camera cannot be opened
        if not self.cap.isOpened():
            QMessageBox.critical(self.view, "Error", "Could not open default camera.")
            self.cap = None
            return
        
        # If resuming from a pause within the same session, record the pause interval and reset the current_pause_start_time
        if self.current_pause_start_time:
            pause_end_time = datetime.now()
            self.pause_intervals.append((self.current_pause_start_time, pause_end_time))
            self.current_pause_start_time = None
        # If starting a new session, set the start time
        else:
            self.start_time = datetime.now()
        
        self._is_running = True        
        self.timer.start()

    def stop_camera(self):
        """Stops the camera and save session data."""

        if self.start_time:
            self.end_time = datetime.now()

            self.timer.stop()

            self._is_running = False
            
            # Handle the situation where the user paused the camera before stopping
            if self.current_pause_start_time:
                self.pause_intervals.append((self.current_pause_start_time, self.end_time))
                self.current_pause_start_time = None

            # Close the camera if it is open
            if self.cap:
                self.cap.release()
                self.cap = None
            
            # Clear the camera feed label and reset the eye status label
            self.view.camera_feed_label.clear() 
            self.view.camera_feed_label.setText("Click start to activate the attention detector 📷")
            self.view.eye_status_label.setText(DEFAULT_PREDICTION_TEXT)

            self.is_stop.emit()

            # Calculate and save session metrics and logs 
            session_metrics = self.create_session_metrics()
            session_log = self.create_session_log()

            # Save session log and metrics to local database
            insert_session_to_local_db(session_log, session_metrics)

            # Save session metrics to cloud database
            try:
                insert_session_to_cloud_db_response = insert_session_to_cloud_db(session_metrics)
                if insert_session_to_cloud_db_response['status'] != "success":
                    raise Exception
            except ConnectionError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Connection Error")
                msg.setText("You appear to be offline. The session data was not uploaded to the cloud.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Unexpected Error")
                msg.setText("Uh oh, an unexpected error occurs. The session data was not uploaded to the cloud.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

            self._reset_state()

    def pause_camera(self):
        """Pauses the camera and saves the current pause start time."""

        self.timer.stop()
        self.current_pause_start_time = datetime.now()
        self.cap.release()
        self._is_running = False

    def toggle_camera(self):
        """Toggles the camera state between running and paused."""
        
        if self._is_running:
            self.pause_camera()
        else:
            self.start_camera()

    def check_rule_1(self):
        """
        Checks for Rule 1 (5 consecutive long blinks) every time a new SVC prediction is made.
        If triggered and notification shown, set last_trigger_svc_idx to prevent trigerring Rule 2 with the same sequence.
        """

        if len(self.all_svc_predictions) < RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS:
            return

        # Define the end index of the sequence as the latest prediction
        sequence_end_idx = len(self.all_svc_predictions) - 1
        # Define the start index of the sequence 
        sequence_start_idx = sequence_end_idx - RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS + 1

        # Evaluate rule 1 only if this potential sequence starts at or after processed svc predictions
        if sequence_start_idx < self.last_svc_trigger_index:
            return 

        # Check if the last RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS are all '2'
        is_rule_1_triggered = True
        for i in range(RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS):
            if self.all_svc_predictions[sequence_start_idx + i] != 2: # Assuming 2 is 'long blink'
                is_rule_1_triggered = False
                break

        # If Rule 1 is triggered, show the notification and update the last trigger index
        if is_rule_1_triggered:
            rule_1_trigger_message = f"GOTCHA! Looks like you're losing focus.\nDon’t drift off yet! Stay in view and keep your eyes open." 
            self.show_drowsiness_notification(rule_1_trigger_message)
            self.last_svc_trigger_index = sequence_end_idx + 1

    def check_rule_2(self):
        """Check for rule 2 (proportion of long blinks (2) to total number of blinks (1, 2)) every RULE_2_EVALUATION_INTERVAL_SEC."""
        
        if not self.all_svc_predictions:
            return
        
        predictions_per_sec = self.actual_fps / PREDICTION_INTERVAL_FRAME
        
        rule_2_window_size = int(predictions_per_sec * RULE_2_WINDOW_SEC)
       
        # Get predictions from the last 60 seconds (or fewer if not enough history)
        sequence_start_idx = max(0, len(self.all_svc_predictions) - rule_2_window_size)
        if sequence_start_idx < self.last_svc_trigger_index:
            return  # Skip if the sequence starts before the last processed index
        
        # Get the current window of predictions for Rule 2 evaluation
        current_window = self.all_svc_predictions[sequence_start_idx:]
        if len(current_window) < rule_2_window_size:
            return

        # Count the number of long blinks (2) and short blinks (1) in the current window            
        number_of_long_blinks = current_window.count(2)  
        number_of_short_blinks = current_window.count(1)
        total_blinks = number_of_long_blinks + number_of_short_blinks

        # Trigger Rule 2 if the proportion of long blinks is greater than 25%
        if total_blinks > 0:
            proportion_long_blinks = number_of_long_blinks / total_blinks
            if proportion_long_blinks > 0.25:
                self.last_svc_trigger_index = len(self.all_svc_predictions) 
                self.show_drowsiness_notification(
                    f"👀 You're blinking slow... {proportion_long_blinks*100:.1f}% of your recent blinks were long. "
                    f"\nFeeling sleepy? Maybe stretch or grab a drink!"
                )
    
    def update_frame(self):
        """Capture a frame from the webcam, process it, and update the display."""

        # Check if the camera is initialized and opened
        if self.cap is None or not self.cap.isOpened():
            return
        
        # Read a frame from the camera
        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.critical(self.view, "Error", "Error processing live camera feed.")
            self.stop_camera()
            return
        
        self.frame_count += 1

        # Convert the frame to RGB format for MediaPipe processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # MediaPipe Detection 
        try:
            detection_result = self.detector.detect(mp_image)
            # Extract face landmarks from the detection result
            face_landmarks_list = detection_result.face_landmarks
        except Exception as e:
            print(f"Error during face detection: {e}")
            detection_result = None 

        image_height, image_width = frame.shape[:2]

        # Initialize the annotated image as a copy of the original frame
        annotated_image = np.copy(frame_rgb)

        average_ear = 0.0
        if detection_result and face_landmarks_list:
            annotated_image = draw_face_landmarks_on_image(frame_rgb, face_landmarks_list)

            # Get the first face landmarks (only one face will be detected)
            face_landmarks = detection_result.face_landmarks[0]

            # Calculate the gaze direction
            l_corner, r_corner, l_gaze_points, r_gaze_points, l_gaze_point, r_gaze_point, avg_gaze_point, self.current_looking_direction = calculate_gaze(image_width, image_height, face_landmarks)
            cv2.line(annotated_image, l_corner, tuple(np.ravel(l_gaze_points[2]).astype(np.int32)), (4, 191,191), 3)
            cv2.line(annotated_image, r_corner, tuple(np.ravel(r_gaze_points[2]).astype(np.int32)), (4, 191,191), 3)

            # Calculate EAR for both eyes if the coordinates are valid
            left_eye_coords = get_pixel_coords_from_landmarks(face_landmarks, LEFT_EYE_INDICES, image_width, image_height)
            right_eye_coords = get_pixel_coords_from_landmarks(face_landmarks, RIGHT_EYE_INDICES, image_width, image_height)
            if len(left_eye_coords) == 6 and len(right_eye_coords) == 6:
                left_ear = calculate_ear(left_eye_coords)
                right_ear = calculate_ear(right_eye_coords)
                average_ear = (left_ear + right_ear) / 2.0

        # Store and update EAR value
        rounded_average_ear = round(average_ear, 5)
        self.ear_values.append(rounded_average_ear)
        self.all_ear_values.append(rounded_average_ear)
        self.latest_ear_value.emit(rounded_average_ear)

        # Make SVC prediction
        if (self.svc_model is not None 
            and len(self.ear_values) == NUMBER_OF_EAR 
            and self.frame_count % PREDICTION_INTERVAL_FRAME == 0):
            
            # Create a DataFrame for the SVC model
            columns = [f"EAR {i + 1}" for i in range(NUMBER_OF_EAR)] # Create column names, e.g. "EAR 1" - "EAR 15"
            # Convert deque to numpy array and reshape it into a 2D array for SVC prediction
            ear_sample_array = np.array(list(self.ear_values)).reshape(1, -1) # Shape (1, 15), e.g. [[0.25, 0.30, ..., 0.28]]
            ear_sample_df = pd.DataFrame(ear_sample_array, columns=columns)

            ear_classification_result = EYE_OPEN # Default classification result

            try:
                # Predict using the loaded SVC model
                prediction = self.svc_model.predict(ear_sample_df)
                # prediction_proba = self.svc_model.predict_proba(ear_sample_df) 

                # Get and store the classification result
                ear_classification_result = prediction[0]
                self.all_svc_predictions.append(ear_classification_result)

                # confidence = np.max(prediction_proba) * 100

                # Set the current prediction text based on the classification result
                match(ear_classification_result):
                    case 0:
                        self.current_prediction = f"Focused 👁️👁️"
                    case 1:
                        self.current_prediction = f"Blinking 😌"
                    case 2:
                        self.current_prediction = f"Closed eye 💤"
                    case _:
                        self.current_prediction = DEFAULT_PREDICTION_TEXT
            
            except Exception as e:
                print(f"Error during SVC prediction: {e}")
                self.current_prediction = "Prediction Error"

            # Evaluate rules to determine drowsiness
            # Rule 1 is checked for every new svc prediction made
            self.check_rule_1()

            # Calculate the number of SVC predictions that should trigger rule 2 evaluation
            predictions_per_second = self.actual_fps / PREDICTION_INTERVAL_FRAME # Number of svc predictions made per second
            rule_2_eval_trigger_count = int(predictions_per_second * RULE_2_EVALUATION_INTERVAL_SEC) # Number of SVC predictions that should trigger rule 2 evaluation
            
            if (rule_2_eval_trigger_count > 0 
                and len(self.all_svc_predictions) > 0 
                and (len(self.all_svc_predictions) - self.last_svc_trigger_index) % rule_2_eval_trigger_count == 0):
                self.check_rule_2()

        # Flip the image horizontally for a mirror effect
        annotated_image = cv2.flip(annotated_image, 1)  
        
        # Display prediction
        self.view.eye_status_label.setText(self.current_prediction)

        # Display the annotated image with eye landmarks and gaze direction
        frame_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        # Convert BGR frame to QImage for PySide6 display
        qt_image = QImage(
            frame_bgr.data, frame_bgr.shape[1], frame_bgr.shape[0],
            frame_bgr.strides[0], QImage.Format_BGR888
        )
        # Scale the QImage to fit the QLabel while keeping aspect ratio
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.view.camera_feed_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.view.camera_feed_label.setPixmap(scaled_pixmap)

    def show_drowsiness_notification(self, message):
        """Displays a drowsiness notification pop-up."""

        def handle_reenergize():
            """Handle the re-energize button click."""
            # Record the notification pop up duration as a pause interval
            self.pause_intervals.append((self.notification_timestamps[-1], datetime.now()))
            # Pause the session
            self.toggle_camera()
            self.drowsiness_notification_sound_effect.stop()
            self.page_selected.emit("mind_energizer")
            dialog_box.close()
        
        def handle_continue():
            """Handle the continue button click."""
            self.is_notification_end.emit()
            # Record the notification pop up duration as a pause interval
            self.pause_intervals.append((self.notification_timestamps[-1], datetime.now()))
            self.drowsiness_notification_sound_effect.stop()
            dialog_box.close()

        def handle_stop():
            """Handle the stop button click."""
            # Record the notification pop up duration as a pause interval
            self.pause_intervals.append((self.notification_timestamps[-1], datetime.now()))
            self.drowsiness_notification_sound_effect.stop()
            dialog_box.close()
            # Stop the camera only after a short delay to ensure the dialog box closes properly and prevent unexpected behavior
            QTimer.singleShot(0, self.stop_camera)

        self.is_notification_start.emit()

        # Record the notification trigger time
        self.notification_timestamps.append(datetime.now())

        # Create the dialog box
        dialog_box = QDialog(self.view)
        dialog_box.setWindowTitle("Feeling sleepy?")
        dialog_box.setFixedSize(400, 200)
        dialog_box.setObjectName("notification")

        # Create the noti message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setObjectName("noti_message_label")

        # Create the noti buttons and connect to handlers
        reenergize_btn = QPushButton("Re-energize")
        reenergize_btn.setCursor(QCursor(Qt.PointingHandCursor))
        reenergize_btn.setObjectName("noti_reenergize_btn")
        reenergize_btn.clicked.connect(handle_reenergize)
        continue_btn = QPushButton("Continue")
        continue_btn.setCursor(QCursor(Qt.PointingHandCursor))
        continue_btn.setObjectName("noti_continue_btn")
        continue_btn.clicked.connect(handle_continue)
        stop_btn = QPushButton("Stop")
        stop_btn.setCursor(QCursor(Qt.PointingHandCursor))
        stop_btn.setObjectName("noti_stop_btn")
        stop_btn.clicked.connect(handle_stop)

        btns_holder = QWidget()
        btns_holder_layout = QHBoxLayout(btns_holder)
        btns_holder_layout.addWidget(reenergize_btn)
        btns_holder_layout.addWidget(continue_btn)
        btns_holder_layout.addWidget(stop_btn)

        dialog_box_layout = QVBoxLayout(dialog_box)
        dialog_box_layout.addStretch(1)
        dialog_box_layout.addWidget(message_label)
        dialog_box_layout.addStretch(1)
        dialog_box_layout.addWidget(btns_holder)

        # Play the drowsiness notification sound until the user click a noti button
        self.drowsiness_notification_sound_effect.setVolume(1)
        self.drowsiness_notification_sound_effect.play()

        dialog_box.exec()

    def show_completion_notification(self, duration_ms=5000):
        """Show a notification when the focus session is completed."""

        # Determine the position of the notification based on the user's looking direction
        # The position of the notification is always opposite to the user's looking direction
        looking_direction = self.current_looking_direction
        match (looking_direction):
            case ("LEFT", "UP"):
                # Notification is displayed at the bottom right corner
                x = self.view.width() - 80
                y = self.view.height() - 80
            case ("LEFT", "DOWN"):
                # Notification is displayed at the upper right corner
                x = self.view.width() - 80
                y = 40
            case ("RIGHT", "UP"):
                # Notification is displayed at the bottom left corner
                x = 20
                y = self.view.height() - 80
            case ("RIGHT", "DOWN"):
                # Notification is displayed at the upper left corner
                x = 20
                y = 40

        # Create a notification widget        
        self.notif = QWidget() 
        self.notif.adjustSize()
        self.notif.move(x, y)
        layout = QVBoxLayout(self.notif)

        # Ensure the notification is always shown on top of other windows
        self.notif.setWindowFlags(
            Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        # Set the background color of the widget to transparent
        self.notif.setAttribute(Qt.WA_TranslucentBackground)
        self.notif.setAttribute(Qt.WA_ShowWithoutActivating)

        # Session completion message
        label = QLabel("Focus session completed! 🎉")
        label.setObjectName("completion_notification_label")
        layout.addWidget(label)
        
        self.notif.show()

        # Set the audio setting and play the audio
        self.audio_output.setVolume(0.1)
        self.completion_notification_sound_player.setPosition(0)  # Play the audio from beginning
        self.completion_notification_sound_player.play()

        # Automatically close the notification after a delay
        QTimer.singleShot(duration_ms, lambda: (self.notif.close(), setattr(self, 'notif', None)))
    
    def create_session_log(self):
        """Create and return a SessionLog data class object"""

        return SessionLog(
            session_id=self.session_id,
            svc_predictions=self.all_svc_predictions,
            ear_values=self.all_ear_values
        )
    
    def create_session_metrics(self):
        """Calculate and return a SessionMetrics data class object"""

        # Calculate attention span
        # The earliest distracted time is the start of the first pause interval, or the end time if no pauses were recorded
        earliest_distracted_time = self.pause_intervals[0][0] if self.pause_intervals else self.end_time
        attention_span = (earliest_distracted_time - self.start_time).total_seconds()

        # Calculate frequency of unfocus, i.e. number of attention losses
        # Frequency of unfocus is the number of pauses the user has taken and the number of times the notification was triggered
        frequency_unfocus = len(self.pause_intervals)

        # Calculate active and pause durations
        active_duration = self.end_time - self.start_time
        pause_duration = timedelta(0)
        for pause_start_time, pause_end_time in self.pause_intervals:
            pause_interval_duration = pause_end_time - pause_start_time
            active_duration -= pause_interval_duration
            pause_duration += pause_interval_duration
        active_duration = active_duration.total_seconds()
        pause_duration = pause_duration.total_seconds()
        
        # Calculate total unfocus duration, i.e. when the user close their eyes or look away and pause the session
        total_unfocus_duration_in_sec = self.all_svc_predictions.count(EYE_CLOSED) * PREDICTION_INTERVAL_FRAME * (1 / self.actual_fps) + pause_duration
        
        # Calculate the total focus duration, i.e. when the user has their eyes open 
        total_focus_duration_in_sec = self.all_svc_predictions.count(EYE_OPEN) * PREDICTION_INTERVAL_FRAME * (1 / self.actual_fps)
        
        # Create the LoginSession singleton instance to get user information
        login_session = LoginSession()
        user_id = login_session.get_user_id()
        username = login_session.get_username()

        return SessionMetrics(
            session_id=self.session_id,
            user_id=user_id,
            username=username,
            start_time=str(self.start_time),
            end_time=str(self.end_time),
            active_duration=active_duration,
            pause_duration=pause_duration,
            attention_span=attention_span,
            frequency_unfocus=frequency_unfocus,
            focus_duration=total_focus_duration_in_sec,
            unfocus_duration=total_unfocus_duration_in_sec
        )



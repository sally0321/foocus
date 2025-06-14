import os
from collections import deque
from datetime import datetime, timedelta

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget,  QMessageBox, QDialog, QHBoxLayout
from PySide6.QtCore import QTimer, Qt, QObject, Signal, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QImage, QPixmap, QCursor
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision
import joblib 
import cv2
import pandas as pd
from requests.exceptions import ConnectionError

from views.attention_detector_widget import AttentionDetectorWidget
from utils.eye_landmarks_utils import *
from utils.sessiondb_utils import *
from utils.cloud_sessiondb_utils import *
from models.data import *
from models.login_session import LoginSession

FACE_LANDMARKER_TASK_PATH = "resources/models/face_landmarker.task" 
SVC_MODEL_PATH = "resources/models/svc_ear_model.joblib"
EAR_CALCULATION_RESULT_DIR = "./ear_calculation_results"
EAR_CLASSIFICATION_RESULT_DIR = "./ear_classification_results"
NUMBER_OF_EAR= 15 
PREDICTION_INTERVAL_FRAME = 5 
DEFAULT_PREDICTION_TEXT = "Status: N/A"
RULE_1_WINDOW_SEC = 5
RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS = 5
RULE_2_WINDOW_SEC = 60
RULE_2_EVALUATION_INTERVAL_SEC = 5
DEFAULT_FPS = 30.0 

class AttentionDetectorWidgetController(QObject):
    latest_ear_value = Signal(float)
    is_notification = Signal()
    page_selected = Signal(str)
    is_stop = Signal()

    def __init__(self):
        super().__init__()

        self.view = AttentionDetectorWidget()
        
        self.timer = QTimer()

        # self.view.start_pause_btn.clicked.connect(self.toggle_camera)
        # self.view.stop_btn.clicked.connect(self.stop_camera)
        self.timer.timeout.connect(self.update_frame)

        self.start_time = None
        self.end_time = None
        self.pause_intervals = []
        self.current_pause_start_time= None
        self.notification_times = []
        self.session_id = str(uuid.uuid4())

        # Video Capture
        self.cap = None
        self.actual_fps = DEFAULT_FPS
        self.detector = self._initialize_face_landmarker()
        self._is_running = False

        # EAR Data and Classification Setup
        self.ear_values = deque(maxlen=NUMBER_OF_EAR) # Store the last N EAR values
        self.all_ear_values = [] # Stores all ear values
        self.frame_count = 0
        self.svc_model = self._load_svc_model()
        self.all_svc_predictions = [] # Stores all SVC prediction labels (e.g., 0, 1, 2)
        self.svc_prediction_count = 0 # Counts how many SVC predictions made in current session
        self.processed_until_svc_pred_index = 0
        self.current_prediction = DEFAULT_PREDICTION_TEXT # Display status
        self.ear_calculation_result_file = None # File to write EAR values
        self.ear_classification_result_file = None 

        self.last_notification_time = datetime.min # Initialize to allow the first notification

        # Ensure output directory exists
        os.makedirs(EAR_CALCULATION_RESULT_DIR, exist_ok=True)
        os.makedirs(EAR_CLASSIFICATION_RESULT_DIR, exist_ok=True)

        self.timer.timeout.connect(self.update_frame)

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
            QMessageBox.critical(self, "Error", f"Failed to initialize Face Landmarker:\n{e}\nCheck the path: {FACE_LANDMARKER_TASK_PATH}")
            return None 

    def _load_svc_model(self):
        """Loads the trained SVC model."""
        try:
            model = joblib.load(SVC_MODEL_PATH)
            return model
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", f"SVC Model file not found:\n{SVC_MODEL_PATH}\n\nReal-time classification will be disabled.")
            return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load SVC model:\n{e}")
            return None

    def _reset_state(self):
        """Resets frame count, EAR values, prediction text, and drowsiness detection state."""
        self.frame_count = 0
        self.ear_values.clear()
        self.current_prediction = DEFAULT_PREDICTION_TEXT
        self.all_svc_predictions.clear()
        self.svc_prediction_count = 0
        self.processed_until_svc_pred_index = 0
        self.actual_fps = DEFAULT_FPS 

        self.start_time = None
        self.end_time = None
        self.pause_intervals = []
        self.current_pause_start_time = None
        self.notification_times = []

        self.session_id = str(uuid.uuid4())

    def _open_ear_calculation_result_file(self, base_filename):
        """Opens a new output file for EAR values, closing the previous one if open."""
        # Close previous EAR output file.
        if self.ear_calculation_result_file and not self.ear_calculation_result_file.closed:
            self.ear_calculation_result_file.close()

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(EAR_CALCULATION_RESULT_DIR, f"{base_filename}_{timestamp}.txt")
        
        try:
            self.ear_calculation_result_file = open(output_path, "w")
        except Exception as e:
            self.ear_calculation_result_file = None 
            QMessageBox.warning(self, "Warning", f"Could not open EAR output file:\n{output_path}\n\n{e}")

    def _open_ear_classification_result_file(self, base_filename):
        """Opens a new output file for classification results, closing the previous one if open."""
        # Close previous classification result file.
        if self.ear_classification_result_file and not self.ear_classification_result_file.closed:
            self.ear_classification_result_file.close()

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(EAR_CLASSIFICATION_RESULT_DIR, f"{base_filename}_{timestamp}.txt")
        
        try:
            self.ear_classification_result_file = open(output_path, "w")
        except Exception as e:
            self.ear_classification_result_file = None # Ensure it's None on failure
            QMessageBox.warning(self, "Warning", f"Could not open classification result file:\n{output_path}\n\n{e}")

    def start_camera(self):
        if not self.cap:
            self._reset_state()
            self._open_ear_calculation_result_file("camera_capture")
            self._open_ear_classification_result_file("camera_capture")
            self.timer.setInterval(33)
            self.actual_fps = DEFAULT_FPS
            self.start_time = datetime.now()
        
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open default camera.")
            self.cap = None
            return
        
        if self.current_pause_start_time:
            pause_end_time = datetime.now()
            self.pause_intervals.append((self.current_pause_start_time, pause_end_time))
            self.current_pause_start_time = None
        
        self._is_running = True        
        self.timer.start()

    def stop_camera(self):
        if self.start_time:
            self.timer.stop()

            self._is_running = False
            
            self.end_time = datetime.now()
            if self.current_pause_start_time:
                self.pause_intervals.append((self.current_pause_start_time, self.end_time))

            if self.cap:
                self.cap.release()
                self.cap = None
            
            if self.ear_calculation_result_file and not self.ear_calculation_result_file.closed:
                self.ear_calculation_result_file.close()
                self.ear_calculation_result_file = None
            if self.ear_classification_result_file and not self.ear_classification_result_file.closed:
                self.ear_classification_result_file.close()
                self.ear_classification_result_file = None
            
            self.view.camera_feed_label.clear() # Clear the video display
            self.view.camera_feed_label.setText("Click start to activate the attention detector 📷")
            # self.view.start_pause_btn.setText("Start")

            self.is_stop.emit()

            session_metrics = self.create_session_metrics()
            session_log = self.create_session_log()
            insert_session_to_local_db(session_log, session_metrics)

            try:
                insert_session_to_cloud_db_response = insert_session_to_cloud_db(session_metrics)
                if insert_session_to_cloud_db_response['status'] != "success":
                    raise Exception
            except ConnectionError as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Connection Error")
                msg.setText("You appear to be offline. The session data was not uploaded to the cloud.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Unexpected Error")
                msg.setText("Uh oh, an unexpected error occurs. The session data was not uploaded to the cloud.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

            self._reset_state()

    def pause_camera(self):
        self.timer.stop()
        self.cap.release()
        self.current_pause_start_time = datetime.now()
        self._is_running = False

    def toggle_camera(self):
        if self._is_running:
            self.pause_camera()
            # self.view.start_pause_btn.setText("Start")
        else:
            self.start_camera()
            # self.view.start_pause_btn.setText("Pause")

    def check_rule_1(self):
        """
        Checks for Rule 1 (5 consecutive long blinks) every time a new SVC prediction is made.
        If triggered and notification shown, advances self.processed_until_svc_pred_index to prevent trigerring Rule 2 with the same sequence.
        """
        if len(self.all_svc_predictions) < RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS:
            return

        # Define the end index of the sequence as the latest prediction
        sequence_end_idx = len(self.all_svc_predictions) - 1
        # Define the start index of the sequence 
        sequence_start_idx = sequence_end_idx - RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS + 1

        # Evaluate rule 1 only if this potential sequence starts at or after processed svc predictions
        if sequence_start_idx < self.processed_until_svc_pred_index:
            return 

        # Check if the last RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS are all '2'
        is_rule_1_triggered = True
        for i in range(RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS):
            if self.all_svc_predictions[sequence_start_idx + i] != 2: # Assuming 2 is 'long blink'
                is_rule_1_triggered = False
                break

        # TODO: change rule trigger message and remove print statement
        if is_rule_1_triggered:
            rule_1_trigger_message = (f"Rule 1: Drowsiness inferred. {RULE_1_NUMBER_OF_CONSECUTIVE_LONG_BLINKS} "
                             f"consecutive 'long blink' outputs detected, ending at prediction "
                             f"#{sequence_end_idx + 1}.")
            print(f"Rule 1 Condition Met: Sequence from {sequence_start_idx + 1} to {sequence_end_idx + 1}.")

            self.show_drowsiness_notification(rule_1_trigger_message)
            self.notification_times.append(datetime.now())
            self.processed_until_svc_pred_index = sequence_end_idx + 1

    def check_rule_2(self):
        """Check for rule 2 (proportion of long blinks (2) to total number of blinks) every RULE_2_EVALUATION_INTERVAL_SEC."""
        if not self.all_svc_predictions:
            return

            
        number_of_predictions_per_second = self.actual_fps / PREDICTION_INTERVAL_FRAME
        
        rule_2_window_size = int(number_of_predictions_per_second * RULE_2_WINDOW_SEC)
       
        # Get predictions from the last 60 seconds (or fewer if not enough history)
        sequence_start_idx = max(0, len(self.all_svc_predictions) - rule_2_window_size)
        current_window = self.all_svc_predictions[sequence_start_idx:]

        if len(current_window) < rule_2_window_size:
            # print(f"Rule 2: Not enough predictions in current window. Current window size: {len(current_window)}")
            return
        
        number_of_long_blinks = current_window.count(2)  
        number_of_short_blinks = current_window.count(1)
        total_blinks = number_of_long_blinks + number_of_short_blinks

        # print(f"Rule 2 Eval: Window size={len(current_window)} preds. Long={number_of_long_blinks}, Short={number_of_short_blinks}, Total Blinks={total_blinks}")

        if total_blinks > 0:
            proportion_long_blinks = number_of_long_blinks / total_blinks
            # print(f"Rule 2 Eval: Proportion of long blinks = {proportion_long_blinks:.2f}")
            if proportion_long_blinks > 0.25:
                self.show_drowsiness_notification(
                    f"Rule 1: Drowsiness inferred. Proportion of long blinks "
                    f"({proportion_long_blinks*100:.1f}%) exceeded 25% in the last {RULE_2_WINDOW_SEC}s."
                )
                self.notification_times.append(datetime.now())
    
    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return
        
        ret, frame = self.cap.read()
        if not ret:
            print("Cannot read frame.")
            self.stop_camera()
            return
        
        self.frame_count += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # MediaPipe Detection 
        try:
            detection_result = self.detector.detect(mp_image)
            face_landmarks_list = detection_result.face_landmarks
        except Exception as e:
             print(f"Error during face detection: {e}")
             detection_result = None 

        image_height, image_width = frame.shape[:2]
        annotated_image = frame_rgb 

        if detection_result and face_landmarks_list:
            annotated_image = draw_face_landmarks_on_image(frame_rgb, face_landmarks_list)

            face_landmarks = detection_result.face_landmarks[0]

            left_eye_coords = get_pixel_coords_from_landmarks(face_landmarks, LEFT_EYE_INDICES, image_width, image_height)
            right_eye_coords = get_pixel_coords_from_landmarks(face_landmarks, RIGHT_EYE_INDICES, image_width, image_height)

            # Calculate EAR
            average_ear = 0.0
            if len(left_eye_coords) == 6 and len(right_eye_coords) == 6:
                left_ear = calculate_ear(left_eye_coords)
                right_ear = calculate_ear(right_eye_coords)
                average_ear = (left_ear + right_ear) / 2.0

            # Store EAR value
            rounded_average_ear = round(average_ear, 5)
            self.ear_values.append(rounded_average_ear)
            self.all_ear_values.append(rounded_average_ear)
            self.latest_ear_value.emit(rounded_average_ear)

            # Write EAR to file if open
            if self.ear_calculation_result_file and not self.ear_calculation_result_file.closed:
                self.ear_calculation_result_file.write(f"{average_ear:.4f}\n")
                
            # SVC prediction
            if (self.svc_model is not None and len(self.ear_values) == NUMBER_OF_EAR and self.frame_count % PREDICTION_INTERVAL_FRAME == 0):
                # Prepare features: Convert deque to numpy array and reshape
                ear_sample_array = np.array(list(self.ear_values)).reshape(1, -1) # Shape (1, 15)
                
                columns = [f"EAR {i + 1}" for i in range(NUMBER_OF_EAR)]
                ear_sample_df = pd.DataFrame(ear_sample_array, columns=columns)

                ear_classification_result = 0 # Default to a non-blink class

                try:
                    # Predict using the loaded SVC model
                    prediction = self.svc_model.predict(ear_sample_df)
                    prediction_proba = self.svc_model.predict_proba(ear_sample_df) # Get probabilities

                    # Update the display text (customize based on your class labels)
                    ear_classification_result = prediction[0]
                    confidence = np.max(prediction_proba) * 100
                    self.current_prediction = f"Status: {ear_classification_result} ({confidence:.1f}%)"

                    if self.ear_classification_result_file and not self.ear_classification_result_file.closed:
                        self.ear_classification_result_file.write(f"{ear_classification_result}\n")
                    
                    # Store prediction for
                    self.all_svc_predictions.append(ear_classification_result)
                    self.svc_prediction_count += 1

                except Exception as e:
                    print(f"Error during SVC prediction: {e}")
                    self.current_prediction = "Status: Prediction Error"

                # Evaluate rules to determine drowsiness
                # Rule 1 is checked for every new svc prediction made
                self.check_rule_1()

                # Calculate the number of SVC predictions that should trigger rule 2 evaluation
                number_of_predictions_per_second = self.actual_fps / PREDICTION_INTERVAL_FRAME
                trigger_count_for_rule_2_eval = int(number_of_predictions_per_second * RULE_2_EVALUATION_INTERVAL_SEC)
                
                if trigger_count_for_rule_2_eval > 0 \
                    and self.svc_prediction_count > 0 and \
                    (self.svc_prediction_count - self.processed_until_svc_pred_index) % trigger_count_for_rule_2_eval == 0:
                    self.check_rule_2()

        # Display Frame and Prediction 
        frame_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

        # Add the prediction text overlay onto the BGR frame
        cv2.putText(frame_bgr, self.current_prediction,
                    (10, 30), # Position (top-left corner)
                    cv2.FONT_HERSHEY_SIMPLEX, 1, # Font type and scale
                    (0, 255, 0) if "Error" not in self.current_prediction else (0, 0, 255), # Color (Green=OK, Red=Error)
                    2, cv2.LINE_AA) # Thickness and line type

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
            self.toggle_camera()
            sound.stop()
            self.page_selected.emit("mind_energizer")
            dialog_box.close()
        
        def handle_continue():
            sound.stop()
            dialog_box.close()

        def handle_stop():
            sound.stop()
            dialog_box.close()
            QTimer.singleShot(0, self.stop_camera)

        self.is_notification.emit()
        # TODO: change message

        dialog_box = QDialog(self.view)
        dialog_box.setWindowTitle("Feeling sleepy?")
        dialog_box.setFixedSize(400, 200)
        dialog_box.setObjectName("notification")

        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setObjectName("noti_message_label")

        reenergize_btn = QPushButton("Re-energize")
        continue_btn = QPushButton("Continue")
        stop_btn = QPushButton("Stop")
        reenergize_btn.setCursor(QCursor(Qt.PointingHandCursor))
        continue_btn.setCursor(QCursor(Qt.PointingHandCursor))
        stop_btn.setCursor(QCursor(Qt.PointingHandCursor))
        reenergize_btn.clicked.connect(handle_reenergize)
        continue_btn.clicked.connect(handle_continue)
        stop_btn.clicked.connect(handle_stop)
        reenergize_btn.setObjectName("noti_reenergize_btn")
        continue_btn.setObjectName("noti_continue_btn")
        stop_btn.setObjectName("noti_stop_btn")

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

        sound = QSoundEffect(source=QUrl.fromLocalFile("resources/audio/noti_sound_effect.wav"))
        sound.setVolume(1)
        sound.play()

        dialog_box.exec()
    
    def create_session_log(self):
        return SessionLog(
            session_id=self.session_id,
            svc_predictions=self.all_svc_predictions,
            ear_values=self.all_ear_values
        )
    
    def create_session_metrics(self):
        first_notification_time = self.notification_times[0] if self.notification_times else datetime.max
        first_pause_start_time = self.pause_intervals[0][0] if self.pause_intervals else datetime.max
        # Choose the earliest of the two distraction times
        earliest_distracted_time = min(first_notification_time, first_pause_start_time)
        # If both were empty, fall back to end_time
        if earliest_distracted_time == datetime.max:
            earliest_distracted_time = self.end_time
        attention_span = (earliest_distracted_time - self.start_time).total_seconds()

        number_of_attention_loss = len(self.notification_times) + len(self.pause_intervals)

        active_duration = self.end_time - self.start_time
        pause_duration = timedelta(0)
        for pause_start_time, pause_end_time in self.pause_intervals:
            pause_interval_duration = pause_end_time - pause_start_time
            active_duration -= pause_interval_duration
            pause_duration += pause_interval_duration
        active_duration = active_duration.total_seconds()
        pause_duration = pause_duration.total_seconds()
        
        total_unfocus_duration_in_sec = self.all_svc_predictions.count(2) * PREDICTION_INTERVAL_FRAME * (1 / self.actual_fps) + pause_duration
        
        total_focus_duration_in_sec = self.all_svc_predictions.count(0) * PREDICTION_INTERVAL_FRAME * (1 / self.actual_fps)
        
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
            frequency_unfocus=number_of_attention_loss,
            focus_duration=total_focus_duration_in_sec,
            unfocus_duration=total_unfocus_duration_in_sec
        )



        


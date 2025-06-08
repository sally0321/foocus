import numpy as np
from mediapipe.python import solutions
from mediapipe.framework.formats import landmark_pb2

LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

def get_pixel_coords_from_landmarks(landmarks, indices, image_width, image_height):
    """ Gets pixel coordinates for specific landmark indices"""
    return [(int(landmarks[i].x * image_width), int(landmarks[i].y * image_height))
            for i in indices if 0 <= i < len(landmarks)] 

def calculate_euclidean_distance(p1, p2):
    """Calculate euclidean distance between point 1 and point 2"""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_ear(eye_landmarks_coords):
    """Calculate Eye Aspect Ratio (EAR) for one eye based on 6 eye coordinates"""
    if len(eye_landmarks_coords) != 6:
        return 0.0 # Return a default value
    
    # Extract points P1-P6 to be used in the EAR formula
    p1, p2, p3, p4, p5, p6 = eye_landmarks_coords

    # Calculate vertical distances
    vertical1 = calculate_euclidean_distance(p2, p6)
    vertical2 = calculate_euclidean_distance(p3, p5)

    # Calculate horizontal distance
    horizontal = calculate_euclidean_distance(p1, p4)

    # Avoid division by zero
    if horizontal == 0:
        return 0.0 # Return a default value
    
    # Calculate EAR
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear
    
def draw_face_landmarks_on_image(rgb_image, face_landmarks_list):
    annotated_image = np.copy(rgb_image)

    for face_landmarks in face_landmarks_list:
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
        ])

        left_eye_landmarks_proto = landmark_pb2.NormalizedLandmarkList(
            landmark=[face_landmarks_proto.landmark[i] for i in LEFT_EYE_INDICES]
        )

        right_eye_landmarks_proto = landmark_pb2.NormalizedLandmarkList(
            landmark=[face_landmarks_proto.landmark[i] for i in RIGHT_EYE_INDICES]
        )

        # Draw left eye
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=left_eye_landmarks_proto,
            connections=None, 
            landmark_drawing_spec=solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
            connection_drawing_spec=solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1)
        )

        # Draw right eye
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=right_eye_landmarks_proto,
            connections=None, 
            landmark_drawing_spec=solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
            connection_drawing_spec=solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1)
        )

    return annotated_image








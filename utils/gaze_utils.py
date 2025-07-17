import cv2
import numpy as np

# Gaze Score multiplier (Higher = more sensitive to eye movement)
# Too high: Jittery, overshoots
# Too low: Not responsive enough
x_score_multiplier = 15   # Horizontal gaze sensitivity 
y_score_multiplier = 5   # Vertical gaze sensitivity 

# Camera calibration adjustments (0.8-1.5)
focal_length_multiplier = 1.0   

# Iris movement adjustment
iris_sensitivity_multiplier = 3.5 

# 3D model points centered at left eye
leye_3d = np.array([
    [225.0, -175.0, 135.0],     # Nose tip (relative to left eye)
    [225.0, -505.0, 70.0],      # Chin (relative to left eye)
    [0.0, 0.0, 0.0],            # Left eye corner (origin)
    [450.0, 0.0, 0.0],          # Right eye corner (relative to left eye)
    [75.0, -325.0, 10.0],       # Left mouth corner (relative to left eye)
    [375.0, -325.0, 10.0]       # Right mouth corner (relative to left eye)
    ], dtype=np.float64)

# 3D model points centered at right eye  
reye_3d = np.array([
    [-225.0, -175.0, 135.0],    # Nose tip (relative to right eye)
    [-225.0, -505.0, 70.0],     # Chin (relative to right eye)
    [-450.0, 0.0, 0.0],         # Left eye corner (relative to right eye)
    [0.0, 0.0, 0.0],            # Right eye corner (origin)
    [-375.0, -325.0, 10.0],     # Left mouth corner (relative to right eye)
    [-75.0, -325.0, 10.0]       # Right mouth corner (relative to right eye)
    ], dtype=np.float64)

def calculate_gaze(img_w, img_h, face_landmarks):
    # Convert landmark x and y to pixel coords
    face_2d = [(lm.x * img_w, lm.y * img_h) for lm in face_landmarks]
    face_2d = np.asarray(face_2d)

    # Get relevant landmarks for headpose estimation  
    face_2d_head = np.array([
        face_2d[1],      # Nose
        face_2d[199],    # Chin
        face_2d[33],     # Left eye left corner
        face_2d[263],    # Right eye right corner
        face_2d[61],     # Left mouth corner
        face_2d[291]     # Right mouth corner
    ], dtype=np.float64)

    # Get eye corners as integers
    l_corner = face_2d_head[2].astype(np.int32)
    r_corner = face_2d_head[3].astype(np.int32)

    # Get eye centers coords by calculating the average of x and y of inner and outer eye corners
    left_eye_center = np.array([
        (face_2d[33][0] + face_2d[133][0]) / 2, 
        (face_2d[33][1] + face_2d[133][1]) / 2
    ], dtype=np.float32)
    
    right_eye_center = np.array([
        (face_2d[362][0] + face_2d[263][0]) / 2,  
        (face_2d[362][1] + face_2d[263][1]) / 2
    ], dtype=np.float32)
    
    # Get pupil coords by calculating the average position of iris landmarks
    left_iris_landmarks = [468, 469, 470, 471, 472]  
    right_iris_landmarks = [473, 474, 475, 476, 477]  
    
    left_pupil = np.array([
        np.mean([face_2d[idx][0] for idx in left_iris_landmarks]),
        np.mean([face_2d[idx][1] for idx in left_iris_landmarks])
    ], dtype=np.float32)
    
    right_pupil = np.array([
        np.mean([face_2d[idx][0] for idx in right_iris_landmarks]),
        np.mean([face_2d[idx][1] for idx in right_iris_landmarks])
    ], dtype=np.float32)
    
    # Get gaze vectors by calculating the displacement of the pupils from eye center
    left_gaze_vector = left_pupil - left_eye_center
    right_gaze_vector = right_pupil - right_eye_center
    
    # Adjust the gaze vectorw
    final_left_gaze_vector = np.array([
        left_gaze_vector[0] * iris_sensitivity_multiplier * x_score_multiplier,
        left_gaze_vector[1] * iris_sensitivity_multiplier * y_score_multiplier
    ])
    
    final_right_gaze_vector = np.array([
        right_gaze_vector[0] * iris_sensitivity_multiplier * x_score_multiplier, 
        right_gaze_vector[1] * iris_sensitivity_multiplier * y_score_multiplier
    ])

    # The camera matrix (adjusted with focal length multiplier)
    focal_length = focal_length_multiplier * img_w
    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                            [0, focal_length, img_w / 2],
                            [0, 0, 1]])

    # Distortion coefficients (assume webcam has only little distortion, hence set the value to zero)
    dist_coeffs = np.zeros((4, 1), dtype=np.float64)

    # Solve PnP to get rotational vector and translational vector
    _, l_rvec, l_tvec = cv2.solvePnP(leye_3d, face_2d_head, cam_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    _, r_rvec, r_tvec = cv2.solvePnP(reye_3d, face_2d_head, cam_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    # Create 3D eye gaze vector 
    left_gaze_3d = np.array([
        [final_left_gaze_vector[0] * 0.5, final_left_gaze_vector[1] * 0.5, 100],  # Near point
        [final_left_gaze_vector[0], final_left_gaze_vector[1], 300],  # Medium point
        [final_left_gaze_vector[0] * 1.5, final_left_gaze_vector[1] * 1.5, 500]   # Far point
    ], dtype=np.float32)
    
    right_gaze_3d = np.array([
        [final_right_gaze_vector[0] * 0.5, final_right_gaze_vector[1] * 0.5, 100],
        [final_right_gaze_vector[0], final_right_gaze_vector[1], 300],
        [final_right_gaze_vector[0] * 1.5, final_right_gaze_vector[1] * 1.5, 500]
    ], dtype=np.float32)
    
    # Project the 3D gaze vectors onto 2D image, to get the 2D pixel coords of each 3D points
    # Pass in rvec and tvec to take the rotational and translational vector of the eye into consideration (e.g. when user turns their head)
    l_gaze_points, _ = cv2.projectPoints(left_gaze_3d, l_rvec, l_tvec, cam_matrix, dist_coeffs)
    r_gaze_points, _ = cv2.projectPoints(right_gaze_3d, r_rvec, r_tvec, cam_matrix, dist_coeffs)
    
    # Get medium points
    l_gaze_point = tuple(np.ravel(l_gaze_points[1]).astype(np.int32))  
    r_gaze_point = tuple(np.ravel(r_gaze_points[1]).astype(np.int32))  
   
    # Calculate average gaze point (where both eyes are looking)
    avg_gaze_x = int((l_gaze_point[0] + r_gaze_point[0]) / 2)
    avg_gaze_y = int((l_gaze_point[1] + r_gaze_point[1]) / 2)
    
    # Determine looking direction
    x_looking_direction = "LEFT" if avg_gaze_x > (img_w / 2) else "RIGHT"
    y_looking_direction = "DOWN" if avg_gaze_y > (img_h / 2) else "UP"
    looking_direction = (x_looking_direction, y_looking_direction)

    return l_corner, r_corner, l_gaze_point, r_gaze_point, looking_direction
import cv2
import mediapipe as mp
import numpy as np

# Gaze Score multiplier (Higher = more sensitive to eye movement)
# - Too high: Jittery, overshoots
# - Too low: Not responsive enough
x_score_multiplier = 15   # Horizontal gaze sensitivity 
y_score_multiplier = 5   # Vertical gaze sensitivity 

# Smoothing threshold (Lower = more responsive, Higher = more stable)
threshold = 0.08

# Distance to project gaze points 
# Closer = more accurate for near objects, Further = better for distant estimation
gaze_projection_distance = 400 

# Camera calibration adjustments (0.8-1.5)
focal_length_multiplier = 1.0   

# Gaze offset corrections
x_offset_correction = 0         # Horizontal offset in pixels (-50 to +50)
y_offset_correction = 0         # Vertical offset in pixels (-50 to +50)

# Advanced smoothing (exponential moving average)
# lower = more responsiveness 
smoothing_factor = 0.5          

iris_sensitivity_multiplier = 5.0  # Additional multiplier for iris movement
iris_smoothing_factor = 0.3        # Separate smoothing for iris (more responsive)

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
    face_2d = []
    for lm in face_landmarks:
        # Convert landmark x and y to pixel coordinates
        x, y = int(lm.x * img_w), int(lm.y * img_h)
        # Add the 2D coordinates to an array
        face_2d.append((x, y))
    
    face_2d = np.asarray(face_2d)
    
    # Get eye centers (more accurate than corners for gaze)
    left_eye_center = np.array([
        (face_2d[33][0] + face_2d[133][0]) / 2,  # Average of left eye corners
        (face_2d[33][1] + face_2d[133][1]) / 2
    ], dtype=np.float32)
    
    right_eye_center = np.array([
        (face_2d[362][0] + face_2d[263][0]) / 2,  # Average of right eye corners  
        (face_2d[362][1] + face_2d[263][1]) / 2
    ], dtype=np.float32)
    
    # Get pupil positions with enhanced iris detection
    # Use multiple iris landmarks for better precision
    left_iris_landmarks = [468, 469, 470, 471, 472]  # Multiple iris points
    right_iris_landmarks = [473, 474, 475, 476, 477]  # Multiple iris points
    
    # Calculate average position of multiple iris landmarks
    left_pupil = np.array([
        np.mean([face_2d[idx][0] for idx in left_iris_landmarks]),
        np.mean([face_2d[idx][1] for idx in left_iris_landmarks])
    ], dtype=np.float32)
    
    right_pupil = np.array([
        np.mean([face_2d[idx][0] for idx in right_iris_landmarks]),
        np.mean([face_2d[idx][1] for idx in right_iris_landmarks])
    ], dtype=np.float32)
    
    # Calculate gaze vectors with enhanced sensitivity
    left_gaze_vector = left_pupil - left_eye_center
    right_gaze_vector = right_pupil - right_eye_center
    
    # Apply enhanced iris sensitivity
    left_gaze_vector *= iris_sensitivity_multiplier
    right_gaze_vector *= iris_sensitivity_multiplier
    
    # Apply iris-specific smoothing
    smooth_iris_lx = (1 - iris_smoothing_factor) * left_gaze_vector[0]
    smooth_iris_ly = (1 - iris_smoothing_factor) * left_gaze_vector[1]
    smooth_iris_rx = (1 - iris_smoothing_factor) * right_gaze_vector[0]
    smooth_iris_ry = (1 - iris_smoothing_factor) * right_gaze_vector[1]
    
    # Use smoothed values
    left_gaze_vector = np.array([smooth_iris_lx, smooth_iris_ly])
    right_gaze_vector = np.array([smooth_iris_rx, smooth_iris_ry])
    
    # Apply final gaze score adjustments
    left_gaze_adjusted = np.array([
        left_gaze_vector[0] * x_score_multiplier,
        left_gaze_vector[1] * y_score_multiplier
    ])
    
    right_gaze_adjusted = np.array([
        right_gaze_vector[0] * x_score_multiplier, 
        right_gaze_vector[1] * y_score_multiplier
    ])

    # Get relevant landmarks for headpose estimation  
    face_2d_head = np.array([
        face_2d[1],      # Nose
        face_2d[199],    # Chin
        face_2d[33],     # Left eye left corner
        face_2d[263],    # Right eye right corner
        face_2d[61],     # Left mouth corner
        face_2d[291]     # Right mouth corner
    ], dtype=np.float64)

    # Calculate left x gaze score
    if (face_2d[243,0] - face_2d[130,0]) != 0:
        lx_score = (face_2d[468,0] - face_2d[130,0]) / (face_2d[243,0] - face_2d[130,0])
        
        # Apply smoothing
        lx_score = (1 - smoothing_factor) * lx_score

    # Calculate left y gaze score
    if (face_2d[23,1] - face_2d[27,1]) != 0:
        ly_score = (face_2d[468,1] - face_2d[27,1]) / (face_2d[23,1] - face_2d[27,1])
        
        # Apply smoothing
        ly_score = (1 - smoothing_factor) * ly_score

    # Calculate right x gaze score
    if (face_2d[359,0] - face_2d[463,0]) != 0:
        rx_score = (face_2d[473,0] - face_2d[463,0]) / (face_2d[359,0] - face_2d[463,0])
        
        # Apply smoothing
        rx_score = (1 - smoothing_factor) * rx_score

    # Calculate right y gaze score
    if (face_2d[253,1] - face_2d[257,1]) != 0:
        ry_score = (face_2d[473,1] - face_2d[257,1]) / (face_2d[253,1] - face_2d[257,1])
        
        # Apply smoothing
        ry_score = (1 - smoothing_factor) * ry_score

    # The camera matrix (adjusted with focal length multiplier)
    focal_length = focal_length_multiplier * img_w
    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                            [0, focal_length, img_w / 2],
                            [0, 0, 1]])

    # Distortion coefficients 
    dist_coeffs = np.zeros((4, 1), dtype=np.float64)

    # Solve PnP
    _, l_rvec, l_tvec = cv2.solvePnP(leye_3d, face_2d_head, cam_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    _, r_rvec, r_tvec = cv2.solvePnP(reye_3d, face_2d_head, cam_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    # Get rotational matrix from rotational vector
    l_rmat, _ = cv2.Rodrigues(l_rvec)
    r_rmat, _ = cv2.Rodrigues(r_rvec)

    # Adjust headpose vector with gaze score
    l_gaze_rvec = np.array(l_rvec)
    l_gaze_rvec[2][0] -= (lx_score-.5) * x_score_multiplier
    l_gaze_rvec[0][0] += (ly_score-.5) * y_score_multiplier

    r_gaze_rvec = np.array(r_rvec)
    r_gaze_rvec[2][0] -= (rx_score-.5) * x_score_multiplier
    r_gaze_rvec[0][0] += (ry_score-.5) * y_score_multiplier

    # --- Projection ---

    # Get eye corners as integers
    l_corner = face_2d_head[2].astype(np.int32)
    r_corner = face_2d_head[3].astype(np.int32)

    # Calculate actual gaze vectors based on enhanced pupil displacement
    # Left eye gaze vector (from eye center to pupil, projected forward)
    left_gaze_3d = np.array([
        [left_gaze_adjusted[0] * 0.5, left_gaze_adjusted[1] * 0.5, 100],  # Near point
        [left_gaze_adjusted[0], left_gaze_adjusted[1], 300],  # Medium point
        [left_gaze_adjusted[0] * 1.5, left_gaze_adjusted[1] * 1.5, 500]   # Far point
    ], dtype=np.float32)
    
    # Right eye gaze vector  
    right_gaze_3d = np.array([
        [right_gaze_adjusted[0] * 0.5, right_gaze_adjusted[1] * 0.5, 100],
        [right_gaze_adjusted[0], right_gaze_adjusted[1], 300],
        [right_gaze_adjusted[0] * 1.5, right_gaze_adjusted[1] * 1.5, 500]
    ], dtype=np.float32)
    
    # Project the actual gaze vectors
    l_gaze_points, _ = cv2.projectPoints(left_gaze_3d, l_rvec, l_tvec, cam_matrix, dist_coeffs)
    r_gaze_points, _ = cv2.projectPoints(right_gaze_3d, r_rvec, r_tvec, cam_matrix, dist_coeffs)
    
    l_gaze_point = tuple(np.ravel(l_gaze_points[1]).astype(np.int32))  # Medium distance point
    r_gaze_point = tuple(np.ravel(r_gaze_points[1]).astype(np.int32))  # Medium distance point
   
    # Calculate average gaze point (where both eyes are looking)
    avg_gaze_x = int((l_gaze_point[0] + r_gaze_point[0]) / 2)
    avg_gaze_y = int((l_gaze_point[1] + r_gaze_point[1]) / 2)
    avg_gaze_point = (avg_gaze_x, avg_gaze_y)
        
    x_looking_direction = "LEFT" if avg_gaze_x > (img_w / 2) else "RIGHT"
    y_looking_direction = "DOWN" if avg_gaze_y > (img_h / 2) else "UP"
    looing_direction = (x_looking_direction, y_looking_direction)

    return l_corner, r_corner, l_gaze_points, r_gaze_points, l_gaze_point, r_gaze_point, avg_gaze_point, looing_direction
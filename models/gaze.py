import cv2
import mediapipe as mp
import numpy as np

draw_gaze = True
draw_full_axis = True
draw_gaze_points = True 

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

iris_sensitivity_multiplier = 3.0  # Additional multiplier for iris movement
iris_smoothing_factor = 0.3        # Separate smoothing for iris (more responsive)

# Gaze amplification parameters
gaze_amplification_base = 2.0      # Base multiplier for gaze displacement
gaze_amplification_scaling = 0.15  # Additional scaling based on displacement magnitude (adjust for sensitivity)
max_gaze_amplification = 5.0       # Maximum amplification to prevent extreme values

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
    refine_landmarks=True,
    max_num_faces=2,
    min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

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

# Initialize all smoothing variables
last_lx, last_rx = 0, 0
last_ly, last_ry = 0, 0
smooth_lx, smooth_rx = 0, 0
smooth_ly, smooth_ry = 0, 0
smooth_iris_lx, smooth_iris_rx = 0, 0
smooth_iris_ly, smooth_iris_ry = 0, 0

def calculate_gaze_point(eye_corner, gaze_rvec, tvec, cam_matrix, dist_coeffs, pupil_displacement=None, distance=500):
    """
    Calculate where the gaze vector intersects with screen plane
    Using proper 3D projection from rotation vector with enhanced pupil displacement
    """
    # Base gaze point
    gaze_point_3d = np.array([[0, 0, distance]], dtype=np.float32)
    
    # If pupil displacement is provided, amplify the gaze direction
    if pupil_displacement is not None:
        # Calculate displacement magnitude for dynamic multiplier
        displacement_magnitude = np.sqrt(pupil_displacement[0]**2 + pupil_displacement[1]**2)
        
        # Dynamic multiplier based on displacement (increases with distance from center)
        # Base multiplier + additional scaling based on how far pupil is from center
        dynamic_multiplier = gaze_amplification_base + (displacement_magnitude * gaze_amplification_scaling)
        
        # Clamp the multiplier to prevent extreme values
        dynamic_multiplier = min(dynamic_multiplier, max_gaze_amplification)
        
        # Apply enhanced displacement to gaze direction
        enhanced_x = pupil_displacement[0] * dynamic_multiplier
        enhanced_y = pupil_displacement[1] * dynamic_multiplier
        
        # Modify the 3D gaze point based on pupil displacement
        gaze_point_3d = np.array([[enhanced_x, enhanced_y, distance]], dtype=np.float32)
    
    # Project the 3D gaze point to 2D screen coordinates
    gaze_point_2d, _ = cv2.projectPoints(gaze_point_3d, gaze_rvec, tvec, cam_matrix, dist_coeffs)
    
    # Extract coordinates and apply offset corrections
    gaze_x = int(gaze_point_2d[0][0][0] + x_offset_correction)
    gaze_y = int(gaze_point_2d[0][0][1] + y_offset_correction)
    
    return (gaze_x, gaze_y)

def calculate_3d_gaze_direction(eye_corner, pupil_2d, rvec, tvec, cam_matrix, dist_coeffs):
    """
    Calculate 3D gaze direction more accurately using pupil position relative to eye corner
    """
    # Calculate gaze direction in 2D
    gaze_2d = np.array([pupil_2d[0] - eye_corner[0], pupil_2d[1] - eye_corner[1]], dtype=np.float32)
    
    # Convert to 3D direction (simplified approach)
    # This assumes the eye is looking in the direction proportional to pupil displacement
    gaze_3d = np.array([gaze_2d[0], gaze_2d[1], 0], dtype=np.float32)
    
    return gaze_3d

while cap.isOpened():
    success, img = cap.read()
    
    if not success:
        continue

    # Flip + convert img from BGR to RGB
    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    img.flags.writeable = False
    
    # Get the result
    results = face_mesh.process(img)
    img.flags.writeable = True
    
    # Convert the color space from RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    (img_h, img_w, img_c) = img.shape

    if not results.multi_face_landmarks:
        cv2.imshow('Head Pose Estimation', img)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
        continue 

    for face_landmarks in results.multi_face_landmarks:
        face_2d = []
        for idx, lm in enumerate(face_landmarks.landmark):
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
        smooth_iris_lx = iris_smoothing_factor * smooth_iris_lx + (1 - iris_smoothing_factor) * left_gaze_vector[0]
        smooth_iris_ly = iris_smoothing_factor * smooth_iris_ly + (1 - iris_smoothing_factor) * left_gaze_vector[1]
        smooth_iris_rx = iris_smoothing_factor * smooth_iris_rx + (1 - iris_smoothing_factor) * right_gaze_vector[0]
        smooth_iris_ry = iris_smoothing_factor * smooth_iris_ry + (1 - iris_smoothing_factor) * right_gaze_vector[1]
        
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
            smooth_lx = smoothing_factor * smooth_lx + (1 - smoothing_factor) * lx_score
            lx_score = smooth_lx
            last_lx = lx_score

        # Calculate left y gaze score
        if (face_2d[23,1] - face_2d[27,1]) != 0:
            ly_score = (face_2d[468,1] - face_2d[27,1]) / (face_2d[23,1] - face_2d[27,1])
            
            # Apply smoothing
            smooth_ly = smoothing_factor * smooth_ly + (1 - smoothing_factor) * ly_score
            ly_score = smooth_ly
            last_ly = ly_score

        # Calculate right x gaze score
        if (face_2d[359,0] - face_2d[463,0]) != 0:
            rx_score = (face_2d[473,0] - face_2d[463,0]) / (face_2d[359,0] - face_2d[463,0])
            
            # Apply smoothing
            smooth_rx = smoothing_factor * smooth_rx + (1 - smoothing_factor) * rx_score
            rx_score = smooth_rx
            last_rx = rx_score

        # Calculate right y gaze score
        if (face_2d[253,1] - face_2d[257,1]) != 0:
            ry_score = (face_2d[473,1] - face_2d[257,1]) / (face_2d[253,1] - face_2d[257,1])
            
            # Apply smoothing
            smooth_ry = smoothing_factor * smooth_ry + (1 - smoothing_factor) * ry_score
            ry_score = smooth_ry
            last_ry = ry_score

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
        
        # Draw actual gaze vectors for left eye
        if draw_gaze:
            # Draw gaze line from eye corner through the projected gaze points
            if draw_full_axis:
                # Draw to near gaze point
                cv2.line(img, l_corner, tuple(np.ravel(l_gaze_points[0]).astype(np.int32)), (255,0,0), 2)
            # Draw to far gaze point (main gaze line)
            cv2.line(img, l_corner, tuple(np.ravel(l_gaze_points[2]).astype(np.int32)), (0,0,255), 3)

        # Draw actual gaze vectors for right eye
        if draw_gaze:
            # Draw gaze line from eye corner through the projected gaze points
            if draw_full_axis:
                # Draw to near gaze point  
                cv2.line(img, r_corner, tuple(np.ravel(r_gaze_points[0]).astype(np.int32)), (255,0,0), 2)
            # Draw to far gaze point (main gaze line)
            cv2.line(img, r_corner, tuple(np.ravel(r_gaze_points[2]).astype(np.int32)), (0,0,255), 3)

        # Calculate and draw gaze points
        if draw_gaze_points:
            # Calculate gaze points using enhanced method with pupil displacement
            l_gaze_point = calculate_gaze_point(l_corner, l_gaze_rvec, l_tvec, cam_matrix, dist_coeffs, 
                                              pupil_displacement=left_gaze_adjusted, distance=300)
            r_gaze_point = calculate_gaze_point(r_corner, r_gaze_rvec, r_tvec, cam_matrix, dist_coeffs, 
                                              pupil_displacement=right_gaze_adjusted, distance=300)
            
            # Draw gaze points as circles
            if 0 <= l_gaze_point[0] < img_w and 0 <= l_gaze_point[1] < img_h:
                cv2.circle(img, l_gaze_point, 8, (255, 0, 255), -1)  # Magenta circle for left eye
                cv2.circle(img, l_gaze_point, 12, (255, 255, 255), 2)  # White border
                cv2.putText(img, 'L', (l_gaze_point[0]-5, l_gaze_point[1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
            if 0 <= r_gaze_point[0] < img_w and 0 <= r_gaze_point[1] < img_h:
                cv2.circle(img, r_gaze_point, 8, (0, 255, 255), -1)  # Cyan circle for right eye
                cv2.circle(img, r_gaze_point, 12, (255, 255, 255), 2)  # White border
                cv2.putText(img, 'R', (r_gaze_point[0]-5, r_gaze_point[1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
            # Calculate average gaze point (where both eyes are looking)
            avg_gaze_x = int((l_gaze_point[0] + r_gaze_point[0]) / 2)
            avg_gaze_y = int((l_gaze_point[1] + r_gaze_point[1]) / 2)
            avg_gaze_point = (avg_gaze_x, avg_gaze_y)
            
            # Draw average gaze point
            if 0 <= avg_gaze_point[0] < img_w and 0 <= avg_gaze_point[1] < img_h:
                cv2.circle(img, avg_gaze_point, 10, (0, 255, 0), -1)  # Green circle for average gaze
                cv2.circle(img, avg_gaze_point, 15, (255, 255, 255), 2)  # White border
                cv2.putText(img, 'GAZE', (avg_gaze_point[0]-20, avg_gaze_point[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow('Head Pose Estimation', img)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
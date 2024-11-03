import time
from imutils import face_utils
import dlib
import cv2
import numpy as np

# Load dlib's detector and predictor
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv2.VideoCapture(0)

# Variables for head movement detection
head_turn_start_time = None
HEAD_TURN_THRESHOLD = 1  # seconds to trigger warning


# Function to detect gaze direction
def detect_eye_gaze(eye_points, gray):
    # Extract the eye region
    (x, y, w, h) = cv2.boundingRect(np.array([eye_points]))
    eye = gray[y:y + h, x:x + w]

    # Thresholding to isolate the pupil
    _, threshold_eye = cv2.threshold(eye, 70, 255, cv2.THRESH_BINARY_INV)

    # Calculate moments to find the center of the pupil
    moments = cv2.moments(threshold_eye)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])  # x coordinate of pupil
        # Determine direction based on the position of pupil
        if cx < w * 0.3:
            return "Looking Left"
        elif cx > w * 0.7:
            return "Looking Right"
        else:
            return "Looking Center"
    return "Not Detected"


while True:
    # Capture frame and convert to grayscale
    _, image = cap.read()
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    rects = detector(gray, 0)

    # Process each face detected
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract left and right eye landmarks
        left_eye = shape[36:42]
        right_eye = shape[42:48]

        # Detect eye gaze direction
        left_eye_direction = detect_eye_gaze(left_eye, gray)
        right_eye_direction = detect_eye_gaze(right_eye, gray)

        # Display gaze direction
        cv2.putText(image, f"Left Eye: {left_eye_direction}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(image, f"Right Eye: {right_eye_direction}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Track head movement by monitoring nose position (landmark 30)
        nose_point = shape[30]
        mid_x = (shape[36][0] + shape[45][0]) / 2  # Midpoint between the eyes
        if nose_point[0] < mid_x - 10:
            if head_turn_start_time is None:
                head_turn_start_time = time.time()
            elif time.time() - head_turn_start_time > HEAD_TURN_THRESHOLD:
                cv2.putText(image, "Warning: Look at the screen!", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            head_turn_start_time = None  # Reset timer if head returns to center

        # Draw landmarks
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    # Show the result
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

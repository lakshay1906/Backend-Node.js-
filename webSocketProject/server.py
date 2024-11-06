from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import base64
import numpy as np
import dlib
import time

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Ensure this file is in the correct path

# Threshold for head movement duration
HEAD_TURN_THRESHOLD = 1  # seconds to trigger warning
head_turn_start_time = None

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

def detect_movement(frame):
    global head_turn_start_time
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    left_eye_movement = "none"
    right_eye_movement = "none"
    head_movement = "none"

    for face in faces:
        shape = predictor(gray, face)
        shape_np = np.array([[p.x, p.y] for p in shape.parts()])

        # Extract left and right eye landmarks
        left_eye_points = shape_np[36:42]
        right_eye_points = shape_np[42:48]

        # Detect eye gaze direction
        left_eye_movement = detect_eye_gaze(left_eye_points, gray)
        right_eye_movement = detect_eye_gaze(right_eye_points, gray)

        # Track head movement by monitoring nose position (landmark 30)
        nose_point = shape_np[30]
        mid_x = (shape_np[36][0] + shape_np[45][0]) / 2  # Midpoint between the eyes

        # Determine head movement direction
        if nose_point[0] < mid_x - 10:
            if head_turn_start_time is None:
                head_turn_start_time = time.time()
            elif time.time() - head_turn_start_time > HEAD_TURN_THRESHOLD:
                head_movement = "left"
        elif nose_point[0] > mid_x + 10:
            if head_turn_start_time is None:
                head_turn_start_time = time.time()
            elif time.time() - head_turn_start_time > HEAD_TURN_THRESHOLD:
                head_movement = "right"
        else:
            head_turn_start_time = None  # Reset timer if head returns to center
            head_movement = "center"

    return left_eye_movement, right_eye_movement, head_movement

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("connection open")
    try:
        while True:
            try:
                data = await websocket.receive_text()

                if not data.startswith("data:image/jpeg;base64,"):
                    print("Received empty or malformed data")
                    continue

                # Extract base64 part
                img_data = base64.b64decode(data.split(",")[1])
                np_arr = np.frombuffer(img_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # Detect movements
                left_eye_movement, right_eye_movement, head_movement = detect_movement(frame)

                # Send detection results back to the client
                await websocket.send_json({
                    "left_eye_movement": left_eye_movement,
                    "right_eye_movement": right_eye_movement,
                    "head_movement": head_movement
                })

            except WebSocketDisconnect:
                print("WebSocket disconnected")
                break
            except Exception as e:
                print("Error processing frame:", e)

    finally:
        await websocket.close()
        print("connection closed")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import base64
import numpy as np
import dlib

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
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Make sure to provide the correct path

def detect_movement(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    left_eye_movement = "none"
    right_eye_movement = "none"
    head_movement = "none"

    for face in faces:
        landmarks = predictor(gray, face)

        # Get landmark points for eyes and nose
        left_eye_x = landmarks.part(36).x
        right_eye_x = landmarks.part(45).x
        nose_x = landmarks.part(33).x

        # Determine head movement
        if nose_x < left_eye_x:
            head_movement = "left"
        elif nose_x > right_eye_x:
            head_movement = "right"
        else:
            head_movement = "center"

        # Determine eye movement
        if left_eye_x < face.left() + 30:  # Example threshold
            left_eye_movement = "left"
        if right_eye_x > face.right() - 30:  # Example threshold
            right_eye_movement = "right"

    return left_eye_movement, right_eye_movement, head_movement

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("connection open")
    try:
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Received data: {data[:100]}...")  # Log the beginning of the data to inspect format

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

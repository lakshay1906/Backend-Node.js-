import React, { useEffect, useRef, useState } from "react";

function App() {
  const [movementData, setMovementData] = useState({});
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const socketRef = useRef(null);

  useEffect(() => {
    // Start video stream
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    });

    // Set up WebSocket connection
    socketRef.current = new WebSocket("ws://localhost:8000/ws");

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMovementData(data);
    };

    return () => socketRef.current.close();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imgData = canvas.toDataURL("image/jpeg"); // Full data URL
      console.log("Sending data:", imgData); // Log the data before sending
      if (socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(imgData); // Send full data URL
      }
    }, 200); // Send frame every 200ms

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center" }}>
      <h1>Examination</h1>
      <video ref={videoRef} style={{ display: "block" }} />
      <canvas ref={canvasRef} style={{ display: "block" }} />
      <div>
        <h2>Movement Data</h2>
        <p>Left Eye Movement: {movementData.left_eye_movement}</p>
        <p>Right Eye Movement: {movementData.right_eye_movement}</p>
        <p>Head Movement: {movementData.head_movement}</p>
      </div>
    </div>
  );
}

export default App;

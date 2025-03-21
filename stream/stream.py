import socket
import cv2
import numpy as np
import torch

# Load YOLO model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # Change this if using a custom model

# Server settings
HOST = "0.0.0.0"  
PORT = 5001

# Create and bind the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("🚀 Waiting for connection...")

# Accept connection
conn, addr = server_socket.accept()
print(f"✅ Connected by {addr}")

# Receive and process video stream
data = b""
while True:
    packet = conn.recv(4096)
    if not packet:
        break
    data += packet

    while b"\xff\xd8" in data and b"\xff\xd9" in data:
        start = data.index(b"\xff\xd8")
        end = data.index(b"\xff\xd9") + 2
        jpg_data = data[start:end]
        data = data[end:]

        # Convert bytes to OpenCV frame
        image = np.frombuffer(jpg_data, dtype=np.uint8)
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Run YOLO on the frame
        results = model(frame)

        # Draw YOLO detections
        for *box, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = map(int, box)
            label = f"{model.names[int(cls)]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the processed video
        cv2.imshow("🛠 YOLO Detection", frame)
        if cv2.waitKey(1) == ord("q"):
            break

conn.close()
server_socket.close()
cv2.destroyAllWindows()

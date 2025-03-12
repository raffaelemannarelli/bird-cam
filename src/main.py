from ultralytics import YOLO
import torch

# Load a model
model = YOLO("yolo11n.pt")

# Set the device (force MPS if available)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

# Train the model
results = model.train(data="../yolo_dataset/dataset.yaml", epochs=100, imgsz=640, device=device)

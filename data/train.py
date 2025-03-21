from ultralytics import YOLO
import torch
from pathlib import Path

# Get the directory of the current script
SCRIPT_DIR = Path(__file__).parent

# Load a model
model = YOLO("yolo11n.pt")

# Set the device (force MPS if available)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

# Train the model
dataset_path = SCRIPT_DIR / "yolo_dataset/dataset.yaml"
results = model.train(data=str(dataset_path), epochs=100, imgsz=640, device=device)
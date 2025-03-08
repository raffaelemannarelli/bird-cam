# NABirds to YOLO Dataset Conversion

This repository provides a complete pipeline to convert the NABirds dataset into the YOLO format for training object detection models. The script processes images, bounding boxes, and class labels to create a structured dataset ready for YOLO training.

## Features
- Converts NABirds dataset annotations into YOLO format.
- Organizes images and labels into `train/` and `val/` directories.
- Normalizes bounding boxes for YOLO compatibility.
- Generates a `dataset.yaml` file for seamless YOLO training.
- Includes a setup script to install dependencies and run the conversion.

## Directory Structure
```
/your_project
│── script.py                # Main Python script for conversion
│── setup.sh                 # Shell script for environment setup
│── requirements.txt         # Required Python packages
│── yolo_dataset             # Output dataset for YOLO training
│   ├── images
│   │   ├── train            # Training images
│   │   ├── val              # Validation images
│   ├── labels
│   │   ├── train            # YOLO annotation files for training
│   │   ├── val              # YOLO annotation files for validation
│   ├── dataset.yaml         # YOLO dataset configuration
```

## Setup & Installation
### **1. Download the NABirds Dataset**
You need to manually download the NABirds dataset from the following link:
[NABirds Dataset](https://dl.allaboutbirds.org/merlin---computer-vision--terms-of-use?submissionGuid=2a2b6860-3abc-40f6-b736-f87f9f39e722)

Extract the dataset into your project directory.

### **2. Clone the Repository**
```bash
git clone https://github.com/raffaelemannarelli/bird-cam.git
```

### **3. Run the Setup Script**
```bash
chmod +x setup.sh
source ./setup.sh
```
This will create a virtual environment, install dependencies, and run the conversion script.

## Usage
Once the dataset is converted, you can train a YOLO model using **Ultralytics YOLOv8**:
```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(data="yolo_dataset/dataset.yaml", epochs=50, imgsz=640)
```

## Requirements
- Python 3.x
- `pandas`, `tqdm`, `shutil`, `pathlib`
- YOLOv8 (optional for training)

## Credits
This project is based on the **NABirds dataset**, created by the Cornell Lab of Ornithology.

## License
This repository is available for educational and research purposes.


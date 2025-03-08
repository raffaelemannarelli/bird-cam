from pathlib import Path
import shutil
import pandas as pd
from tqdm import tqdm

# Define paths
DATASET_DIR = Path("/Users/raffaelemannarelli/vision/nabirds")  # Change this to the NABirds dataset path
IMAGES_DIR = DATASET_DIR / "images"
OUTPUT_DIR = Path("yolo_dataset")
TRAIN_IMG_DIR = OUTPUT_DIR / "images/train"
VAL_IMG_DIR = OUTPUT_DIR / "images/val"
TRAIN_LABEL_DIR = OUTPUT_DIR / "labels/train"
VAL_LABEL_DIR = OUTPUT_DIR / "labels/val"

# Create necessary directories
for dir in [TRAIN_IMG_DIR, VAL_IMG_DIR, TRAIN_LABEL_DIR, VAL_LABEL_DIR]:
    dir.mkdir(parents=True, exist_ok=True)

# Load dataset files
images = pd.read_csv(DATASET_DIR / "images.txt", sep=" ", header=None, names=["image_id", "filename"])
labels = pd.read_csv(DATASET_DIR / "image_class_labels.txt", sep=" ", header=None, names=["image_id", "class_id"])
bboxes = pd.read_csv(DATASET_DIR / "bounding_boxes.txt", sep=" ", header=None, names=["image_id", "x", "y", "width", "height"])
sizes = pd.read_csv(DATASET_DIR / "sizes.txt", sep=" ", header=None, names=["image_id", "img_width", "img_height"])
split_info = pd.read_csv(DATASET_DIR / "train_test_split.txt", sep=" ", header=None, names=["image_id", "is_train"])

# Merge information into a single DataFrame
data = images.merge(labels, on="image_id").merge(bboxes, on="image_id").merge(sizes, on="image_id").merge(split_info, on="image_id")

# Process images and labels
for _, row in tqdm(data.iterrows(), total=len(data)):
    img_path = IMAGES_DIR / row["filename"]

    label_filename = row["filename"].replace(".jpg", ".txt")
    # remove the dir name in the label_filename
    label_filename = label_filename.split('/')[1]
    
    class_id = row["class_id"] - 1  # Adjust class ID to start from 0

    # YOLO format normalization
    x_center = (row["x"] + row["width"] / 2) / row["img_width"]
    y_center = (row["y"] + row["height"] / 2) / row["img_height"]
    norm_width = row["width"] / row["img_width"]
    norm_height = row["height"] / row["img_height"]

    label_content = f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}\n"

    # Train or validation split
    if row["is_train"] == 1:
        img_dest = TRAIN_IMG_DIR / row["filename"].split('/')[1]
        label_dest = TRAIN_LABEL_DIR / label_filename
    else:
        img_dest = VAL_IMG_DIR / row["filename"].split('/')[1]
        label_dest = VAL_LABEL_DIR / label_filename

    # Ensure the destination directory exists
    img_dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy image
    shutil.copy(img_path, img_dest)
    
    # Write YOLO label file
    with open(label_dest, "w") as f:
        f.write(label_content)
    

# Create dataset.yaml file
dataset_yaml = f"""
train: {TRAIN_IMG_DIR.resolve()}
val: {VAL_IMG_DIR.resolve()}
nc: 555  # Number of classes
names: ["species_1", "species_2", ..., "species_555"]  # Replace with actual names
"""

with open(OUTPUT_DIR / "dataset.yaml", "w") as f:
    f.write(dataset_yaml)

print("NABirds dataset converted to YOLO format successfully!")
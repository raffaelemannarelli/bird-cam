import requests
import os
import tarfile
from tqdm import tqdm  # Import tqdm for progress bar
from pathlib import Path
import shutil
import pandas as pd

# Step 1: Download and extract the dataset
# Dropbox shared link
url = "https://www.dropbox.com/scl/fi/yas70u9uzkeyzrmrfwcru/nabirds.tar.gz?rlkey=vh0uduhckom5jyp73igjugqtr&e=1&dl=1"

# File name and destination
output_file = "nabirds.tar.gz"
output_dir = "nabirds"

# Download the file
print("Downloading dataset...")
response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))  # Get total file size
with open(output_file, "wb") as file, tqdm(
    desc="Downloading",
    total=total_size,
    unit="B",
    unit_scale=True,
    unit_divisor=1024,
) as progress_bar:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))  # Update progress bar

print("Download complete!")

# Extract the file
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Extracting dataset...")
with tarfile.open(output_file, "r:gz") as tar:
    tar.extractall(path=output_dir)

print(f"Dataset extracted to {output_dir}")

# Optional: Remove the tar file after extraction
os.remove(output_file)
print("Cleanup complete!")

# Step 2: Process the dataset (existing code)
# Define paths
DATASET_DIR = Path.cwd() / "nabirds"
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

# move the dataset.yaml to the pthe yolo_dataset directory
shutil.move('dataset.yaml', OUTPUT_DIR)

print("NABirds dataset converted to YOLO format successfully!")
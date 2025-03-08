#!/bin/bash

# Define paths
BASE_DIR=$(dirname "$(realpath "$0")")
REQUIREMENTS_FILE="$BASE_DIR/requirements.txt"
NABIRDS_ZIP="$BASE_DIR/nabirds.zip"
NABIRDS_DIR="$BASE_DIR/nabirds"
SCRIPT_FILE="$BASE_DIR/script/script.py"

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r "$REQUIREMENTS_FILE"

# Run the script
echo "Running the script..."
python "$SCRIPT_FILE"

echo "Setup completed successfully!"

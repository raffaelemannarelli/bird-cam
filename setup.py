import os
import subprocess
import zipfile

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, 'requirements.txt')
NABIRDS_ZIP = os.path.join(BASE_DIR, 'nabirds.zip')
NABIRDS_DIR = os.path.join(BASE_DIR, 'nabirds')
SCRIPT_FILE = os.path.join(BASE_DIR, 'script', 'script.py')

# create the venv venv
subprocess.check_call([os.sys.executable, '-m', 'venv', 'venv'])
# activate the venv
subprocess.check_call(['venv/bin/activate'])

# Install packages from requirements.txt
subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', '-r', REQUIREMENTS_FILE])

# Run the script in script.py
subprocess.check_call([os.sys.executable, SCRIPT_FILE])

print("Setup completed successfully!")
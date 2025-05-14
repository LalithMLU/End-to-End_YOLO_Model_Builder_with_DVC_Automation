import os
import configparser
import zipfile
from pathlib import Path
import shutil
import yaml

# Function to read the configuration file
def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

# Function to create directory if it does not exist
def create_directory_if_not_exists(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        try:
            # Create the directory if it does not exist
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{directory_path}': {e}")
    else:
        print(f"Directory '{directory_path}' already exists.")

# Function to determine the next version number for images or labels
def get_next_version(target_path):
    existing_versions = [d for d in os.listdir(target_path) if os.path.isdir(os.path.join(target_path, d))]
    version_numbers = []

    for version in existing_versions:
        if version.startswith("v"):
            try:
                version_number = int(version[1:])
                version_numbers.append(version_number)
            except ValueError:
                pass

    if version_numbers:
        next_version = max(version_numbers) + 1
    else:
        next_version = 1

    return next_version

# Function to extract ZIP files and segregate the contents
def extract_and_segregate(zip_directory, img_base_path, label_base_path):
    next_version = max(get_next_version(img_base_path), get_next_version(label_base_path))
    versioned_img_path = os.path.join(img_base_path, f"v{next_version}")
    versioned_label_path = os.path.join(label_base_path, f"v{next_version}")

    create_directory_if_not_exists(versioned_img_path)
    create_directory_if_not_exists(versioned_label_path)

    for zip_file in Path(zip_directory).glob("*.zip"):
        print(f"Processing ZIP file: {zip_file}")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Find all files within the 'obj_train_data' folder in the ZIP archive
                obj_train_data_files = [f for f in zip_ref.namelist() if f.startswith('obj_train_data/')]

                if not obj_train_data_files:
                    print(f"No 'obj_train_data' folder found in {zip_file}, skipping...")
                    continue

                for file_name in obj_train_data_files:
                    # Get the file's relative path without the 'obj_train_data/' prefix
                    relative_path = file_name[len('obj_train_data/'):]

                    if relative_path:  # Check if there is a valid file path after the prefix
                        if relative_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")):
                            dest_path = os.path.join(versioned_img_path, os.path.basename(relative_path))
                        elif relative_path.lower().endswith(".txt"):
                            dest_path = os.path.join(versioned_label_path, os.path.basename(relative_path))
                        else:
                            print(f"Skipping unsupported file type: {relative_path}")
                            continue

                        # Extract the file to the appropriate directory
                        with zip_ref.open(file_name) as source, open(dest_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                            print(f"Extracted: {relative_path} to {dest_path}")


            # Remove the ZIP file after extraction
            if zip_directory.exists():
                zip_directory.unlink()

            print(f"Deleted the ZIP file: {zip_directory}")

            print(f"Successfully processed ZIP file: {zip_file}")

        except zipfile.BadZipFile:
            print(f"Error: '{zip_file}' is not a valid ZIP file.")
        except Exception as e:
            print(f"An error occurred while processing '{zip_file}': {e}")
            
# Function to read and parse the parameters from a YAML file
def read_params(file_path):
    with open(file_path, "r") as file:
        params = yaml.safe_load(file)  # Load YAML content
    return params

def evm():
    params = read_params('/path/to/params.yaml')
    zip_directory = params['export']['zip_path']
    target_directory_imgs = params['export']['target_directoryimgs']
    target_directory_labels = params['export']['target_directorylabels']

    # Check and create directories for images and labels
    create_directory_if_not_exists(target_directory_imgs)
    create_directory_if_not_exists(target_directory_labels)

    extract_and_segregate(zip_directory, target_directory_imgs, target_directory_labels)
    
    
    for filename in os.listdir(zip_directory):
        # Construct the full file path
        file_path = os.path.join(zip_directory, filename)
        # Check if the file is a ZIP file and if it's actually a file (not a directory)
        if filename.endswith(".zip") and os.path.isfile(file_path):
            os.remove(file_path)  # Remove the ZIP file
            print(f"Deleted: {file_path}")

    print("All ZIP files have been cleared from the directory=>",zip_directory)




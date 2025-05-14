import os
import shutil
import glob
import random
import yaml

# Function to read and parse the parameters from a YAML file
def read_params(file_path):
    with open(file_path, "r") as file:
        params = yaml.safe_load(file)  # Load YAML content
    return params

def get_latest_folder(base_path):
    """Get the latest folder from the base path"""
    folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not folders:
        raise ValueError(f"No folders found in {base_path}")
    return max(folders, key=os.path.getmtime)  # Get the most recently modified folder

def fetch_images_and_labels(imgs_path, labels_path):
    """Recursively fetch images and their corresponding labels"""
    images = glob.glob(os.path.join(imgs_path, "*.jpg"))  # Modify if different format (e.g., PNG)
    labels = []
    
    for img in images:
        label_file = os.path.join(labels_path, os.path.basename(img).replace(".jpg", ".txt"))
        if os.path.exists(label_file):
            labels.append((img, label_file))
    
    return labels

def split_data(imgs_path, labels_path, output_dir, train_ratio=0.8, val_ratio=0.2, test_ratio=0):
    """Splits images and labels into train, val, and test sets for YOLO training."""
    os.makedirs(output_dir, exist_ok=True)
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(output_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'labels', split), exist_ok=True)

    labels = fetch_images_and_labels(imgs_path, labels_path)
    random.shuffle(labels)
    
    train_split = int(len(labels) * train_ratio)
    val_split = int(len(labels) * (train_ratio + val_ratio))
    
    splits = {
        'train': labels[:train_split],
        'valid': labels[train_split:val_split],
        'test': labels[val_split:]
    }

    for split, label_pairs in splits.items():
        for img, label in label_pairs:
            shutil.copy(img, os.path.join(output_dir, 'images', split))
            shutil.copy(label, os.path.join(output_dir, 'labels', split))
    
    print("Data split complete!")

if __name__ == "__main__":
    params = read_params('/path/to/params.yaml')  # Use raw string for Windows paths
    imgs_folder = get_latest_folder(params['split']['images_folder'])
    labels_folder = get_latest_folder(params['split']['labels_folder'])
    output_directory = params['split']['yolo_dataset']
    
    split_data(imgs_folder, labels_folder, output_directory)

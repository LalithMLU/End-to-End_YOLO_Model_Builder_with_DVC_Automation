import os
import glob
import yaml
import shutil
import re
from ultralytics import YOLO

# === Step 1: Load params.yaml ===
with open('/path/to/params.yaml', 'r') as file:
    params = yaml.safe_load(file)

plant = params['train']['plant']
epochs = params['train'].get('epochs', 30)
imgsz = params['train'].get('imgsz', 640)
class_names = params['train']['classes']
num_classes = len(class_names)

# === Step 2: Define paths ===
dataset_dir = params['train']['yolo_dataset']
model_dir = os.path.join('models', plant, 'pytorch')

# Ensure dataset directory exists before writing data.yaml
os.makedirs(dataset_dir, exist_ok=True)
data_yaml_path = os.path.join(dataset_dir, 'data.yaml')

# === Step 3: Write data.yaml ===
data_yaml_content = {
    'train': os.path.join(dataset_dir, 'images/train'),
    'val': os.path.join(dataset_dir, 'images/val'),
    'nc': num_classes,
    'names': class_names
}
with open(data_yaml_path, 'w') as f:
    yaml.dump(data_yaml_content, f)

# === Step 4: Get latest .pt model ===
pt_files = glob.glob(os.path.join(model_dir, '*.pt'))
if not pt_files:
    raise FileNotFoundError(f"No .pt files found in {model_dir}")

latest_model = max(pt_files, key=os.path.getmtime)
print(f"Using base model: {latest_model}")

# === Step 5: Train the model ===
model = YOLO(latest_model)
results = model.train(
    data=data_yaml_path,
    epochs=epochs,
    imgsz=imgsz,
    save=True,
    project=model_dir,
    name='temp_training',
    exist_ok=True
)

# === Step 6: Versioned saving of best.pt ===
trained_model_path = os.path.join(model_dir, 'temp_training', 'weights', 'best.pt')

# Extract version number from base model filename
base_filename = os.path.basename(latest_model)

match = re.search(r'(\d+)(?=\.pt$)', base_filename)
if match:
    version_num = int(match.group(1)) + 1
    new_model_name = re.sub(r'\d+(?=\.pt$)', str(version_num).zfill(len(match.group(1))), base_filename)
else:
    name_part = base_filename.rsplit('.', 1)[0]
    new_model_name = f"{name_part}_v1.pt"

final_model_path = os.path.join(model_dir, new_model_name)

# Move best.pt to new versioned name
if os.path.exists(trained_model_path):
    os.replace(trained_model_path, final_model_path)
    print(f"New trained model saved to: {final_model_path}")
else:
    raise FileNotFoundError("Training completed but best.pt was not found.")

# === Step 7: Rename temp_training folder to match final model name ===
result_folder_name = os.path.splitext(new_model_name)[0] + "_results"
result_folder_path = os.path.join(model_dir, result_folder_name)

temp_folder_path = os.path.join(model_dir, 'temp_training')

if os.path.exists(temp_folder_path):
    os.rename(temp_folder_path, result_folder_path)
    print(f"Training results saved to: {result_folder_path}")


import os
import glob
import shutil
import subprocess
import yaml
from ultralytics import YOLO

# === Step 1: Load parameters from params.yaml ===
with open('/path/to/params.yaml', 'r') as file:
    params = yaml.safe_load(file)

plant = params['train']['plant']
pytorch_model_dir = os.path.join('models', plant, 'pytorch')
openvino_base_dir = os.path.join('models', plant, 'openvino')

# === Step 2: Get the latest .pt model ===
pt_files = glob.glob(os.path.join(pytorch_model_dir, '*.pt'))
if not pt_files:
    raise FileNotFoundError(f"No .pt files found in {pytorch_model_dir}")

latest_model = max(pt_files, key=os.path.getmtime)
model_name = os.path.splitext(os.path.basename(latest_model))[0]
print(f"Latest model selected for optimization: {latest_model}")

# === Step 3: Export to ONNX using Ultralytics ===
print("Exporting model to ONNX...")
model = YOLO(latest_model)
onnx_export_path = model.export(format='onnx', dynamic=False, simplify=True)

# === Step 4: Locate ONNX model file ===
if isinstance(onnx_export_path, (tuple, list)):
    latest_onnx = onnx_export_path[0]
else:
    latest_onnx = onnx_export_path

if not os.path.exists(latest_onnx):
    raise FileNotFoundError(f"ONNX export failed: {latest_onnx} not found")

# === Step 5: Convert ONNX to OpenVINO IR using OpenVINO CLI (ovc) ===
conversion_cmd = ['ovc', latest_onnx]
print("Running conversion command:", " ".join(conversion_cmd))
subprocess.run(conversion_cmd, check=True)

# === Step 6: Locate .xml and .bin files in the current working directory ===
cwd = os.getcwd()
converted_xml = os.path.join(cwd, model_name + '.xml')
converted_bin = os.path.join(cwd, model_name + '.bin')

if not (os.path.exists(converted_xml) and os.path.exists(converted_bin)):
    raise FileNotFoundError("Conversion failed: .xml or .bin file not found in working directory")

# === Step 7: Create destination folder and move the converted files ===
final_output_folder = os.path.join(openvino_base_dir, model_name + '_openvino_model')
os.makedirs(final_output_folder, exist_ok=True)

final_xml_path = os.path.join(final_output_folder, model_name + '.xml')
final_bin_path = os.path.join(final_output_folder, model_name + '.bin')

shutil.move(converted_xml, final_xml_path)
shutil.move(converted_bin, final_bin_path)

# === Step 8: Optional - delete ONNX file ===
if os.path.exists(latest_onnx):
    os.remove(latest_onnx)

print("✅ OpenVINO conversion complete!")
print(f"🧠 Model XML saved to: {final_xml_path}")
print(f"📦 Model BIN saved to: {final_bin_path}")


# 🎯 Automated YOLO Training Pipeline with DVC

This project presents a fully **automated, end-to-end pipeline** for training YOLO object detection models using annotated video data. It leverages **DVC (Data Version Control)** to orchestrate tasks from raw video input to model export in both PyTorch and OpenVINO formats.

---

## 📂 Project Structure

```
dvc_project/
│
├── dataset/                            # Data directory
│   └── input_videos/                   # Raw video dataset
│
├── src/                                # Source code
│   ├── Annotation_confirmation/
│   │   └── confirmation.py             # Confirmation stage script
│   ├── cvat_automation_export/
│   │   └── Latest_CVAT_ImportExport.py # CVAT export script
│   ├── cvat_automation_import/
│   │   └── Latest_CVAT_ImportExport.py # CVAT import script
│   ├── openvino_conversion/
│   │   └── openvino_conversion.py      # OpenVINO model conversion
│   ├── splitting_dataset/
│   │   └── splitting_dataset.py        # Data splitting script
│   └── training/                       # Model training
│       └── training.py                 # Model training script
│
├── models/                             # Model outputs
│   └── custom_folder_name_1/
│       ├── openvino/                   # OpenVINO format models
│       └── pytorch/                    # PyTorch format models
│
├── results/                            # Result outputs
│   ├── export_files/                   # Exported files (e.g. from CVAT)
│   ├── frames/                         # Extracted frames from video
│   ├── output_video_mp4/               # Converted videos (not annotated)
│   └── yolo_dataset/                   # YOLO-formatted dataset
│
├── dvc.yaml                            # DVC pipeline file
├── param.yaml                          # All pipeline settings are stored here
└── requirements.txt                    # Python dependencies
```

---

## ⚙️ How It Works

1. **Configure Parameters**  
   All pipeline settings are stored in `params.yaml` – including CVAT login, video paths, job IDs, and training options.

2. **Add Raw Video**  
   Place your video file into `dataset/input_videos/`.

3. **Trigger the Pipeline**  
   DVC will handle the rest:  
   - Video is processed and uploaded to CVAT  
   - After manual annotation, the export script is triggered  
   - YOLO dataset is prepared  
   - Model is trained  
   - The trained model is saved in both PyTorch and OpenVINO formats under `models/`

4. **Fully Automated**  
   Once annotation is done, **no manual steps are required** to train and save the model.

---

## 🚀 Pipeline Stages

| Stage        | Description                                     |
|--------------|-------------------------------------------------|
| `import`     | Upload video frames to CVAT for annotation      |
| `confirmation` | Check annotation status (manual/auto)          |
| `export`     | Export annotations from CVAT in YOLO format     |
| `split`      | Prepare YOLO-compliant training dataset         |
| `train`      | Train YOLOv8 using the specified parameters     |
| `optimization` | Convert trained model to OpenVINO format       |

---

## 📌 Highlights

- 🔄 **Fully Automated Pipeline** using `dvc.yaml`
- 📦 Supports **custom object classes**
- 🧠 Trains **YOLOv8** model on video annotations
- 💡 Converts model to **OpenVINO** for deployment
- 💾 All stages and data are **version controlled with DVC**

---

## 📁 Dependencies

Install all requirements with:

```bash
pip install -r requirements.txt
```

---

## 📘 Prerequisites

- Python 3.8+
- [DVC](https://dvc.org/doc/install)
- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenVINO Toolkit (optional)](https://docs.openvino.ai/)

---

## 🛠 Customization

Modify the `params.yaml` file to:
- Change CVAT project/task settings
- Set training parameters like epochs, image size, class names
- Update export/import paths

---

## 🤝 Contribution & Feedback

Feel free to open issues or contribute improvements!  
This is a dynamic, real-world machine learning pipeline crafted for **reusability**, **scalability**, and **production deployment**.

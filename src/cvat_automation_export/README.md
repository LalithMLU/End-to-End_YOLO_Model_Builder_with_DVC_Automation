# Automated CVAT Pipeline 

## Overview

This repository contains pipeline for automated CVAT pipeline using Python-based CVAT-SDK library.

The pipeline performs the following steps:

1. Reads CVAT username, CVAT password from config file
3. User must enter the project id, task id, job id in config file.
3. User must enter the Entity type: (1=project, 2=task, 3=job) to download images and labels of a particular entity.
4. Base path of folder must be provided in the config file to store images and labels.

## Features

• Uses a configuration file (config.properties) to read required parameters such as project id, task id, job id, export format, and entity type.
• Eliminates the need for manual user input during runtime, making it more automated.
• Focuses only on exporting entities (projects, tasks, jobs). Omits task creation and image file selection functionality.
• Assumes all configuration values are valid, reducing checks for dynamic errors during runtime.
• Reads the directory path (zip path) from the configuration file and creates it automatically before exporting.
• Reads username and password from the configuration file (config.properties) for automatic authentication.
• Uses ExtractVersionMkdirs_Working only for creating directories and invoking version-related tasks during export.




## Configuration file

[CVAT]<br>
host= path of CVAT server with port number
username = Provide your username
password = Provide your password
exp_format = Enter the export format (e.g., 'YOLO 1.1'):
entity_type = (1=project, 2=task, 3=job)
project_id = Enter the Project ID
task_id = Enter the task ID
job_id = Enter the job ID

Provide the path where the CVAT server installed

## Running the Pipeline
1. Clone or Download the repository 
2. Install the required packages using requirements file
3. Setup the configuration path in configuration file 
4. Run the python script
```
python3 main.py
```


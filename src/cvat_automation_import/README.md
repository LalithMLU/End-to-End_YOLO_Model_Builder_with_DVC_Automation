# Automated CVAT Pipeline 

## Overview

This repository contains pipeline for automated CVAT pipeline using Python-based CVAT-SDK library.

The pipeline performs the following steps:

1. Reads CVAT username, CVAT password from the user
2.  Lists all the available projects with their Project ID and Project name
3. User must enter the project id for task creation
4. User must provide the name of the task to be created
5. User must select the image files and upload them 

## Features

- Fetches and lists available projects from the CVAT server.
- Allows user to select image files through a file dialog.
- Creates a new task in a specified project with the selected images.



## Configuration file

[CVAT]<br>
host= path of CVAT server with port number

Provide the path where the CVAT server installed

## Running the Pipeline
1. Clone or Download the repository 
2. Install the required packages using requirements file
3. Setup the configuration path in configuration file 
4. Run the python script
```
python3 main.py
```


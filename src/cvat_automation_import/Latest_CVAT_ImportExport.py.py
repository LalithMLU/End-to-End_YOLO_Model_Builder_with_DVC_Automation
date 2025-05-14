import os
import configparser
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from cvat_sdk import make_client
from cvat_sdk.core.proxies.tasks import ResourceType
from pathlib import Path
import sys
import ffmpeg
import cv2
import shutil
import yaml



# Function to read and parse the parameters from a YAML file
def read_params(file_path):
    with open(file_path, "r") as file:
        params = yaml.safe_load(file)  # Load YAML content
    return params

# Function to read images from a specified folder
def select_files():
    params = read_params('/path/to/params.yaml')
    file_path = params['import']['output_folder_frames']  # Path for the folder containing frames/
    file_paths = []
    for img in os.listdir(file_path):
        file_paths.append(os.path.join(file_path, img))
    return file_paths

# Function to convert video files to .mp4 and extract frames
def conversion():
    # Helper function to convert videos to .mp4 format
    def convert_video(input_file, output_file):
        if input_file.lower().endswith('.mp4'):
            print(f"Input file '{input_file}' is already in .mp4 format. Copying to output folder.")
            if not os.path.exists(output_file):  # Avoid redundant copies
                shutil.copy(input_file, output_file)
            return

        try:
            (
                ffmpeg
                .input(input_file)
                .output(output_file, vcodec='libx264', acodec='aac')  # Specify codecs for conversion
                .run()
            )
            print(f"Conversion successful: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error during conversion: {e.stderr.decode('utf8')}")
            sys.exit(1)

    # Helper function to extract frames from a video
    def extract_frames(video_path, output_folder, skip_frames=1):
        video_capture = cv2.VideoCapture(video_path)

        if not video_capture.isOpened():
            print(f"Error: Could not open video file {video_path}.")
            return

        success, frame = video_capture.read()
        count = 0
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        date_str = datetime.now().strftime('%Y%m%d')

        while success:
            frame_path = os.path.join(output_folder, f"{base_name}_frame_{count}.jpg")
            cv2.imwrite(frame_path, frame)

            # Skip frames if specified
            for _ in range(skip_frames):
                video_capture.grab()

            success, frame = video_capture.read()
            count += 1

        video_capture.release()
        print(f"{count} frames extracted successfully from {video_path} into {output_folder}.")

    # Main function to handle the conversion and frame extraction process
    def main():
        params = read_params('/path/to/params.yaml')

        test_variable = 1

        if test_variable == 0:
            print('The test variable must be 1')
        try:
            params = read_params('/path/to/params.yaml')
            input_folder = params['import']['input_folder']  # Path for input videos
            output_folder_mp4 = params['import']['output_folder_mp4']  # Path for converted videos
            output_folder_frames = params['import']['output_folder_frames']  # Path for extracted frames
            skip_frames = params['import']['skip_frames']  # Frame skipping interval
        except KeyError as e:
            print(f"Error: Missing configuration key {e}. Please check the configuration file.")
            sys.exit(1)

        # Validate input/output paths
        if not os.path.isdir(input_folder):
            print(f"Error: Input folder '{input_folder}' does not exist.")
            sys.exit(1)
        os.makedirs(output_folder_mp4, exist_ok=True)
        os.makedirs(output_folder_frames, exist_ok=True)

        # Process video files in the input folder
        for file_name in os.listdir(input_folder):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder_mp4, os.path.splitext(file_name)[0] + '.mp4')

            convert_video(input_file, output_file)  # Convert or copy the file
            extract_frames(output_file, output_folder_frames, skip_frames)  # Extract frames from the output file

    if __name__ == "__main__":
        main()

# Function to create a new task in CVAT
def create_task(client, project_id, task_name, image_files, tasksize):
    task_spec = {
        "name": task_name,
        "project_id": project_id,
        "segment_size": int(tasksize),
    }
    
    task = client.tasks.create_from_data(
        spec=task_spec,
        resource_type=ResourceType.LOCAL,
        resources=image_files
    )
    task.fetch()
    print(f"\nTask '{task.name}' created with ID: {task.id}")
    print(f"Total number of images in task: {task.size}")

    # Fetch job details for the task
    all_jobs = client.jobs.list()
    jobs = [job for job in all_jobs if job.task_id == task.id]

    for i, job in enumerate(jobs):
        job.fetch()
        print(f"Job: ID {job.id} | Frames {job.start_frame + 1} to {job.stop_frame + 1} | Frame Count: {job.stop_frame - job.start_frame + 1}")
  
    # Check for unexpected frame counts in jobs
    for i, job in enumerate(jobs):
        if (job.stop_frame - job.start_frame + 1) != tasksize:
            print(f"Warning: Job ID {job.id} has an unexpected frame count: {job.stop_frame - job.start_frame + 1}")

# Main function to handle the conversion and task creation process
def main():
    params = read_params('/path/to/params.yaml')
    conversion()  # Convert videos and extract frames
    

    host = params['import']['host']  # CVAT host URL
    tasksize = params['import']['TaskSize']  # Task size in frames

    username = params['import']['username']  # CVAT username
    password = params['import']['password']  # CVAT password

    with make_client(host=host, credentials=(username, password)) as client:
        action = 1  # Set action to create a new task

        if action == 1:
            # List available projects
            projects = client.projects.list()
            for project in projects:
                print(f"ID: {project.id} | Name: {project.name}")
            
            p = params['import']['project_id']  # Project ID
            project_id = int(p)
            t = params['import']['task_name']  # Task name
            task_name = t
            image_files = select_files()  # Get image files from output folder

            create_task(client, project_id, task_name, image_files, tasksize)  # Create a new task
            print(f"The task is created successfully.\nproject ID: {p}\nTask name: {task_name}\nTask size: {tasksize}")
            
if __name__ == "__main__":
    main()

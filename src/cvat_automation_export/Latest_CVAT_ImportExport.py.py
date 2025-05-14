import os
import yaml
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from cvat_sdk import make_client  
from cvat_sdk.core.proxies.tasks import ResourceType 
from pathlib import Path
import yaml

# Importing a custom module for creating directories and performing version-related tasks
import ExtractVersionMkdirs_Working

# Function to read and parse the parameters from a YAML file
def read_params(file_path):
    with open(file_path, "r") as file:
        params = yaml.safe_load(file)  # Load YAML content
    return params

# Function to export a dataset or project from CVAT
def export_entity(client, entity_type, entity_id, export_format, output_file_path):
    entity = None
    
    # Retrieve the entity based on the type
    if entity_type == 'task':
        entity = client.tasks.retrieve(entity_id)  # Fetch a task
    elif entity_type == 'job':
        entity = client.jobs.retrieve(entity_id)  # Fetch a job
    elif entity_type == 'project':
        entity = client.projects.retrieve(entity_id)  # Fetch a project
    
    # Check if the entity exists
    if entity is None:
        print(f"{entity_type.capitalize()} with ID {entity_id} does not exist.")
        return
    
    # If the output path is a directory, create a default file name
    if os.path.isdir(output_file_path):
        output_file_path = os.path.join(output_file_path, f"exported_{entity_type}_{entity_id}.zip")
    
    # Avoid overwriting files by appending a timestamp if a file already exists
    if os.path.exists(output_file_path):
        base, ext = os.path.splitext(output_file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        output_file_path = f"{base}_{timestamp}{ext}"  

    # Export the dataset or project
    entity.export_dataset(
        format_name=export_format,  
        filename=output_file_path,  
        include_images=True 
    )
    print(f"{entity_type.capitalize()} {entity_id} exported successfully to {output_file_path}")

# Main function to control the export process
def main():
    params = read_params('/path/to/params.yaml')
    host = params['export']['host'] # Extract the CVAT host URL from the configuration
    zip_path = Path(params['export']['zip_path']) # Extract the directory path for storing exported zip files
    
    ExtractVersionMkdirs_Working.create_directory_if_not_exists(zip_path)

    username = params['export']['username']
    password = params['export']['password']

    # Use the CVAT SDK to authenticate with the server
    with make_client(host=host, credentials=(username, password)) as client:
        action = "2"
        if action == "2":
            while True:
                entity_type = params['export']['entity_type']
                entity_map = {'1': 'project', '2': 'task', '3': 'job'}
                if entity_type not in entity_map:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    continue
                
                entity_type = entity_map[entity_type]

                if entity_type == 'task' or entity_type == 'job':
                    project_id = int(params['export']['project_id'])
                    if project_id == 0:
                        continue

                    export_format = params['export']['exp_format']  # Format for export
                    output_file_path = zip_path  # Set output directory
                    print("Saved Zip file in path=", zip_path)
                    
                    if entity_type == 'task':
                        task_id = params['export']['task_id'].split(',')
                        for t_id in task_id:
                            export_entity(client, 'task', int(t_id.strip()), export_format, output_file_path)
                    elif entity_type == 'job':
                        job_ids = params['export']['job_id'].split(',')  # Get multiple job IDs
                        for job_id in job_ids:
                            job_id_int = int(job_id.strip())
                            job = client.jobs.retrieve(job_id_int)
                            
                            # Check the state of the job
                            job_state = job.stage  # You can also try `job.status` if `stage` doesn't reflect state
                            print(f"Job ID {job_id_int} state: {job_state}")
                            
                            if job_state.lower() == 'acceptance':
                                export_entity(client, 'job', job_id_int, export_format, output_file_path)
                            else:
                                print(f"Skipping job {job_id_int} because it is not completed (state: {job_state}).")
                else:
                    export_format = params['export']['exp_format']  # Format for export
                    output_file_path = zip_path  # Set output directory
                    print("Saved Zip file in path=", zip_path)
                    entity_id = int(params['project']['project_id'])
                    export_entity(client, entity_type, entity_id, export_format, output_file_path)

                ExtractVersionMkdirs_Working.evm()
                break

if __name__ == "__main__":
    main()


import os
from huggingface_hub import hf_hub_download, list_repo_files

# Specify the model repository and destination folder
model_repo = "Qwen/Qwen2-VL-2B-Instruct"
destination_folder = "./Qwen2-VL-2B-Instruct"

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# List all files in the repository
files = list_repo_files(repo_id=model_repo)

# Download each file to the destination folder
for file in files:
    file_path = hf_hub_download(repo_id=model_repo, filename=file, local_dir=destination_folder)
    print(f"Downloaded {file} to {file_path}")
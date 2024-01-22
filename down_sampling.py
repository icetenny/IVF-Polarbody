import os
import random

def delete_random_images(folder_path, remain_percentage=0.25):
    # Get the list of files in the folder
    files = os.listdir(folder_path)
    
    # Calculate the number of files to be deleted
    num_files_to_delete = int(len(files) * (1 - remain_percentage))
    
    # Randomly select files to be deleted
    files_to_delete = random.sample(files, num_files_to_delete)
    
    # Construct the full file paths
    files_to_delete_paths = [os.path.join(folder_path, file) for file in files_to_delete]
    
    # Delete the selected files
    for file_path in files_to_delete_paths:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Example usage:
folder_path = "data_pic/out/pb_split_pat147_relight_balanced_701020_final/test/1"
delete_random_images(folder_path, remain_percentage=408/602)

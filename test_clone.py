import os
import shutil


def clone_and_rename_images(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    for file_name in files:
        # Check if the file ends with '-f-f.jpg' and not '-f-f-f.jpg'
        if file_name.endswith('-f-f.jpg') and not file_name.endswith('-f-f-f.jpg'):
            # Extract the prefix (e.g., '1-1') and create the new file name
            prefix = file_name[:-8]
            new_file_name = f"{prefix}.jpg"

            # Construct the full paths
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_file_name)

            shutil.copy2(old_path, new_path)

            print(old_path, new_path)

if __name__ == "__main__":
    # Provide the path to the folder containing the images
    folder_path = r'data_pic\out\pb_split_pat147_relight_balanced_701020_final\test2\0'

    # Call the function to clone and rename the images
    clone_and_rename_images(folder_path)

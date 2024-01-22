import os
import cv2
import numpy as np

# Input and output folders
input_folder = 'data_pic/in/Labeled-pat147/train/images'  # Replace with the path to your input folder
output_folder = 'data_pic/out/debright'  # Replace with the path to your output folder

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in the input folder
file_list = os.listdir(input_folder)

# Set the target average brightness
target_avg_brightness = 127.0

# Process each file in the input folder
for file_name in file_list:
    # Construct the full path for the input and output images
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, file_name)

    # Load the grayscale image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Calculate the current average brightness
    current_avg_brightness = np.mean(image)

    # Calculate the adjustment factor
    adjustment_factor = target_avg_brightness / current_avg_brightness

    # Apply the adjustment to the image
    adjusted_image = np.clip(image * adjustment_factor, 0, 255).astype(np.uint8)

    # Save the adjusted image to the output folder
    cv2.imwrite(output_path, adjusted_image)

    print(f"Processed: {file_name}")

print("Processing complete.")

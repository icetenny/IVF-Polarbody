from PIL import Image
import os

# Input and output directories
input_dir = "data_pic/out/pb_split_pat147_relight_balanced_702010_final/test/0"

# Ensure the output directory exists

# List all files in the input directory
files = os.listdir(input_dir)

# Loop through the files and process images
for file in files:
    if file.endswith((".jpg", ".jpeg", ".png", ".gif")):
        # Open the image
        img = Image.open(os.path.join(input_dir, file))

        # Flip the image horizontally
        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

        # Save the flipped image to the output directory
        output_file = os.path.join(input_dir,  f'{file.split(".")[0]}-f.jpg')
        flipped_img.save(output_file)

        print(f"Flipped and saved: {output_file}")

print("All images flipped and saved.")

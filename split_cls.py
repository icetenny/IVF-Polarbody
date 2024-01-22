import os
import shutil
import random

# Define the input directory containing your classes
input_dir = 'data_pic/out/pb_class_pat147_relight_'

# Define the output directories for train, validation, and test data
output_dir = 'data_pic/out/pb_split_pat147_relight_balanced_702010_final'
train_dir = os.path.join(output_dir, 'train')
val_dir = os.path.join(output_dir, 'val')
test_dir = os.path.join(output_dir, 'test')

# Create train, validation, and test directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Set the ratios for training, validation, and testing
train_ratio = 0.7
val_ratio = 0.1
test_ratio = 0.2

# Iterate through the class directories in the input folder
for class_name in os.listdir(input_dir):
    class_dir = os.path.join(input_dir, class_name)
    if os.path.isdir(class_dir):
        # Create class-specific subdirectories in train, validation, and test in the output folder
        train_class_dir = os.path.join(train_dir, class_name)
        val_class_dir = os.path.join(val_dir, class_name)
        test_class_dir = os.path.join(test_dir, class_name)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(val_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)

        # List all images in the class directory
        images = os.listdir(class_dir)

        # Randomly shuffle the list of images
        random.shuffle(images)

        # Calculate the number of images for training, validation, and testing
        num_images = len(images)
        num_train_images = int(train_ratio * num_images)
        num_val_images = int(val_ratio * num_images)

        # Split the images into training, validation, and testing sets
        train_images = images[:num_train_images]
        val_images = images[num_train_images:num_train_images + num_val_images]
        test_images = images[num_train_images + num_val_images:]

        # Copy training images to the train directory in the output folder
        for image in train_images:
            src = os.path.join(class_dir, image)
            dst = os.path.join(train_class_dir, image)
            shutil.copy(src, dst)

        # Copy validation images to the validation directory in the output folder
        for image in val_images:
            src = os.path.join(class_dir, image)
            dst = os.path.join(val_class_dir, image)
            shutil.copy(src, dst)

        # Copy testing images to the test directory in the output folder
        for image in test_images:
            src = os.path.join(class_dir, image)
            dst = os.path.join(test_class_dir, image)
            shutil.copy(src, dst)

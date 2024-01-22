import os
import cv2
import numpy as np
import csv

IMAGE_PATH = "data_pic/in/Labeled-pat147/train/images"
# LABEL_PATH = "data_pic/in/Labeled-pat147/train/labels"
# PB_SIZE = (40, 20)
HAS_FLIPPED = True
DRAW_AND_SHOW = False

csv_file = "data_csv/out/pat147-mod.csv"  # Replace with the path to your CSV file
csv_dict = {}  # Initialize an empty dictionarya

OUTPUT_FOLDER = "data_pic/out/no_crop_pat147"
all_label = [0, 1]

# create folder for all label
for l in all_label:
    os.makedirs(os.path.join(OUTPUT_FOLDER, str(l)), exist_ok=True)

# Read csv and make into a dict
with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        key = row[0]
        values = row[1]
        csv_dict[key] = values

image_files = os.listdir(IMAGE_PATH)

# Process each image file
for image_file in image_files:
    try:

        image_id = image_file.split("_")[0]
        # print(image_id)

        # if image_id != "6-17":continue

        image_path = os.path.join(IMAGE_PATH, image_file)

        label_file = image_file.replace(".jpg", ".txt")
        # label_path = os.path.join(LABEL_PATH, label_file)

        # Read the image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_height, img_width = img.shape

        
        find_label = csv_dict.get(image_id)

        cv2.imwrite(os.path.join(OUTPUT_FOLDER, str(find_label), f"{image_id}.jpg"), img)
        # print(f"Saving {image_id} to folder {str(find_label)}")
        # exit()

        # if DRAW_AND_SHOW:
        #     cv2.imshow("show", img)
        #     cv2.imshow("rotated_show", rotated_image)
        #     cv2.imshow("pb", pb_image)
        #     key = cv2.waitKey()
        #     cv2.destroyWindow("pb")
        #     if key == ord('q'):
        #         break

    except Exception as e:
        print("error", image_file)
        print(e)
        

cv2.destroyAllWindows()

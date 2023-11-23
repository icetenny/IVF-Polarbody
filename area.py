import os
import cv2
import numpy as np
import csv

IMAGE_PATH = "Labeled-45pat/train/images"
LABEL_PATH = "Labeled-45pat/train/labels"
PB_SIZE = (40, 20)
HAS_FLIPPED = True
DRAW_AND_SHOW = False

output_csv_file = "area.csv"
csv_out = open(output_csv_file, mode='w', newline='')
csv_out_writer = csv.writer(csv_out)

header = ["id", "cyto_area", "pb_area", "area_ratio"]
csv_out_writer.writerow(header)

image_files = os.listdir(IMAGE_PATH)

# Process each image file
for image_file in image_files:
    image_id = image_file.split("_")[0]
    out = [image_id,'-','-','-']
    print(image_id)

    # if image_id != "6-17":continue

    image_path = os.path.join(IMAGE_PATH, image_file)

    label_file = image_file.replace(".jpg", ".txt")
    label_path = os.path.join(LABEL_PATH, label_file)

    # Read the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_height, img_width = img.shape

    # Resize
    # img = cv2.resize(img, (img_width // 2 , img_height // 2))
    # img_height, img_width = img.shape

    area_cyto = None
    area_pb = None

    # Read the label file and extract coordinates
    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()
        for line in lines:
            label = line.strip().split()
            index = int(label[0])
            coords = np.array([float(i) for i in label[1:]]
                              ).reshape(((len(label)-1)//2, 2))
            coords = (coords * (img_width, img_height)).astype(int)

            area = 0.5 * np.abs(np.dot(coords[:, 0], np.roll(coords[:, 1], 1)) - np.dot(coords[:, 1], np.roll(coords[:, 0], 1)))

            print(index, area)
            # input()

            if index == 0:
                out[1] = area
            elif index == 1:
                out[2] = area

        if out[1] != "-" and out[2] != "-":
            out[3] = out[2] / out[1]

        csv_out_writer.writerow(out)

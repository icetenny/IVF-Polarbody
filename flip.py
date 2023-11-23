import os
import cv2
import numpy as np
import csv
import shutil


IMAGE_PATH = "Labeled-45pat/train/images"
LABEL_PATH = "Labeled-45pat/train/labels"
# PB_SIZE = (40, 20)

OUTPUT_DIR = "Labeled-45pat-flip"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "labels"), exist_ok=True)

image_files = os.listdir(IMAGE_PATH)

# Process each image file
for image_file in image_files:
    image_id = image_file.split("_")[0]
    print(image_id)

    image_path = os.path.join(IMAGE_PATH, image_file)

    label_file = image_file.replace(".jpg", ".txt")
    label_path = os.path.join(LABEL_PATH, label_file)

    # copy original
    shutil.copy(os.path.join(IMAGE_PATH, image_file), os.path.join(OUTPUT_DIR, "images", image_id + "_.jpg"))
    shutil.copy(os.path.join(LABEL_PATH, label_file), os.path.join(OUTPUT_DIR, "labels", image_id + "_.txt"))
    print("Copying:", image_id)

    # Read the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_height, img_width = img.shape

    flipped_img = cv2.flip(img, 1)

    flipped_anno = []

    # Resize
    # img = cv2.resize(img, (img_width // 2 , img_height // 2))
    # img_height, img_width = img.shape


    # Read the label file and extract coordinates
    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()
        for line in lines:
            label = line.strip().split()
            index = int(label[0])
            coords = np.array([float(i) for i in label[1:]]
                              ).reshape(((len(label)-1)//2, 2))

            flipped_coords = coords.copy()
            flipped_coords[:, 0] = 1 - flipped_coords[:, 0]
            flipped_anno.append([index] + list(flipped_coords.ravel()))

            ori_coords = (coords * (img_width, img_height)).astype(int)
            flipped_coords = (flipped_coords * (img_width, img_height)).astype(int)

            center = np.mean(coords, axis=0).astype(int)

            # for o_coord in ori_coords:
            #     cv2.circle(img, o_coord, 2, (0, 255, 0), -1)
            # for f_coord in flipped_coords:
            #     cv2.circle(flipped_img, f_coord, 2, (0, 255, 0), -1)

            # cv2.circle(img, center, 4, (0, 255, 255), -1)
            # cv2.putText(img, str(index), center, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0,255,255), 2)

    # Write flipped img and anno
    cv2.imwrite(os.path.join(OUTPUT_DIR, "images", image_id + "-f_.jpg"), flipped_img)
    with open(os.path.join(OUTPUT_DIR, "labels", image_id + "-f_.txt"), "w") as w_txt:
        w_txt.write("\n".join([" ".join([str(i) for i in anno]) for anno in flipped_anno]))
        w_txt.close()
    print("Flipping:", image_id)

    # cv2.imshow("show", img)
    # cv2.imshow("flipped show", flipped_img)
    # key = cv2.waitKey()
    # if key == ord('q'):
    #     break

cv2.destroyAllWindows()


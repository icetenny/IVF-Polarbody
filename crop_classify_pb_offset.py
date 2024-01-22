import os
import cv2
import numpy as np
import csv

IMAGE_PATH = "data_pic/out/debright"
LABEL_PATH = "data_pic/in/Labeled-pat147/train/labels"
# PB_SIZE = (40, 20)
HAS_FLIPPED = True
DRAW_AND_SHOW = False

csv_file = "data_csv/out/pat147-mod.csv"  # Replace with the path to your CSV file
csv_dict = {}  # Initialize an empty dictionarya

OUTPUT_FOLDER = "data_pic/out/pb_class_pat147_relight_"
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

        image_path = os.path.join(IMAGE_PATH, image_file)

        label_file = image_file.replace(".jpg", ".txt")
        label_path = os.path.join(LABEL_PATH, label_file)

        # Read the image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_height, img_width = img.shape

        center_cyto, center_pb = None, None
        coords_cyto, coords_pb = None, None

        # Read the label file and extract coordinates
        with open(label_path, 'r') as label_file:
            lines = label_file.readlines()
            for line in lines:
                label = line.strip().split()
                index = int(label[0])
                coords = np.array([float(i) for i in label[1:]]
                                ).reshape(((len(label)-1)//2, 2))
                coords = (coords * (img_width, img_height)).astype(int)

                center = np.mean(coords, axis=0).astype(int)

                if index == 0:
                    center_cyto = center
                    coords_cyto = coords
                elif index == 1:
                    center_pb = center
                    coords_pb = coords

                if DRAW_AND_SHOW:
                    for coord in coords:
                        cv2.circle(img, coord, 2, (0, 255, 0), -1)
                    cv2.circle(img, center, 4, (0, 255, 255), -1)
                    cv2.putText(img, str(index), center, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0,255,255), 2)

            # Rotate if cyto and pb are presented
            if center_cyto is not None and center_pb is not None:
                final_angle = -90
                angle = np.arctan2(
                    center_pb[1] - center_cyto[1], center_pb[0] - center_cyto[0])
                angle_degrees = np.degrees(angle)
                apply_angle = angle_degrees - final_angle

                rotation_matrix = cv2.getRotationMatrix2D(
                    (img_width//2, img_height//2), apply_angle, 1)
                rotated_image = cv2.warpAffine(
                    img, rotation_matrix, (img_width, img_height))

                rotated_coords_pb = np.array([cv2.transform(np.array(
                    [[c]], dtype=np.float32), rotation_matrix)[0][0] for c in coords_pb]).astype(int)
                

                x1, y1 = np.min(rotated_coords_pb, axis=0)
                x2, y2 = np.max(rotated_coords_pb, axis=0)

                offset = 10

                x_d = x2-x1+offset*2
                y_d = y2-y1+offset*2

                x_mid = (x1+x2)//2
                y_mid = (y1+y2)//2

                sq_d = max(x_d, y_d) // 2


                # pb_image = rotated_image[y1:y2+1, x1:x2+1].copy()
                pb_image = rotated_image[y_mid-sq_d: y_mid+sq_d+1, x_mid-sq_d: x_mid+sq_d+1].copy()

                pb_image = cv2.resize(pb_image, (128,128))


                if HAS_FLIPPED:
                    find_label = csv_dict.get(image_id.rstrip("-f"))
                else:
                    find_label = csv_dict.get(image_id)

                if not find_label:
                    print("No label found:", image_id)
                    continue

                cv2.imwrite(os.path.join(OUTPUT_FOLDER, str(find_label), f"{image_id}.jpg"), pb_image)
                # print(f"Saving {image_id} to folder {str(find_label)}")
                # exit()

                if DRAW_AND_SHOW:
                    cv2.rectangle(rotated_image, (x1, y1), (x2, y2), (255, 255, 255))
                    for coord in rotated_coords_pb:
                        cv2.circle(rotated_image, coord, 2, (0, 0, 255), -1)

                # print(csv_dict)
            else:
                print("No PB Found: ", image_id)
                continue

        if DRAW_AND_SHOW:
            cv2.imshow("show", img)
            cv2.imshow("rotated_show", rotated_image)
            cv2.imshow("pb", pb_image)
            key = cv2.waitKey()
            cv2.destroyWindow("pb")
            if key == ord('q'):
                break

    except Exception as e:
        print("error", image_file)
        print(e)
        

cv2.destroyAllWindows()

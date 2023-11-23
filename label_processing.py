import os
import cv2
import numpy as np
import csv

IMAGE_PATH = "Labeled-45pat-flip/images"
LABEL_PATH = "Labeled-45pat-flip/labels"
PB_SIZE = (40, 20)
HAS_FLIPPED = True
DRAW_AND_SHOW = False

csv_file = "pat45-mod2.csv"  # Replace with the path to your CSV file
csv_dict = {}  # Initialize an empty dictionarya

output_csv_file = "pat45_out_flip.csv"
csv_out = open(output_csv_file, mode='w', newline='')
csv_out_writer = csv.writer(csv_out)

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
    image_id = image_file.split("_")[0]
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

            pb_image = rotated_image[y1:y2+1, x1:x2+1].copy()

            # print(pb_image.shape)
            pb_original_ratio = pb_image.shape[1] / pb_image.shape[0]
            pb_image = cv2.resize(pb_image, PB_SIZE)
            # print(pb_original_ratio)

            pb_out = np.reshape(pb_image/255, -1)
            # print(pb_out.shape)
            # print(pb_out)

            if HAS_FLIPPED:
                find_label = csv_dict.get(image_id.rstrip("-f"))
            else:
                find_label = csv_dict.get(image_id)

            if not find_label:
                print("No label found:", image_id)
                continue

            out_row = [image_id, find_label, str(
                round(pb_original_ratio, 5))] + [str(round(i, 5)) for i in pb_out]

            csv_out_writer.writerow(out_row)

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

cv2.destroyAllWindows()

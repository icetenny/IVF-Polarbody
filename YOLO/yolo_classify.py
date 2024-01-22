from ultralytics import YOLO
import cv2
import os
import csv

# Specify the file path
csv_file_path = "YOLO/final/m-output-final-with-duplicate.csv"

save_dup = True

# Write to the CSV file
file = open(csv_file_path, mode='w', newline='')
writer = csv.writer(file)
if save_dup:
    writer.writerows([["patient_id", "oocyte_no", "duplicate_id", "target", "predict"]])
else:
    writer.writerows([["patient_id", "oocyte_no", "target", "predict"]])

PRED_FOLDER = "data_pic/out/pb_split_pat147_relight_balanced_701020_final/test2"
TARGET = [0,1]

# pic = cv2.imread("data_pic/out/pb_split_pat147_relight_balanced/test/0/3-6-f.jpg")
model = YOLO(r"YOLO\final\weights\m-final.pt")

for tar in TARGET:
    class_folder = os.path.join(PRED_FOLDER, str(tar))
    res = [0,0]

    for pic in os.listdir(class_folder):
        # print(pic)
        result = model.predict(source=os.path.join(class_folder, pic), verbose=False)[0]
        # print(result.probs.top1)
        res[int(result.probs.top1)] += 1

        if not save_dup:
            if "f" in pic:
                pass
            else:
                pat_id, no_image = pic.split(".")[0].split("-")[:2]
                writer.writerows([[pat_id, no_image,  tar, int(result.probs.top1)]])

        else:
            # Save with dup
            duplicate_id = pic.count("f")
            pat_id, no_image = pic.split(".")[0].split("-")[:2]
            writer.writerows([[pat_id, no_image, duplicate_id,  tar, int(result.probs.top1)]])

    print(res)
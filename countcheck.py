import os
LABEL_PATH = "Polar Body.v4i.yolov8\\train\\labels"
count = [0,0]
for file in os.listdir(LABEL_PATH):
    with open(os.path.join(LABEL_PATH, file), "r") as f:
        l = [i.split()[0] for i in f.readlines()]
        for j in l:
            count[int(j)] += 1
        if l == ["0", "0"]:
            print(file)
print(count)
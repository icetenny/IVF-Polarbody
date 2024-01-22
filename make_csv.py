import os
import csv

def extract_id_and_no(image_name):
    id, no = image_name.split('-')
    return int(id), int(no.split('.')[0])

def process_folder(folder_name, folder_index):
    csv_data = []

    for filename in os.listdir(folder_name):
        if filename.endswith(".jpg"):
            id, no = extract_id_and_no(filename)
            csv_data.append({'id': id, 'no': no, 'folder_name': folder_index})

    return csv_data

def merge_scores(csv_data, scores_data):
    for row in csv_data:
        key = (row['id'], row['no'])
        if key in scores_data:
            row['score'] = scores_data[key]
        else:
            row['score'] = None

def create_csv(sorted_data, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'no', 'folder_name', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in sorted_data:
            writer.writerow(row)

def main():
    folder_0_data = process_folder(r'data_pic\out\pb_class_pat147_relight_\0', 0)
    folder_1_data = process_folder(r'data_pic\out\pb_class_pat147_relight_\1', 1)

    all_data = folder_0_data + folder_1_data
    sorted_data = sorted(all_data, key=lambda x: (x['id'], x['no']))

    scores_data = {}

    with open(r'data_csv\out\pat147-mod-with-pbtype.csv', 'r') as scores_file:
        scores_reader = csv.reader(scores_file)
        for row in scores_reader:
            id, no, score = int(row[0]), int(row[1]), row[3]
            scores_data[(id, no)] = score

    merge_scores(sorted_data, scores_data)

    create_csv(sorted_data, 'output_that.csv')

if __name__ == "__main__":
    main()

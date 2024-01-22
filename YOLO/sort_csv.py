import csv

# Specify the input and output file paths
input_csv_file_path = r"YOLO\final\l-output-final.csv"
output_csv_file_path = r"YOLO\final\l-sorted-output-final.csv"

# Read the CSV file into a list of dictionaries
with open(input_csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Sort the data based on the first two columns ("Name" and "Age")
sorted_data = sorted(data, key=lambda x: (int(x['patient_id']), int(x['oocyte_no'])))

# Write the sorted data to a new CSV file
with open(output_csv_file_path, mode='w', newline='') as file:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the sorted data
    writer.writerows(sorted_data)


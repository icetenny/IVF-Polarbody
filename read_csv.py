import csv

csv_file = "pat45-mod2.csv"  # Replace with the path to your CSV file

csv_dict = {}  # Initialize an empty dictionary

with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Skip the header row if it exists
    next(csv_reader, None)

    for row in csv_reader:
        # Assuming the first column is the key, and the rest are values
        key = row[0]
        values = row[1:]
        
        # Create a dictionary entry with the key and values
        csv_dict[key] = values

# Print the resulting dictionary
print(csv_dict)
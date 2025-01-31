import csv
import os

# Get input file path from user
input_file = input("Enter the path to the input file: ")
print(f"Opening file: {input_file}")  # Debugging line

# Check if the file exists
if not os.path.isfile(input_file):
    print("Error: File not found. Please check the path and try again.")
    exit(1)

# Extract the file name without the extension for column A
file_name = os.path.basename(input_file).split('.')[0]

# Set output file name same as input file, with .csv extension
output_file = os.path.splitext(input_file)[0] + ".csv"

data = []
with open(input_file, "r") as file:
    for line in file:
        line = line.strip()
        print(f"Processing line: {line}")  # Debugging output

        # Extract part of the line after "HPE"
        if "HPE" in line:
            extracted_part = line.split("HPE", 1)[-1].strip()  # Extract after 'HPE'

            # Extract the part between the second and second last underscore
            parts = line.split("_")
            if len(parts) >= 4:
                middle_part = "_".join(parts[2:-1])  # Join parts from second underscore to second-last underscore
            else:
                middle_part = ""  # If there aren't enough underscores, return an empty string

            data.append([file_name, middle_part])  # Store file name and extracted part

# Write to the dynamically named CSV file with a semicolon delimiter
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)  # Use semicolon for European formats
    writer.writerow(["File Name", "Extracted"])  # Header row
    writer.writerows(data)

print(f"CSV file '{output_file}' has been created successfully.")
import os
import csv

def process_file(input_file):
    # Check if the file exists
    if not os.path.isfile(input_file):
        print("Error: File not found. Please check the path and try again.")
        return []

    # Get the directory of the input file and its base name without extension
    directory = os.path.dirname(input_file)
    file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]

    # Set the output CSV file path in the same folder with the same name but .csv extension
    output_file = os.path.join(directory, file_name_without_extension + "_output.csv")

    # Read the input file and process lines
    data = []
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            print(f"Processing line: {line}")  # Debugging output
            if "HPE" in line:
                # Extract part after 'HPE'
                extracted_part = line.split("HPE", 1)[-1].strip()
                # Extract the part after the second underscore and before the third underscore in the extracted part for column B
                parts = extracted_part.split("_")
                if len(parts) >= 3:
                    # Extract part from the second underscore to the third underscore
                    middle_part = "_".join(parts[2:4])  # Getting the third part (index 2) and fourth part (index 3)
                    data.append([file_name_without_extension, middle_part])  # Store filename without extension and extracted part

    # Write to a CSV file with a semicolon delimiter
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)  # Use semicolon for European formats
        writer.writerow(["Filename", "Extracted"])  # Header row
        writer.writerows(data)

    print(f"CSV file '{output_file}' has been created successfully.")
    return data

def main():
    # Get input file path from user
    input_file = input("Enter the path to the input file: ")
    print(f"Opening file: {input_file}")  # Debugging line

    # Process the file and output results
    process_file(input_file)

if __name__ == "__main__":
    main()

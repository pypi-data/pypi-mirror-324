import csv
import os

# Get folder path from the user
folder_path = input("Enter the path to the folder containing .txt files: ").strip()

# Check if the folder exists
if not os.path.isdir(folder_path):
    print("Error: Folder not found. Please check the path and try again.")
    exit(1)

# Process all .txt files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        input_file = os.path.join(folder_path, filename)
        output_file = os.path.join(folder_path, os.path.splitext(filename)[0] + ".csv")

        print(f"Processing file: {input_file}")

        # Read the input file and process lines
        data = []
        unique_values = set()  # To store unique values for Column B

        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                print(f"Processing line: {line}")  # Debugging output

                if "HPE" in line:
                    extracted_part = line.split("HPE", 1)[-1].strip()

                    # Extract everything after the second "_" but before the last "_"
                    parts = extracted_part.split("_")
                    if len(parts) > 2:
                        extracted_part = "_".join(parts[2:-1])  # Extract from third part to second-last part

                    # Skip duplicate values for Column B
                    if extracted_part not in unique_values:
                        unique_values.add(extracted_part)
                        data.append([os.path.splitext(filename)[0],
                                     extracted_part])  # Store filename without .txt and extracted part

        # Write to a CSV file with a semicolon delimiter
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Filename", "Extracted"])  # Header row
            writer.writerows(data)

        print(f"CSV file '{output_file}' has been created successfully.")

print("Processing complete for all .txt files.")

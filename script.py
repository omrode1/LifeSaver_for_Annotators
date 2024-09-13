import os

# Define the directory containing your label files
folder_path = './Annotation_automation/data 18k (copy)'

# Indices you want to keep and their new mappings
# Update the indices if necessary based on your classes.txt file
keep_classes = {
    1: 0,  # Hardhat -> 0
    2: 1   # No_hardhat -> 1
}

# Function to process each label file
def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # List to hold updated lines
    updated_lines = []

    for line in lines:
        # Split the line by spaces to get the class index and bounding box values
        parts = line.strip().split()

        # Check if parts have sufficient data
        if len(parts) < 5:
            print(f"Skipping malformed line in {file_path}: {line}")
            continue

        # Get the class index (the first element)
        class_index = int(parts[0])

        # Print the class index for debugging
        print(f"Found class index {class_index} in {file_path}")

        # Check if the class index is one of the ones we want to keep
        if class_index in keep_classes:
            # Update the class index and keep the rest of the bounding box values
            parts[0] = str(keep_classes[class_index])
            updated_lines.append(' '.join(parts))

    # If there are updated lines, write them back to the file (overwriting it)
    if updated_lines:
        with open(file_path, 'w') as file:
            file.write('\n'.join(updated_lines) + '\n')
    else:
        print(f"No valid labels found for {file_path}. File was not updated.")

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        process_file(file_path)

print("Processing complete!")

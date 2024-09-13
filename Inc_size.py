import os

# Directory containing your label files
labels_folder = 'path to your dataset'

# Define the percentage to increase the bounding box size (e.g., 10%)
increase_percent = -10 / 100  # Convert percentage to a fraction/ you can use negative value for decresing

# Function to adjust the bounding box size
def adjust_bbox_size(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        parts = line.strip().split()

        if len(parts) < 5:
            print(f"Skipping malformed line in {file_path}: {line}")
            continue

        # Extract the class, x_center, y_center, width, and height
        class_index = parts[0]
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        # Increase width and height by the defined percentage
        new_width = width * (1 + increase_percent)
        new_height = height * (1 + increase_percent)

        # Ensure the bounding box stays within the image (x_center, y_center are normalized [0,1])
        if new_width > 1:
            new_width = 1
        if new_height > 1:
            new_height = 1

        # Make sure the new bounding box doesn't exceed the image frame
        # Adjust the new width and height so that they fit within [0,1] boundaries
        if x_center - new_width / 2 < 0:
            new_width = x_center * 2
        if x_center + new_width / 2 > 1:
            new_width = (1 - x_center) * 2

        if y_center - new_height / 2 < 0:
            new_height = y_center * 2
        if y_center + new_height / 2 > 1:
            new_height = (1 - y_center) * 2

        # Store the updated bounding box values
        updated_lines.append(f"{class_index} {x_center:.6f} {y_center:.6f} {new_width:.6f} {new_height:.6f}")

    # Write the updated lines back to the file
    if updated_lines:
        with open(file_path, 'w') as file:
            file.write('\n'.join(updated_lines) + '\n')
    else:
        print(f"No valid labels found for {file_path}. File was not updated.")

# Iterate through all label files and adjust bounding box size
for filename in os.listdir(labels_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(labels_folder, filename)
        adjust_bbox_size(file_path)

print("Bounding box adjustment complete!")

# Path to the input file
input_file_path = "correct.txt"  # Replace with your actual file path
output_file_path = "../../utils/main_skin.csv"  # Output file path

# Read the lines from the file
try:
    with open(input_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# Process each line to add quotes around the first value
updated_lines = []

for line in lines:
    # Split the line by the first comma
    parts = line.split(",", 1)

    # Add double quotes around the first value if it isn't already quoted
    if not parts[0].startswith('"') and not parts[0].endswith('"'):
        parts[0] = f'"{parts[0]}"'

    # Join the updated first part with the rest of the line and add it to the updated lines list
    updated_line = ",".join(parts)
    updated_lines.append(updated_line)

# Write the updated lines to a new file
try:
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for line in updated_lines:
            output_file.write(line)
    print(f"File updated successfully! The new file is saved as {output_file_path}")
except Exception as e:
    print(f"Error writing to file: {e}")

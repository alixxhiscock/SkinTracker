import re

# Function to add quotes around the skin names
def add_quotes(text):
    return re.sub(r"^(\S+)", r'"\1"', text)

# File paths (change these as needed)
input_file_path = 'backup - Copy.csv'  # The file you're reading from
output_file_path = 'maybegood.txt'  # The file you're writing to

# Open the input file, read lines, and process each line
with open(input_file_path, 'r') as infile:
    lines = infile.readlines()

# Apply the add_quotes function to each line
processed_lines = [add_quotes(line.strip()) for line in lines]

# Write the processed lines to a new file
with open(output_file_path, 'w') as outfile:
    outfile.write("\n".join(processed_lines))

print(f"Processed data saved to {output_file_path}")

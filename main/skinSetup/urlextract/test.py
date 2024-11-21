import re

# File paths
data_file_path = "maybegood.txt"  # File containing data without URLs
urls_file_path = "filtered_wikia_urls.txt"  # File containing raw URLs
output_file_path = "correct.txt"  # Output file

# Regex to match valid skin URLs (no "_skin" in the URL part)
valid_url_pattern = r"https://static\.wikia\.nocookie\.net/hypixel-skyblock/images/\w+/\w+/.*?_Skin\.png/revision/latest\?cb=\d+"

# Load data and URLs
with open(data_file_path, "r", encoding="utf-8") as data_file:
    data_lines = data_file.readlines()

with open(urls_file_path, "r", encoding="utf-8") as urls_file:
    raw_urls = urls_file.read()

# Extract valid URLs
valid_urls = re.findall(valid_url_pattern, raw_urls)

# Create a dictionary to map item names to URLs (strip the '_Skin' suffix)
url_map = {}
for url in valid_urls:
    # Extract the item name from the URL (e.g., "Loafed_Black_Cat_Skin")
    match = re.search(r"/([\w_]+)_Skin\.png", url)
    if match:
        item_name = match.group(1)  # Keep the underscores intact, remove only '_Skin'
        url_map[item_name] = url

# Debug: Check the URL map
print(f"URL Map: {url_map.keys()}")  # Debugging: Print keys of the URL map to see what we have

# Append URLs to the data lines
output_lines = []
for line in data_lines:
    # Ensure the first word is enclosed in quotes
    line = re.sub(r"^([\w_]+),", r'"\1",', line)  # Add quotes around the first word

    # Extract the item name from the data line (before the first comma)
    match = re.match(r'"([\w_]+)",', line)
    if match:
        item_name = match.group(1).replace('_skin', '').title() # Remove '_skin' suffix from the item name
        print(f"Processing item: {item_name}")  # Debugging the item name
        # Add the corresponding URL if available
        if item_name in url_map:
            line = line.strip() + f',"{url_map[item_name]}"\n'
        else:
            print(f"Warning: No URL found for {item_name}")  # Debugging missing URLs
    output_lines.append(line)

# Write the output to a file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.writelines(output_lines)

print(f"Processed {len(data_lines)} rows. Output saved to {output_file_path}.")

import re
#FINDS CORRECT URLS IN FILE OF URLS
# Load your page source from a file
with open("extracted.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Regex pattern for skin URLs
skin_pattern = r"https://static\.wikia\.nocookie\.net/hypixel-skyblock/images/\w+/\w+/.*?_Skin\.png/revision/latest\?cb=\d+"

# Extract all matching URLs
skin_urls = re.findall(skin_pattern, content)

# Save results to a file
with open("confirmed_skin_urls.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(skin_urls))

print(f"Extracted {len(skin_urls)} skin URLs. Saved to 'confirmed_skin_urls.txt'.")

import os
import csv
import requests
from django.conf import settings
from main.models import Skin
import django

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkinTracker.settings')
django.setup()

# Directory to save images
IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, "skins")
os.makedirs(IMAGE_DIR, exist_ok=True)  # Ensure the directory exists

# Path to your CSV file
CSV_FILE_PATH = os.path.join("C:\\dev\\SkinTracker\\main\\utils\\non_fire_sale_skins.csv")


def download_and_save_image(skin_name, image_url):
    """
    Downloads an image from a URL and saves it to the IMAGE_DIR.
    Updates the Skin model's image_url field.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Save the image using the skin's name
        filename = f"{skin_name}.png"
        filepath = os.path.join(IMAGE_DIR, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        # Update the Skin model's image_url field
        skin = Skin.objects.get(name=skin_name)
        skin.image_url = f"/media/skins/{filename}"  # Adjust based on your MEDIA_URL
        skin.save()

        print(f"Downloaded and updated image for: {skin_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image for {skin_name}: {e}")
    except Skin.DoesNotExist:
        print(f"Skin with name {skin_name} does not exist in the database.")


def process_csv_and_update_images(csv_file_path):
    """
    Reads a CSV file, extracts the skin name and image_url,
    and updates the images for skins.
    """
    with open(csv_file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row or len(row) < 5:  # Skip empty rows or rows with insufficient columns
                continue

            skin_name = row[0].strip()  # Assuming the skin's name is in the first column
            image_url = row[5].strip()  # Assuming the image URL is in the 5th column
            download_and_save_image(skin_name, image_url)


# Execute the process
process_csv_and_update_images(CSV_FILE_PATH)

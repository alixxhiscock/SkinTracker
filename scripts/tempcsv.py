import os
import csv
from datetime import datetime
from main.models import Skin, Item
import django

# Set the environment variable to point to the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkinTracker.settings')
# Initialize Django
django.setup()

def add_skins_from_csv(csv_file_path):
    skins_to_add = []
    items_to_add = []
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            # Extract fields from each row
            skin_name = row[0].strip('"')
            item_name = row[4].strip('"')
            try:
                skin = Skin.objects.get(name=skin_name)
            except Skin.DoesNotExist:
                print(f"Skin with name {skin_name} does not exist.")
                continue
            item, item_created = Item.objects.update_or_create(
                skin=skin,
                defaults={'item': item_name}
            )

            if item_created:
                items_to_add.append(item)

    if items_to_add:
        Item.objects.bulk_create(items_to_add)
        print(f"Added {len(items_to_add)} items to the database.")

# Path to your CSV file
csv_file_path = r'C:\dev\SkinTracker\main\utils\main_skin.csv'
add_skins_from_csv(csv_file_path)
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
            skin_id = row[0]
            skin_name = row[1].strip('"')
            try:
                release_date = datetime.strptime(row[2].strip('"'), '%Y-%m-%d').date()
            except ValueError:
                print(f"Skipping row with invalid release date: {row[2]}")
                continue  # Skip the row if the date format is invalid

            try:
                lbin = int(row[3]) if row[3] else 0  # Default to 0 if empty
            except ValueError:
                print(f"Invalid lbin value for : {row[3]}")
                lbin = 0  # Default to 0 on error

            try:
                quantity = int(row[4]) if row[4] else 0
            except ValueError:
                print(f"Invalid quantity for : {row[4]}")
                quantity = 0  # Default to 0 on error

            try:
                price = int(row[5]) if row[5] else 0  # Default to 0 if empty
            except ValueError:
                print(f"Invalid price for : {row[4]}")
                price = 0  # Default to 0 on error

            image_url = row[6].strip('"')
            #item_name = row[7].strip('"')

            # Prepare skin data for bulk insert
            skin, created = Skin.objects.update_or_create(
                name=skin_name,
                defaults={
                    'release_date': release_date,
                    'quantity': quantity,
                    'price': price,
                    'image_url': image_url,
                    'lbin': lbin,
                }
            )
            #item, item_created = Item.objects.update_or_create(
                #skin=skin,
                #item=item_name,
                #defaults={'skin': skin, 'item': item}
            #)

            #if created:
                #skins_to_add.append(skin)

            #if item_created:
                #items_to_add.append(item)

    if skins_to_add:
        Skin.objects.bulk_create(skins_to_add)
        print(f"Added {len(skins_to_add)} skins to the database.")

    #if items_to_add:
        #Item.objects.bulk_create(items_to_add)
        #print(f"Added {len(items_to_add)} items to the database.")


# Path to your CSV file
csv_file_path = r'C:\dev\SkinTracker\main\utils\main_skin.csv'
add_skins_from_csv(csv_file_path)
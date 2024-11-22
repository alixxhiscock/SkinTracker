import csv
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings
import os

# Setup Django environment if running as a standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SkinTracker.settings")
import django
django.setup()

from main.models import Auction, User, Skin

# Path to your CSV file
CSV_FILE_PATH = "path/to/your/file.csv"

def import_csv():
    try:
        with open(CSV_FILE_PATH, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    id = User.objects.get(username=row["id"])
                    seller = User.objects.get(username=row["seller"])
                    buyer = User.objects.get(username=row["buyer"])
                    item = Skin.objects.get(name=row["item"])
                    timestamp = make_aware(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))

                    # Create an Auction instance
                    auction = Auction(
                        id=uuid.uuid4(),  # Generate a UUID
                        seller=seller,
                        buyer=buyer,
                        price=int(row["price"]),
                        item=item,
                        timestamp=timestamp
                    )
                    auction.save()
                    print(f"Auction {auction.id} imported successfully.")
                except Exception as e:
                    print(f"Error importing row {row}: {e}")

    except FileNotFoundError:
        print("CSV file not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import_csv()

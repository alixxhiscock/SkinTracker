from main.models import User, Skin, Coin, Sale, SaleItem
from django.contrib.contenttypes.models import ContentType
import csv, os, re

def add_from_csv(csv_path):
    with open(csv_path,'r') as file:
        reader=csv.reader(file)
        for row in reader:
            if not row:
                continue
            buyer, _ = User.objects.get_or_create(username=row[0].strip('"'))
            seller, _ = User.objects.get_or_create(username=row[2].strip('"'))
            #Checks if coins format for csv
            try:
                items = row[1].split("/")
                for item in items:
                    if is_coins(item):
                        print(f"Would make buyer_item a coin object")
                    elif Skin.objects.filter(name=item) is not None:
                        print(f"Would set buyer_item to an existing skin object :" )
                items = row[3].split("/")
                for item in items:
                    if is_coins(item):
                        print(f"Would make seller_item a coin object for {parse_value(item)}")
                    elif Skin.objects.filter(name=item) is not None:
                        print("Would set seller_item to an existing skin object")
            except Exception as e:
                print(e)
                continue
            #sale = Sale.objects.create(buyer="buyer",seller="seller")
            #add_sale_item(sale,buyer_item,buyer,buyer_item.id,1)
            #add_sale_item(sale, seller_item, buyer, buyer_item.id, 1)



def is_coins(str):
    return bool(re.match(r'^\d+(\.\d+)?[mb]$', str, re.IGNORECASE))

def parse_value(value):
    multipliers = {'m': 1_000_000, 'b': 1_000_000_000}
    return int(float(value[:-1]) * multipliers.get(value[-1].lower(), 1))

def formatCoins(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}b"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.0f}m"
    else:
        return str(value)

def add_sale_item(sale, item, owner, object_id, quantity):
    content_type = ContentType.objects.get_for_model(item)
    sale_item, _ = SaleItem.objects.create(sale=sale, owner=owner, content_type=content_type, object_id=object_id, quantity=quantity)
    sale_item.save()
    return sale_item

def test_csv(csv_path):
    with open(csv_path,'r') as file:
        reader=csv.reader(file)
        for row in reader:
            if not row:
                continue
            print(row[1].split("/"))

add_from_csv(r'C:\dev\SkinTracker\main\utils\add_sale.csv')
#("Dominik313","lunar_rat"/"3b"/","MrInko","6.2b coins","2024-05-11")


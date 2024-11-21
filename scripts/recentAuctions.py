import json
import requests
from datetime import datetime
from main.models import Auction, Skin, User, Sale
from django.utils import timezone

def getAuctionsJSON(skin):
    url = f"https://sky.coflnet.com/api/auctions/tag/{skin.name}/sold"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for sale in data:
            if Auction.objects.filter(id=sale["uuid"]).exists():
                print(f'ID: {sale["uuid"]} already in database')
                continue
            else:
                seller, _ = User.objects.get_or_create(username=getUsername(sale["auctioneerId"]))
                price = sale["highestBidAmount"]
                item_name = skin.name
                auction_id = sale["uuid"]
                timestamp = sale["end"]
                timestamp = timezone.make_aware(datetime.fromisoformat(timestamp))
                buyer, _ = User.objects.get_or_create(username=getBidder(auction_id))
                auction_item = Auction.objects.create(
                    seller=seller,
                    item_name=skin,
                    price=price,
                    id=auction_id,
                    timestamp=timestamp,
                    buyer=buyer
                )
                print(f"Added ID:{auction_id} {seller} to {buyer} for {price}")


def getBidder(auction_id):
    url = f"https://sky.coflnet.com/api/auction/{auction_id}"
    response = requests.get(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return getUsername(response.json()["bids"][0]["bidder"])
        else:
            print(f"Error fetching username: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error in request to fetch username: {e}")
        return None

def getUsername(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Retrieved data for UUID {uuid}: {response.json()}")  # Debugging output
        return response.json()["name"]
    else:
        print(f"Error fetching username for UUID {uuid}: {response.status_code}")

getAuctionsJSON(Skin.objects.get(name="monochrome_elephant"))
#getBidder("b118f3e66e204021b573e9807276d614")

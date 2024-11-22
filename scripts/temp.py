from main.models import User, Auction, Skin
from datetime import datetime
from django.utils.timezone import make_aware

seller = User.objects.get(username="DNRCheeky")
price = 4800000000
item_name = Skin.objects.get(name="lunar_rat")
auction_id = "01a79d423b3641abb86111e2eab86ce1"
timestamp = make_aware(datetime.now())
buyer = User.objects.get(username="DNRSneaky")
auction_item = Auction.objects.create(
        seller=seller,
        item_name=item_name,
        price=price,
        id=auction_id,
        timestamp=timestamp,
        buyer=buyer)
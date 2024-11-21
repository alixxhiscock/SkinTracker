from django.contrib import admin
from .models import Skin, OwnedSkin, User, Item, Sale, Coin, SaleItem, Auction

admin.site.register(Skin)
admin.site.register(OwnedSkin)
admin.site.register(User)
admin.site.register(Sale)
admin.site.register(Item)
admin.site.register(Coin)
admin.site.register(SaleItem)
admin.site.register(Auction)


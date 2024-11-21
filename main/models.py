from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from main.templatetags.filters import formatCoins

class Skin(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    lbin = models.IntegerField(verbose_name="Lowest BIN",default=0)
    quantity = models.IntegerField(verbose_name="Quantity",default=0)
    price = models.IntegerField(verbose_name="Price in gems",default=0)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    def readable(self):
        return self.name.replace("_"," ").title()

    @property
    def is_local_image(self):
        return self.image_url.startswith('/media/skins/')

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    favorite_skins = models.ManyToManyField(Skin, related_name="favorited_by", blank=True)

    def __str__(self):
        return self.username

class OwnedSkin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    applied = models.BooleanField(default=False)
    pricepaid = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'skin', 'applied')  # Composite unique constraint
        verbose_name = "Owned Skin"
        verbose_name_plural = "Owned Skins"

    def __str__(self):
        return f"{self.user.username} owns {self.quantity} of {self.skin.name}"

class Item(models.Model):
    skin = models.OneToOneField(Skin, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    def __str__(self):
        return self.item

class Coin(models.Model):
    amount = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{formatCoins(self.amount)} coins"

class Sale(models.Model):
    sale_id=models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    timestamp = models.DateTimeField(auto_now_add=True)
    screenshot = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Trade between {self.buyer.username} and {self.seller.username}"

    @property
    def buyer_items(self):
        return self.items.filter(owner=self.buyer)

    @property
    def seller_items(self):
        return self.items.filter(owner=self.seller)

class SaleItem(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='items')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Type of the item
    object_id = models.PositiveIntegerField()  # ID of the item
    item = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the item (if applicable)
    applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.item} (Owner: {self.owner.username})"

class Auction(models.Model):
    id=models.UUIDField(primary_key=True, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_seller")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_buyer")
    price = models.PositiveIntegerField()
    item_name = models.ForeignKey(Skin, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.seller} sold {self.item_name} for {self.price} coins"

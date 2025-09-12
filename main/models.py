import uuid
from django.db import models

# Create your models here.
class Product(models.Model):
    SPORTS_PRODUCT_CATEGORY = [
            ('acsessoris', 'Acsessoris'),
            ('footwear', 'Footwear'),
            ('protective gear', 'Protective Gear'),
            ('team kit', 'Team Kit'),
            ('match equipment', 'Match Equipment'),
            ('training equipment', 'Training Equipment'),
            ('uncategorized', 'Uncategorized')
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # become a primary key
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=30, choices=SPORTS_PRODUCT_CATEGORY,default='uncategorized')
    is_featured = models.BooleanField(default=False) # is the product is featured
    stock = models.PositiveIntegerField(default=0) # available stock
    quantity_purchased = models.PositiveIntegerField(default=0) # quantity purchased by user

    def __str__(self):
        return self.name

    @property
    def is_thebest_seller(self):
        return self.quantity_purchased >= 10

    def update_stok(self):
        if self.stock >= 0 and self.quantity_purchased <= self.stock:
            self.stock -= self.quantity_purchased
        self.save()

    def total_price(self):
        return self.price * self.quantity_purchased
    
from django.contrib.auth.models import AbstractUser
from django.db import models

'''
Models: Your application should have at least 
three models in addition to the User model: 
one for auction listings, one for bids, and 
one for comments made on auction listings. 
It’s up to you to decide what fields each model should have, 
and what the types of those fields should be. 
You may have additional models if you would like
'''

class User(AbstractUser):
    pass

class AuctionListing(models.Model):

    CATEGORY = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electornics'),
        ('Home', 'Home'),
        ('Outdoors', 'Outdoors'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=800)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=12, choices= CATEGORY, blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(AuctionListing)

    def __str__(self):
        return f"Watchlist {self.id} - User: {self.user.username}"
  
class Bids(models.Model):
    pass

class Comments(models.Model):
    pass

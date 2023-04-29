from django.forms import ModelForm
from auctions.models import AuctionListing

# create the form class for auction listing
class NewListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']

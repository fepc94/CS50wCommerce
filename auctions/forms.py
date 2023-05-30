from django.forms import ModelForm
from auctions.models import AuctionListing, Bids

# Create the form class for auction listing
class NewListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']

class PlaceBid(ModelForm):
    class Meta:
        model = Bids
        fields = ['place_bid']
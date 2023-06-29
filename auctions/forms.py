from django.forms import ModelForm
from auctions.models import AuctionListing, Bid, Comment

# Create the form class for auction listing
class NewListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']

class PlaceBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['place_bid']

class AddComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

'''
TODO: https://www.youtube.com/watch?v=6-XXvUENY_8 Para hacer el FRONTEND
'''
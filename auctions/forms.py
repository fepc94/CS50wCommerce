from django import forms
from auctions.models import AuctionListing, Bid, Comment

# Create the form class for auction listing
class NewListing(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class PlaceBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['place_bid']
        widgets = {
            'place_bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import AuctionListing, Watchlist
from .forms import NewListing

from .models import User


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {'listings' : listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            # create a watchlist for every user
            try:
                watchlist = Watchlist.objects.get(user=user)
            except Watchlist.DoesNotExist:
                watchlist = Watchlist.objects.create(user=user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)            
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    return render(request, 'auctions/listing_page.html', {'listing' : listing})

@login_required
def new_listing(request):
    if request.method == 'POST':
        form = NewListing(request.POST)

        if form.is_valid():
            listing = form.save()
            # take into account what user is creating the listing
            listing.created_by = request.user
            listing.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NewListing()
    
    return render(request, 'auctions/new_listing.html', {'form' : form})

@login_required
def watchlist(request):
    watchlist = request.user.watchlist.listings.all()
    return render(request, 'auctions/watchlist.html', {'watchlist' : watchlist})

@login_required
def add_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    request.user.watchlist.listings.add(listing)
    return HttpResponseRedirect(reverse('index'))

@login_required
def remove_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if listing in request.user.watchlist.listings.all():
        request.user.watchlist.listings.remove(listing)
    return HttpResponseRedirect(reverse('index'))

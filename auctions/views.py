from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AuctionListing, Watchlist, Comment, Bid
from .forms import NewListing, PlaceBid, AddComment

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

        # create a watchlist for every user
        try:
            watchlist = Watchlist.objects.get(user=user)
        except Watchlist.DoesNotExist:
            watchlist = Watchlist.objects.create(user=user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_page(request, listing_id):

    listing = AuctionListing.objects.get(pk=listing_id)
    owner = listing.created_by
    comments = Comment.objects.filter(listings=listing_id)
    form1 = PlaceBid()
    form2 = AddComment()

    if owner == request.user:

        return render(request, 'auctions/listing_page.html', 
                {'listing' : listing, 
                'form2' : form2, 
                'comments' : comments })

    elif listing.active_status == False:

        max_bid = Bid.objects.get(place_bid=listing.start_bid)
        user_won = max_bid.user_id
        
        if request.user.id == user_won:

            succes_message = " Congratulations, you won this Auction !"
            messages.success(request, succes_message)

            return render(request, 'auctions/listing_page.html', 
                    {'listing' : listing, 
                    'form2' : form2, 
                    'comments' : comments })

        else:

            error_message = "This Listing has been closed."
            messages.error(request, error_message)

            return render(request, 'auctions/listing_page.html', 
                    {'listing' : listing, 
                    'form2' : form2, 
                    'comments' : comments })

    else:
        return render(request, 'auctions/listing_page.html', 
                {'listing' : listing, 
                'form1' : form1, 
                'form2' : form2, 
                'comments' : comments })

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

@login_required
def set_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    if request.method == 'POST':
        form1 = PlaceBid(request.POST)

        if form1.is_valid():
            # commit = False prevents the form to store any bid to db
            new_bid = form1.save(commit=False)

            # assign the bid to the logged in user.
            new_bid.user = request.user

            if new_bid.place_bid > listing.start_bid:
                new_bid.save()
                listing.start_bid = new_bid.place_bid
                listing.save()

                succes_message = "Successful Bid !"
                messages.success(request, succes_message)

                # Add the listing to the new bid
                new_bid.listings.add(listing)

                return HttpResponseRedirect(reverse('listing_page', args=[listing_id]))
            
            else:
                error_message = "Your bid must be higher than the current price."
                messages.error(request, error_message)
                return HttpResponseRedirect(reverse('listing_page', args=[listing_id]))           
 
    else: 
        form1 = PlaceBid()

    return render(request, 'auctions/listing_page.html', {'form': form1, 'listing': listing})

@login_required
def add_comment(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    if request.method == 'POST':
        form2= AddComment(request.POST)

        if form2.is_valid():
            new_comment = form2.save()

            # track the user that place the bid
            new_comment.user = request.user
            # Add the listing to the new comment
            new_comment.listings.add(listing)
            new_comment.save()

            succes_message = "Successful Comment !"
            messages.success(request, succes_message)

            return HttpResponseRedirect(reverse('listing_page', args=[listing_id]))

    else: 
        form2 = AddComment()

    return render(request, 'auctions/listing_page.html', {'form': form2, 'listing': listing})

@login_required()
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.active_status = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))
        
def categories(request):
    categories = AuctionListing.CATEGORY
    return render(request, 'auctions/categories.html', {'categories': categories})

def list_by_category(request, cat):
    listings = AuctionListing.objects.filter(category=cat)
    print(listings)
    return render(request, 'auctions/by_category.html', {'listings': listings})

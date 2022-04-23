from ast import arg
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from decimal import Decimal

from .models import User, AuctionListing, AuctionBid, AuctionComment, AuctionCategory


# Displays all the listings in the database
def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Used to display listing or close the listing
def listing_view(request, listing_id):
    # Close the current auction
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        listing.auction_status = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    # Handling non-existent page
    # try:
    listing = AuctionListing.objects.get(pk=listing_id)
    try:
        in_user_watchlist = request.user.watchlist.filter(
            pk=listing_id).first()
    except AttributeError:
        in_user_watchlist = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.auction_comment.all().order_by("-id"),
        "in_user_watchlist": in_user_watchlist
    })
    # except:
    # return render(request, "auctions/error.html")


@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        comment = request.POST.get("comment", "")
        if comment != "":
            new_comment = AuctionComment(
                listing=listing, comment_author=request.user, comment=comment)
            new_comment.save()

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def create_bid(request, listing_id):
    if request.method == "POST":
        bid_amount = Decimal(request.POST.get("bid_amount", 0))
        listing = AuctionListing.objects.get(pk=listing_id)

        # Decimal.compare() returns an integer
        # 1 means that the first decimal is more than the second
        if bid_amount.compare(listing.highest_bid) == 1:
            # Creating a new bid row and save it into AuctionBid model
            new_bid = AuctionBid(
                listing=listing, bid_holder=request.user, bid=bid_amount)
            new_bid.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def categories_view(request):
    return render(request, "auctions/categories.html", {
        "categories": AuctionCategory.objects.all()
    })


def category_view(request, category):
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": AuctionCategory.objects.get(category_name=category).auction_listing.all()
    })


# Displaying all the listings that the user has saved in their watchlist
@login_required
def watchlist_view(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        # Checking if listing exists
        if AuctionListing.objects.filter(pk=listing_id).exists():
            watchlist_action = request.POST["watchlist_action"]
            # Adding a watchlist to the user's watchlist
            if watchlist_action == "add":
                request.user.watchlist.add(
                    AuctionListing.objects.get(pk=listing_id))
            # Removing the watchlist
            else:
                request.user.watchlist.remove(
                    AuctionListing.objects.get(pk=listing_id))

        return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })


@ login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        initial_bid = Decimal(request.POST.get("initial_bid", 0))
        img_url = request.POST.get("img_url", "")
        category = request.POST.get("category", "")

        form_invalid = False
        # Returning the form if title doesn't exist
        if title == "":
            messages.warning(request, "A Title is needed for the auction!")
            form_valid = True

        # If the initial bid is less than 0
        if initial_bid.compare(0) == -1:
            messages.warning(request, "A bid can not be a negative number!")
            form_invalid = True

        if form_invalid:
            return render(request, "auctions/create.html", {
                "title": title,
                "description": description,
                "inital_bid": initial_bid,
                "img_url": img_url,
                "category": category
            })

        new_listing = AuctionListing(
            title=title, description=description, img_url=img_url, auction_owner=request.user)
        # new_listing has to be saved before assigning a category to it.
        new_listing.save()
        if category != "":
            # Adding category to the database if it does not yet exist
            if not AuctionCategory.objects.filter(category_name=category).exists():
                new_category = AuctionCategory(category_name=category)
                new_category.save()

            new_listing.category.add(AuctionCategory.objects.get(
                category_name=category))

        new_bid = AuctionBid(listing=new_listing,
                             bid_holder=request.user, bid=initial_bid)
        new_bid.save()
        return HttpResponseRedirect(reverse("listing", args=[new_listing.id]))

    return render(request, "auctions/create.html")

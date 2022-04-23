from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "AuctionListing", blank=True, related_name="watchlist")

    def __str__(self):
        return self.username


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    img_url = models.URLField(blank=True)
    category = models.ManyToManyField(
        "AuctionCategory", blank=True, related_name="auction_listing")
    date_created = models.DateTimeField(auto_now_add=True)
    auction_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(
        get_sentinel_user), blank=True, null=True, default=None, related_name="owned_auction")
    auction_status = models.BooleanField(default=True)

    @property
    def highest_bid_str(self):
        # Bid is ordered by lowest to highest so last() gives us the highest bid
        return "${:,.2f}".format(self.auction_bid.all().order_by('bid').last().bid)

    @property
    def highest_bid(self):
        # Bid is ordered by lowest to highest so last() gives us the highest bid
        return self.auction_bid.all().order_by('bid').last().bid

    @property
    def bid_count(self):
        return self.auction_bid.all().count()

    @property
    def latest_holder(self):
        return self.auction_bid.latest("id").bid_holder

    @property
    def all_categories(self):
        return self.category.all()

    def __str__(self):
        return f"{self.title} is on auction."


class AuctionBid(models.Model):
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="auction_bid")
    bid_holder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), blank=True, null=True, default=None, related_name="auction_bid")
    bid = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.bid}$ bid on {self.listing.title} by {self.bid_holder}"


class AuctionComment(models.Model):
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="auction_comment")
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), blank=True, null=True, default=None, related_name="auction_comment")
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.comment_author.username} commented on \"{self.listing.title}\" auction"


class AuctionCategory(models.Model):
    category_name = models.CharField(
        max_length=64, blank=True)

    def __str__(self):
        return self.category_name

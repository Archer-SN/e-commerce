from django.contrib import admin

from .models import User, AuctionListing, AuctionBid, AuctionComment, AuctionCategory

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(AuctionBid)
admin.site.register(AuctionComment)
admin.site.register(AuctionCategory)

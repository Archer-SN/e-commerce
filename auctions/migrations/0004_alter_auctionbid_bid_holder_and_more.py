# Generated by Django 4.0.4 on 2022-04-21 04:57

import auctions.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionbid_bid_holder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionbid',
            name='bid_holder',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=models.SET(auctions.models.get_sentinel_user), related_name='auction_bid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctioncomment',
            name='comment_author',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=models.SET(auctions.models.get_sentinel_user), related_name='auction_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=models.SET(auctions.models.get_sentinel_user), related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
    ]

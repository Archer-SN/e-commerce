# Generated by Django 4.0.4 on 2022-04-22 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_auctionlisting_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctioncategory',
            old_name='category',
            new_name='category_name',
        ),
    ]

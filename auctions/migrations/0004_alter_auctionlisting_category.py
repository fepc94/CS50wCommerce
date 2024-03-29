# Generated by Django 4.2 on 2023-07-17 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_remove_bid_listings_bid_listings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionlisting",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Fashion", "Fashion"),
                    ("Toys", "Toys"),
                    ("Electronics", "Electornics"),
                    ("Home", "Home"),
                    ("Outdoors", "Outdoors"),
                    ("Books", "Books"),
                    ("Music", "Music"),
                ],
                default="",
                max_length=12,
            ),
        ),
    ]

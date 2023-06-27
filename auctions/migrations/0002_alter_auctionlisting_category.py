# Generated by Django 4.2 on 2023-06-19 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
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
                ],
                default="",
                max_length=12,
            ),
        ),
    ]
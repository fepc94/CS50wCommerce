# Generated by Django 4.2 on 2023-05-30 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0009_alter_bids_place_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bids",
            name="place_bid",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
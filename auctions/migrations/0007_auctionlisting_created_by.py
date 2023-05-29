# Generated by Django 4.2 on 2023-05-29 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_alter_auctionlisting_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

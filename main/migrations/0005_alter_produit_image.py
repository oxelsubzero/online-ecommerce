# Generated by Django 4.2.4 on 2023-08-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_alter_produit_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produit",
            name="image",
            field=models.ImageField(upload_to="static/images/"),
        ),
    ]

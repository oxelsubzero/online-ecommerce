# Generated by Django 4.2.4 on 2023-08-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_adresse"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produit",
            name="image",
            field=models.ImageField(upload_to="media/images/produits"),
        ),
    ]

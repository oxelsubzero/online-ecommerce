# Generated by Django 4.2.4 on 2023-08-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0013_alter_total_value"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="total",
            name="value",
        ),
        migrations.AddField(
            model_name="total",
            name="total_amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

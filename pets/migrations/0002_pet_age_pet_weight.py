# Generated by Django 4.2 on 2023-04-06 02:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="age",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="pet",
            name="weight",
            field=models.FloatField(null=True),
        ),
    ]

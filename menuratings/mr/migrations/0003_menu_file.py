# Generated by Django 3.0.7 on 2020-06-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mr", "0002_auto_20200624_1516"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]

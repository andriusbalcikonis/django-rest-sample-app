# Generated by Django 3.0.7 on 2020-06-25 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mr", "0003_menu_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="menu_file_uplods"),
        ),
    ]

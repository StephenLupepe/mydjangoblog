# Generated by Django 4.1.1 on 2022-10-09 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, upload_to="<str: username>/images"),
        ),
    ]

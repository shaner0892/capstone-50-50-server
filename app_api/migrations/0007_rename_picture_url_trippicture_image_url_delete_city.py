# Generated by Django 4.0.4 on 2022-06-17 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0006_alter_trip_fifty_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trippicture',
            old_name='picture_url',
            new_name='image_url',
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]

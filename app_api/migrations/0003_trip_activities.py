# Generated by Django 4.0.4 on 2022-06-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0002_rename_user_ratereview_fifty_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='activities',
            field=models.ManyToManyField(related_name='trips', to='app_api.activity'),
        ),
    ]

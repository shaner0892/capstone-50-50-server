# Generated by Django 4.0.4 on 2022-06-08 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratereview',
            old_name='user',
            new_name='fifty_user',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='user',
            new_name='fifty_user',
        ),
        migrations.AlterField(
            model_name='state',
            name='established',
            field=models.CharField(max_length=20),
        ),
    ]

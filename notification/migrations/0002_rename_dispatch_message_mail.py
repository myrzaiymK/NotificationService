# Generated by Django 4.2.3 on 2023-07-15 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='dispatch',
            new_name='mail',
        ),
    ]

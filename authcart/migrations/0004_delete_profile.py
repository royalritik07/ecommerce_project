# Generated by Django 4.1.13 on 2024-04-04 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authcart', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

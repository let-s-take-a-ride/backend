# Generated by Django 4.2.6 on 2023-10-23 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_userpreferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='profile_pics/'),
        ),
    ]

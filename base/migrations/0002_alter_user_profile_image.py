# Generated by Django 5.0.2 on 2024-02-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to=''),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-31 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arch_App', '0018_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]

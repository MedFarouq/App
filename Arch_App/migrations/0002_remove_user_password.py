# Generated by Django 4.2.3 on 2023-07-20 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Arch_App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]

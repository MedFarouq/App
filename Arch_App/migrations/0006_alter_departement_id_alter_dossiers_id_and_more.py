# Generated by Django 4.2.3 on 2023-07-24 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arch_App', '0005_rename_dossier_dossiers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departement',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='dossiers',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='fichier',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

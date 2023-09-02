from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class Departement(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
    def formatted_date(self):
        return self.modification.strftime('%Y-%m-%d')

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class Dossier(models.Model):
    id = models.AutoField(primary_key=True,)
    nom = models.CharField(max_length=100)
    size = models.IntegerField(default=0)
    modification = models.DateField(auto_now=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    def formatted_date(self):
        return self.modification.strftime('%Y-%m-%d')

    get_class = 'dossier'
    
class Fichier(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    chemin = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    modification = models.DateField(auto_now=True)
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    def __str__(self):
        
        return self.nom
    
    get_class = 'fichier'

class Log(models.Model):
    nature      = models.CharField(max_length=100)
    # [created-deleted-updated-printed]
    nom = models.CharField(max_length=100)
    size = models.IntegerField(default=0)
    modification = models.DateField(auto_now=True)

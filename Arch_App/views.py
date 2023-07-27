import os
from django.http import HttpResponse
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as loginDjango
from django.contrib.auth import logout
from .models import Dossier, Fichier



def login(request):
  if str(request.user) == 'AnonymousUser':
  
    if request.method == 'POST':
          email = request.POST.get('email')
          password = request.POST.get('password')
          user = User.objects.filter(email=email).filter(password=password).first()

          if user is not None:
              loginDjango(request, user)
              return redirect('homepage')
          else:
              message = "Adresse e-mail ou mot de passe incorrect."
              return render(request, 'arch/login.html', {'message': message})
  
    return render(request, 'arch/login.html')
  else :
    return redirect('homepage')

def register(request):
  if str(request.user) == 'AnonymousUser':
    if request.method == 'POST':
          username = request.POST['Firstname'] + request.POST['Lastname']
          email = request.POST['email']
          password = request.POST['password']
          # Valider les données si nécessaire
          # Sauvegarder l'utilisateur dans la base de données
          user = User(username=username, password=password, email=email)
          user.save()
          # Rediriger l'utilisateur vers la page de connexion après l'inscription
          return redirect('login')
    return render(request, 'arch/register.html')
  else :
    return redirect('homepage')

def homepage(request):
  if str(request.user) == 'AnonymousUser':
    return redirect('login')
  return render(request, 'arch/homepage.html')
  

def loginAtempt(request):
  return render(request, 'arch/login.html')


def logOut(request):
  if str(request.user) != 'AnonymousUser':
    logout(request)
  return redirect('login')


def details(request, dossier):
  if str(request.user) == 'AnonymousUser':
    return redirect('login')
  dossier = Dossier.objects.filter(pk=dossier).first()
  return render(request, 'departement/details.html', {'dossiers': dossier.fichier_set.all(), 'nom': dossier.nom})
  
def departementDetails(request, nom_departement):
  if str(request.user) == 'AnonymousUser':
    return redirect('login')
  dossiers = Dossier.objects.filter(departement__nom=nom_departement)
  for dossier in dossiers:
    dossier.size = dossier.fichier_set.count()

  return render(request, 'departement/details.html', {'dossiers': dossiers, 'nom': nom_departement})

def detailsFile(request, fichier):
  if str(request.user) == 'AnonymousUser':
    return redirect('login')
  fichier = Fichier.objects.filter(pk=fichier).first()

  """ if request.user.departement_id != fichier.dossier.departement_id:
    return HttpResponse(404) """

  

 #headres
  with open(f"{fichier.chemin}", 'rb') as pdf:
          response = HttpResponse(pdf.read(), content_type='application/pdf')
          response['Content-Disposition'] = f"inline;filename={fichier.nom}"
          return response

import os
from django.http import HttpResponse
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as loginDjango
from django.contrib.auth import logout
from .models import Dossier, Fichier,Log
from django.http import JsonResponse
import json



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
          user = User(username=username, password=password, email=email)
          user.save()
          return redirect('login')
    return render(request, 'arch/register.html')
  else :
    return redirect('homepage')

def homepage(request):
  if str(request.user) == 'AnonymousUser':
    return redirect('login')
  logs = Log.objects.all()
  return render(request, 'arch/homepage.html',{'logs': logs})
  

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


def delete_dossiers(request):
    if request.method == 'POST' :

        ids = json.loads(request.POST.get('ids'))

        try:
            for dossier in ids :

              if  dossier["type"] == 'True': # is dossier
                continue
              else:
                fichier = Fichier.objects.filter(pk=dossier["id"]).first()
                if os.path.isfile(fichier.chemin):
                  os.remove(fichier.chemin)
                fichier.delete()

            return JsonResponse({'message': 'Le dossier a été supprimé avec succès.'})
        except Dossier.DoesNotExist:
            # Si le dossier n'existe pas, renvoyer une réponse JSON avec un message d'erreur
            return JsonResponse({'message': 'Le dossier n\'existe pas.'}, status=400)
    else:
        # Rediriger l'utilisateur vers la page d'accueil en cas de requête invalide
        return redirect('homepage')

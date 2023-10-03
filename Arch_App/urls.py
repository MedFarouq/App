from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('loginAtempt/',views.loginAtempt,name='loginAtempt'),
    path('register/',views.register,name='register'),
    path('logOut/',views.logOut,name='logOut'),
    path('homepage/',views.homepage,name='homepage'),
    path('details/<dossier>',views.details,name='details'),
    path('details_file/<fichier>',views.detailsFile,name='detailsFile'),
    path('delete_dossiers/', views.delete_dossiers, name='delete_dossiers'),
    path('add_dossiers/', views.add_dossiers, name='add_dossiers'),
    path('<str:nom_departement>/', views.departementDetails, name='departementDetails'),

]

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
    path('<str:nom_departement>/', views.departementDetails, name='departementDetails'),

]

from django.urls import path
from membre import views

urlpatterns = [
	path('retourner-taux-membre/', views.retourner_taux_membre ,
	 name = "rechercher-membre"),

	path('retourner-entreprise-info/', views.retourner_entreprise_info , 
	name = "rechercher-entreprise-info"),

	path('retourner-consommateur-info/', views.retourner_consommateur_info ,
	name = "rechercher-consommateur-info"),
]
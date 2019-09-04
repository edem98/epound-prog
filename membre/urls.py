from django.urls import path
from membre import views

app_name = 'membre'

urlpatterns = [
    path('retourner-taux-membre/', views.retourner_taux_membre,
         name="rechercher-membre"),

    path('retourner-entreprise-info/', views.retourner_entreprise_info,
         name="rechercher-entreprise-info"),

    path('retourner-consommateur-info/', views.retourner_consommateur_info,
         name="rechercher-consommateur-info"),

    path('generer-mot-de-passe/<int:id>', views.generer_mot_de_passe,
         name="generer"),

]

from django.urls import path, include
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('<str:besoin>/', views.specification_besoin, name ="besoin-specification"),
    path('categories/<int:id_specification>/', views.categorie_specification, name="specification-categories"),
    path('produits-categories/<int:id_categorie>/', views.produit_par_categorie, name="categories-produits"),
    path('produits-specification/<str:specification>/', views.produit_par_specification, name="specification-produits"),

]

from django.urls import path, include
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('troc/login', views.login_troc, name ="troc-login"),
    path('troc/logout', views.logout_troc, name ="troc-logout"),
    path('troc/home', views.troc_home, name ="troc-home"),
    path('troc/profile', views.profile_troc, name ="troc-profile"),
    path('troc/gerer-article', views.gerer_mes_articles, name ="troc-gerer-article"),
    path('troc/ajouter-article', views.AddTrocProduct.as_view(), name ="troc-ajouter-article"),
    path('troc/article-troquer', views.ArticleVendu.as_view(), name ="troc-article-troquer"),
    path('troc/all-article', views.AllArticle.as_view(), name ="troc-all-article"),
    path('rechercher-produit', views.rechercher_produit, name ="rechercher-produit"),
    path('specification-besoin/', views.specification_besoin_json, name ="besoin-specification-json"),
    path('<str:besoin>/', views.specification_besoin, name ="besoin-specification"),
    path('categories/<int:id_specification>/', views.categorie_specification, name="specification-categories"),
    path('produits-categories/<int:id_categorie>/', views.produit_par_categorie, name="categories-produits"),
    path('produits-specification/<str:specification>/', views.produit_par_specification, name="specification-produits"),

]

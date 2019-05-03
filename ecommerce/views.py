from PIL.PngImagePlugin import _idat
from django.shortcuts import render
from django.views.generic import ListView

from ecommerce.models import *
from membre.models import EntrepriseCommerciale, Partenaire


def specification_besoin(request, besoin):
    context = {}
    besoin = ExpressionBesoin.objects.get(besoin = besoin)
    specifications = SpécificationBesoin.objects.filter(besoin_fondamental = besoin)
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:20]
    context['besoin'] = besoin
    context['specifications'] = specifications
    context['produits'] = new_produits
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    return render(request,'ecommerce/specification.html',context)

def categorie_specification(request, id_specification):
    context = {}
    specification = SpécificationBesoin.objects.get(id = id_specification)
    categories = Categorie.objects.filter(specification = specification)
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:20]
    context['categories'] = categories
    context['specification'] = specification
    context['produits'] = new_produits
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    return render(request,'ecommerce/categorie.html',context)

def produit_par_specification(request, specification):
    context = {}
    if specification != "Alimentation générale":
        specification = SpécificationBesoin.objects.get(spécification=specification)
        produits = Produit.objects.filter(categorie_besoin__spécification = specification,disponible=True)
        partenaires = Partenaire.objects.all()[:4]
        context['produits'] = produits
        context['specification'] = specification
        context['partenaires'] = partenaires
        return render(request,'ecommerce/products-specification.html',context)
    else:
        print(specification)
        entreprises = EntrepriseCommerciale.objects.filter(besoin_gere__spécification=specification)
        context['entreprises'] = entreprises
        return render(request,'entreprise.html',context)

def produit_par_categorie(request, id_categorie):
    context = {}
    categorie = Categorie.objects.get(id = id_categorie)
    produits = Produit.objects.filter(categorie=categorie,disponible=True)
    context['produits'] = produits
    context['categorie'] = categorie
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    return render(request,'ecommerce/products-categorie.html',context)

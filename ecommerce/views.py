from PIL.PngImagePlugin import _idat
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import LoginForm

from ecommerce.models import *
from membre.models import EntrepriseCommerciale, Partenaire, ConsommateurParticulier


def login_troc(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            phone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']
            try:
                consomateur = ConsommateurParticulier.objects.get(telephone=phone)
                if check_password(password, consomateur.user.password):
                    user = authenticate(request, username=consomateur.user.username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('ecommerce:troc-home')
            except Exception as e:
                print(e)
        else:
            print(form.errors)
            return render(request, 'ecommerce/troc_login.html', context)
    else:
        form = LoginForm()
        context['form'] = form
    return render(request, 'ecommerce/troc_login.html', context)


def troc_home(request):
    context = {}
    try:
        consommateur = ConsommateurParticulier.objects.get(user=request.user)
        produits = ProduitTroc.objects.filter(disponible=True).exclude(vendeur=consommateur)
        context['consommateur'] = consommateur
        context['produits'] = produits
        categories = Categorie.objects.all()
        context['categories'] = categories
        return render(request, 'ecommerce/troc_home.html', context)
    except Exception as e:
        print(e)
        return redirect('ecommerce:troc-login')


def gerer_mes_articles(request):
    context = {}
    try:
        consommateur = ConsommateurParticulier.objects.get(user=request.user)
        produit_dispo = ProduitTroc.objects.filter(vendeur=consommateur, disponible=True)
        context['consommateur'] = consommateur
        context['produit_dispo'] = produit_dispo
        return render(request, 'ecommerce/gerer_articles.html', context)
    except Exception:
        return redirect('ecommerce:troc-login')


def specification_besoin(request, besoin):
    context = {}
    besoin = ExpressionBesoin.objects.get(besoin=besoin)
    specifications = SpécificationBesoin.objects.filter(besoin_fondamental=besoin)
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:20]
    context['besoin'] = besoin
    context['specifications'] = specifications
    context['produits'] = new_produits
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    categories = Categorie.objects.all()
    context['categories'] = categories
    return render(request, 'ecommerce/specification.html', context)


def specification_besoin_json(request):
    besoin = request.GET.get('besoin')
    besoin = ExpressionBesoin.objects.get(pk=besoin)
    specifications = SpécificationBesoin.objects.filter(besoin_fondamental=besoin)
    specification_retournees = []
    for specification in specifications:
        specification_retournees.append({
            'id': specification.pk,
            'label': specification.spécification,
        })
    data = {'specifications': specification_retournees}
    return JsonResponse(data)


def rechercher_produit(request):
    """
    Ce controlleur renvoie les produits correspondant au parametre specifier dans
    le formulaire apres formatage en donnees Json
    :param request:
    :return: JsonResponse de produit correspondant
    """
    produit = request.GET.get('produit')
    categorie = request.GET.get('categorie')
    print(categorie)
    if categorie:
        categorie = int(categorie)
    produits = Produit.objects.filter(nom__icontains=produit,categorie=categorie)
    context = {'produits': produits}
    return render(request, 'ecommerce/product_found.html', context)


def categorie_specification(request, id_specification):
    context = {}
    specification = SpécificationBesoin.objects.get(id=id_specification)
    categories = Categorie.objects.filter(specification=specification)
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:20]
    context['categories'] = categories
    context['specification'] = specification
    context['produits'] = new_produits
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    return render(request, 'ecommerce/categorie.html', context)


def produit_par_specification(request, specification):
    context = {}
    if specification != "Alimentation générale":
        specification = SpécificationBesoin.objects.get(spécification=specification)
        produits = Produit.objects.filter(categorie_besoin__spécification=specification, disponible=True)
        partenaires = Partenaire.objects.all()[:4]
        context['produits'] = produits
        context['specification'] = specification
        context['partenaires'] = partenaires
        categories = Categorie.objects.all()
        context['categories'] = categories
        return render(request, 'ecommerce/products-specification.html', context)
    else:
        print(specification)
        entreprises = EntrepriseCommerciale.objects.filter(besoin_gere__spécification=specification)
        context['entreprises'] = entreprises
        categories = Categorie.objects.all()
        context['categories'] = categories
        return render(request, 'entreprise.html', context)


def produit_par_categorie(request, id_categorie):
    context = {}
    categorie = Categorie.objects.get(id=id_categorie)
    produits = Produit.objects.filter(categorie=categorie, disponible=True)
    context['produits'] = produits
    context['categorie'] = categorie
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    return render(request, 'ecommerce/products-categorie.html', context)

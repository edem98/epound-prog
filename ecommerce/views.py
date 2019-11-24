from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from archive.models import CommandeClient
from .forms import LoginForm, AddProductTrocForm
from django.contrib.auth.decorators import login_required
from ecommerce.models import *
from membre.models import EntrepriseCommerciale, Partenaire, ConsommateurParticulier, Quartier
from django.contrib.auth.mixins import LoginRequiredMixin


def login_home(request):
    next = request.GET.get('next')
    context = {}
    if request.method == "POST":
        print(request.path)
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
                        print(next)
                        return redirect(next)
                    else:
                        error_message = "User authentiction failed"
                        context['error_message'] = error_message
                        return render(request, 'login.html', context)
                else:
                    error_message = "Password not checked"
                    context['error_message'] = error_message
                    return render(request, 'login.html', context)
            except Exception as e:
                print("------------------")
                print(e)
        else:
            context['errors'] = form.errors
            return render(request, 'login.html', context)
    else:
        form = LoginForm()
        categories = Categorie.objects.all()
        context['categories'] = categories
        context['form'] = form
        context['next'] = next
    return render(request, 'login.html', context)


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
                    else:
                        print("User authentiction failed")
                else:
                    print("Password not checked")
            except Exception as e:
                print(e)
        else:
            print(form.errors)
            return render(request, 'ecommerce/troc_login.html', context)
    else:
        if request.user.is_authenticated:
            return redirect('ecommerce:troc-home')
        form = LoginForm()
        categories = Categorie.objects.all()
        context['categories'] = categories
        context['form'] = form
    return render(request, 'ecommerce/troc_login.html', context)


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
    emplacements = Quartier.objects.all()
    context['emplacements'] = emplacements
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
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
    :return: Response de produit correspondant
    """
    produit = request.GET.get('produit')
    categorie = request.GET.get('categorie')
    emplacement = request.GET.get('emplacement')
    vendeur = request.GET.get('vendeur')
    produits = Produit.objects.filter(disponible=True)
    if produit:
        produits = produits.filter(nom__icontains=produit)
    if categorie:
        categorie = int(categorie)
        produits = produits.filter(categorie=categorie)
    if emplacement:
        emplacement = int(emplacement)
        produits = produits.filter(vendeur__emplacement=emplacement)
    if vendeur:
        vendeur = int(vendeur)
        print("----------")
        print(vendeur)
        produits = produits.filter(vendeur=vendeur)
    context = {'produits': produits}
    categories = Categorie.objects.all()
    context['categories'] = categories
    emplacements = Quartier.objects.all()
    context['emplacements'] = emplacements
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
    return render(request, 'ecommerce/product_found.html', context)


def rechercher_produit_json(request):
    """
    Ce controlleur renvoie les produits correspondant au parametre specifier dans
    le formulaire apres formatage en donnees Json
    :param request:
    :return: JsonResponse de produit correspondant
    """
    nom = request.GET.get('produit')
    produits = Produit.objects.filter(nom__icontains=nom)
    produit_list = []
    for item in produits:
        produit_list.append(item.nom)
    context = {'produits': list(produit_list)}
    return JsonResponse(context)


def categorie_specification(request, id_specification):
    context = {}
    specification = SpécificationBesoin.objects.get(id=id_specification)
    categories = Categorie.objects.filter(specification=specification)
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:20]
    emplacements = Quartier.objects.all()
    context['emplacements'] = emplacements
    context['categories'] = categories
    context['specification'] = specification
    context['produits'] = new_produits
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
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
        emplacements = Quartier.objects.all()
        context['emplacements'] = emplacements
        vendeurs = EntrepriseCommerciale.objects.all()
        context['vendeurs'] = vendeurs
        return render(request, 'ecommerce/products-specification.html', context)
    else:
        print(specification)
        entreprises = EntrepriseCommerciale.objects.filter(besoin_gere__spécification=specification)
        context['entreprises'] = entreprises
        categories = Categorie.objects.all()
        context['categories'] = categories
        vendeurs = EntrepriseCommerciale.objects.all()
        context['vendeurs'] = vendeurs
        return render(request, 'entreprise.html', context)


def produit_par_categorie(request, id_categorie):
    context = {}
    categorie = Categorie.objects.get(id=id_categorie)
    produits = Produit.objects.filter(categorie=categorie, disponible=True)
    context['produits'] = produits
    context['categorie'] = categorie
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
    return render(request, 'ecommerce/products-categorie.html', context)


def besoin_vendeur(request, id_besoin):
    context = {}
    categories = Categorie.objects.all()
    context['categories'] = categories
    emplacements = Quartier.objects.all()
    context['emplacements'] = emplacements
    vendeurs = EntrepriseCommerciale.objects.filter(besoin_fondamental=id_besoin)
    context['entreprises'] = vendeurs
    besoins = ExpressionBesoin.objects.all().order_by('besoin')
    context['besoins'] = besoins
    return render(request, 'ecommerce/vendeur-besoin.html', context)


def besoin_vendeur_json(request, id_besoin):

    vendeurs = EntrepriseCommerciale.objects.filter(besoin_fondamental=id_besoin)
    returned_vendeurs = []
    for item in vendeurs:
        returned_vendeurs.append({
            'banniere_principal': str(item.banniere_principal.url),
            'nom': item.nom,
            'telephone': item.telephone,
            'email': item.email,
            'emplacement': str(item.emplacement),
            'localisation': item.localisation,
            'objet_social': item.objet_social,
        })
    context = {'vendeurs': returned_vendeurs}
    return JsonResponse(context)


@login_required
def logout_troc(request):
    logout(request)
    return redirect('ecommerce:troc-login')


@login_required
def profile_troc(request):
    consommateur = ConsommateurParticulier.objects.get(user=request.user)
    depense_autoriser = 60000 - consommateur.compte_consommateur.depense_epound_mensuel
    context = {'consommateur': consommateur, 'depense_autoriser': depense_autoriser, }
    return render(request,'ecommerce/profile.html', context)


@login_required
def troc_home(request):
    context = {}
    try:
        consommateur = ConsommateurParticulier.objects.get(user=request.user)
        produits = ProduitTroc.objects.filter(status=ProduitTroc.EN_VENTE).exclude(vendeur=consommateur)
        context['consommateur'] = consommateur
        context['produits'] = produits
        categories = Categorie.objects.all()
        context['categories'] = categories
        emplacements = Quartier.objects.all()
        context['emplacements'] = emplacements
        vendeurs = EntrepriseCommerciale.objects.all()
        context['vendeurs'] = vendeurs
        return render(request, 'ecommerce/troc_home.html', context)
    except Exception as e:
        print(e)
        return redirect('ecommerce:troc-login')


@csrf_exempt
def gerer_mes_articles(request):
    context = {}
    if request.method == 'POST':
        if request.POST.getlist('checkboxes[]'):
            items = request.POST.getlist('checkboxes[]')
            for item in items:
                produit = ProduitTroc.objects.get(id=int(item))
                produit.status = ProduitTroc.RETIRER
                produit.save()
            try:
                consommateur = ConsommateurParticulier.objects.get(user=request.user)
                produit_dispo = ProduitTroc.objects.filter(vendeur=consommateur, status=ProduitTroc.EN_VENTE)
                context['consommateur'] = consommateur
                context['produit_dispo'] = produit_dispo
                emplacements = Quartier.objects.all()
                context['emplacements'] = emplacements
                return render(request, 'ecommerce/gerer_articles.html', context)
            except Exception as e:
                print(e)
                return redirect('ecommerce:troc-login')
    else:
        try:
            consommateur = ConsommateurParticulier.objects.get(user=request.user)
            produit_dispo = ProduitTroc.objects.filter(vendeur=consommateur, status=ProduitTroc.EN_VENTE)
            context['consommateur'] = consommateur
            context['produit_dispo'] = produit_dispo
            emplacements = Quartier.objects.all()
            context['emplacements'] = emplacements
            vendeurs = EntrepriseCommerciale.objects.all()
            context['vendeurs'] = vendeurs
            return render(request, 'ecommerce/gerer_articles.html', context)
        except Exception as e:
            print(e)
            return redirect('ecommerce:troc-login')


@login_required
def commander_article(request, id_produit):
    produit = Produit.objects.get(id=id_produit)
    consommateur = ConsommateurParticulier.objects.get(user=request.user)
    return render(request,'ecommerce/single-product.html', {'produit': produit, 'consommateur': consommateur,})


@csrf_exempt
def valider_commande(request):
    if request.method == 'POST':
        consommateur = int(request.POST.get('consommateur'))
        quantite = int(request.POST.get('quantite'))
        produit = int(request.POST.get('produit'))
        # get reel element
        try:
            consommateur = ConsommateurParticulier.objects.get(id=consommateur)
            produit = Produit.objects.get(id=produit)
            commande = CommandeClient(numero_client=consommateur.telephone, numero_vendeur=produit.vendeur.telephone,
                                      code_produit=produit.code_article, quantite=quantite, a_livrer=True)
            commande.save()
            return JsonResponse({'success': "Votre commande a été valider avec succes."})
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Vous ne disposez du montant nécéssaire pour effectuer cette commande."})


class AddTrocProduct(CreateView,LoginRequiredMixin):
    model = ProduitTroc
    form_class = AddProductTrocForm
    template_name = 'ecommerce/ajouter_article.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        vendeur = ConsommateurParticulier.objects.get(user=self.request.user)
        product.vendeur = vendeur
        product.save()
        return super(AddTrocProduct, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid form")
        print(form.errors)
        return super(AddTrocProduct, self).form_invalid(form)


class ArticleVendu(ListView,LoginRequiredMixin):
    model = ProduitTroc
    queryset = ProduitTroc.objects.filter(status=ProduitTroc.VENDU)
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'ecommerce/article_troquer.html'

    def get_queryset(self):
        consommateur = ConsommateurParticulier.objects.get(user=self.request.user)
        queryset = ProduitTroc.objects.filter(vendeur=consommateur)
        queryset = queryset.filter(status=ProduitTroc.VENDU)
        return queryset


class ArticleRetire(ListView,LoginRequiredMixin):
    model = ProduitTroc
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'ecommerce/articles_retires.html'

    def get_queryset(self):
        consommateur = ConsommateurParticulier.objects.get(user=self.request.user)
        queryset = ProduitTroc.objects.filter(vendeur=consommateur)
        queryset = queryset.filter(status=ProduitTroc.RETIRER)
        print(queryset)
        return queryset


class AllArticle(ListView,LoginRequiredMixin):
    model = ProduitTroc
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'ecommerce/tous_les_articles.html'

    def get_queryset(self):
        consommateur = ConsommateurParticulier.objects.get(user=self.request.user)
        return ProduitTroc.objects.filter(vendeur=consommateur)

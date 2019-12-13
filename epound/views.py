from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from ecommerce.models import ExpressionBesoin, Produit, Categorie, SpécificationBesoin
from membre.models import EntrepriseCommerciale, Partenaire, ConsommateurParticulier
from membre.models import Quartier


def acceuil(request):
    context = {}
    besoins = ExpressionBesoin.objects.all()
    new_produits = Produit.objects.filter(disponible=True).order_by('?')[:60]
    partenaires = Partenaire.objects.all()

    categories = Categorie.objects.all()
    emplacements = Quartier.objects.all()

    context['emplacements'] = emplacements
    context['categories'] = categories
    context['besoins'] = besoins
    context['produits'] = new_produits
    context['partenaires'] = partenaires
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
    return render(request, 'index.html', context)


class ListEntreprise(ListView):
    model = EntrepriseCommerciale
    template_name = "entreprise.html"
    context_object_name = "entreprises"
    paginate_by = 100
    queryset = EntrepriseCommerciale.objects.filter(actif=True)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        categories = Categorie.objects.all()
        context['categories'] = categories
        emplacements = Quartier.objects.all()
        context['emplacements'] = emplacements
        vendeurs = EntrepriseCommerciale.objects.all()
        context['vendeurs'] = vendeurs
        besoins = ExpressionBesoin.objects.all().order_by('besoin')
        context['besoins'] = besoins
        return context


def about(request):
    context = {}
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:30]
    partenaires = Partenaire.objects.all()[:4]
    categories = Categorie.objects.all()
    emplacements = Quartier.objects.all()
    context['emplacements'] = emplacements
    context['categories'] = categories
    context['partenaires'] = partenaires
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
    return render(request, 'about.html', context)


def contact(request):
    if request.method == "POST":
        nom = request.POST.get('name')
        mail_de = request.POST.get('email')
        message = request.POST.get('message')
        sujet = "Information sur la epound Corp"
        if nom and message and mail_de:
            try:
                send_mail(sujet, message, mail_de, ['epoundcorporationtg@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    return render(request, 'contact.html')


def partenaires(request):
    context = {}
    partners = Partenaire.objects.all()
    context['partenaires'] = partners
    categories = Categorie.objects.all()
    context['categories'] = categories
    emplacements = Quartier.objects.all()
    context['emplacements'] = emplacements
    vendeurs = EntrepriseCommerciale.objects.all()
    context['vendeurs'] = vendeurs
    return render(request, 'partenaire.html', context)


def politique(request):
    return render(request, 'politique-de-confidentialite.html', )

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from ecommerce.models import ExpressionBesoin, Produit
from epound import settings
from membre.models import EntrepriseCommerciale, Partenaire
from . import settings
import requests
from django.contrib.staticfiles.views import serve


def view_function(request):
   return serve(request, '../static/encryptkey')

def envoyer_sms(message,destinataire,expediteur="epound Corp"):

    url = "http://sms.easysbyskegroup.com:8080/sendsms?username=ysms-epound&password=70011777&type=0&dlr=1&destination="+destinataire+"&source="+expediteur+"&message="+message
    resp = requests.request("POST",url)
    print(resp.status_code,resp.reason)
    print(resp.text[:300]+'...')

def acceuil(request):
    context = {}
    besoins = ExpressionBesoin.objects.all()
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:20]
    partenaires = Partenaire.objects.all()[:4]
    context['besoins'] = besoins
    context['produits'] = new_produits
    context['partenaires'] = partenaires
    return render(request, 'index.html', context)

class ListEntreprise(ListView):
    model = EntrepriseCommerciale
    template_name = "entreprise.html"
    context_object_name = "entreprises"
    paginate_by = 15
    queryset = EntrepriseCommerciale.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        partenaires = Partenaire.objects.all()
        context['partenaires'] = partenaires
        return context

def about(request):
    context = {}
    new_produits = Produit.objects.filter(disponible=True).order_by('-date_ajout')[:30]
    partenaires = Partenaire.objects.all()[:4]
    context['partenaires'] = partenaires
    return render(request, 'about.html', context)

def contact(request):
    if request.method == "POST":
        nom = request.POST.get('name')
        mail_de = request.POST.get('email')
        message = request.POST.get('message')
        sujet = "Information sur la epound Corp"
        if nom and message and mail_de:
            try:
                send_mail(sujet, message, mail_de, ['epoundcorporationtg@gmail.com'],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    return render(request, 'contact.html')

def partenaires(request):
    context = {}
    partners = Partenaire.objects.all()
    context['partenaires'] = partners
    return render(request, 'partenaire.html', context)


def politique(request):
    return render(request, 'politique-de-confidentialite.html',)
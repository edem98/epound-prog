from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from dashboard.tasks import *
from ecommerce.models import ExpressionBesoin, Produit
from epound import settings
from membre.models import EntrepriseCommerciale
from compte.tasks import *
from octroi.tasks import remboursemment_automatique


def acceuil(request):
    context = {}
    besoins = ExpressionBesoin.objects.all()
    new_produits = Produit.objects.all().order_by('-date_ajout')[:30]
    context['besoins'] = besoins
    context['produits'] = new_produits
    return render(request,'index.html',context)


class ListEntreprise(ListView):

    model = EntrepriseCommerciale
    template_name = "entreprise.html"
    context_object_name = "entreprises"
    paginate_by = 15
    queryset = EntrepriseCommerciale.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context


def about(request):
    return render(request,'index.html')

def faq(request):
    return render(request,'faqs/faqs.html',)

def contact(request):
    if request.method == "POST":
        nom = request.POST.get('name')
        mail_de = request.POST.get('email')
        settings.EMAIL_HOST_USER = mail_de
        message = request.POST.get('message')
        sujet = "Information sur la epound Corp"
        if nom and message and mail_de:
            try:
                send_mail(sujet, message, mail_de, ['epoundcorporationtg@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    return render(request,'contact.html')
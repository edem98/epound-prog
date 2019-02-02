from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from ecommerce.models import ExpressionBesoin, Produit
from epound import settings
from membre.models import EntrepriseCommerciale, Partenaire
from django.conf import settings
from urllib.request import Request, urlopen

def envoyer_sms(message,destinataire,expediteur="epound Corp"):

    url = Request("http://sms.easysbyskegroup.com:8080/sendsms?username=ysms-epound&password=70011777&type=0&dlr=1&destination="+destinataire+"&source="+expediteur+"&message="+message, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(url).read()


def send_sms(to, message):
    '''sms utility method'''

    media_url = "http://sms.easysbyskegroup.com:8080/sendsms?username=ysms-epound&password=70011777&type=0&dlr=1&destination=999999999&source=xxxxx&message=xxxxxxx"
    message = message.encode('utf-8')
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(body=message, to=to, from_='+18639008466')
    return response


def sms_sender(message, to):
    to = "+228" + "" + to
    response = send_sms(to, message)
    print(response)


def acceuil(request):
    context = {}
    besoins = ExpressionBesoin.objects.all()
    new_produits = Produit.objects.all().order_by('-date_ajout')[:100]
    context['besoins'] = besoins
    context['produits'] = new_produits
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
        return context


def about(request):
    context = {}
    new_produits = Produit.objects.all().order_by('-date_ajout')[:30]
    context['produits'] = new_produits
    return render(request, 'about.html', context)


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
    return render(request, 'contact.html')


def partenaires(request):
    context = {}
    partners = Partenaire.objects.all()
    context['partenaires'] = partners
    return render(request, 'partenaire.html', context)
from django.shortcuts import render
from django.views.generic import ListView
from ecommerce.models import ExpressionBesoin, Produit
from membre.models import EntrepriseCommerciale


def acceuil(request):
    context = {}
    besoins = ExpressionBesoin.objects.all()
    new_produits = Produit.objects.all().order_by('-date_ajout')[:10]
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
    return render(request,'contact.html')
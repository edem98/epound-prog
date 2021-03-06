from django import forms
from django.forms import ModelForm
from membre.models import *


class MembreForm(forms.ModelForm):
    """docstring for ReservationOnLineForm"""

    class Meta():
        model = Membre
        fields = '__all__'


class TraderForm(MembreForm):
    pass


class ConsommateurForm(MembreForm):
    pass


class ConsommateurParticulierForm(ConsommateurForm):
    pass


class ConsommateurEntrepriseForm(ConsommateurForm):
    pass


class EntrepriseCommercialeForm(MembreForm):
    class Media:
        js = ('js/jquery-3.2.1.min.js','js/select_filtering.js',)

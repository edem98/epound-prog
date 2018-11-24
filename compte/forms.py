from django import forms
from django.forms import ModelForm
from compte.models import *

class CompteForm(forms.ModelForm):
	"""docstring for ReservationOnLineForm"""

	class Meta():
		model = Compte
		fields = '__all__'

class CompteTraderForm(CompteForm):
	pass

class CompteConsommateurForm(CompteForm):
	pass

class CompteEntrepriseCommercialeForm(CompteForm):
	pass
from django import forms
from django.forms import ModelForm
from emision.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class EmissionForm(forms.ModelForm):
	"""docstring for ReservationOnLineForm"""
	def clean_mdp(self):
		mdp = self.cleaned_data['mdp']
		operateur = self.__dict__['data']['operateur'][0]
		operateur = User.objects.get(id=operateur)
		egaux = check_password(mdp,operateur.password)
		if egaux == False :
			raise ValidationError(('le mot de passe ne correspond pas'))
		return mdp

	class Meta():
		model = EmissionUnites
		fields = '__all__'
		widgets =	{
					'mdp': forms.PasswordInput(),
					}

class EmissionSurCompteAlphaForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_mdp(self):
		password = self.cleaned_data['password']
		utilisateur = self.__dict__['data']['utilisateur'][0]
		utilisateur = User.objects.get(id=utilisateur)
		egaux = check_password(password,utilisateur.password)
		if egaux == False :
			raise ValidationError(('le mot de passe ne correspond pas'))
		return password

	class Meta:
		model = EmissionSurCompteAlpha
		fields = '__all__'

class EmissionSurCompteTraderForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_mdp(self):
		password = self.cleaned_data['password']
		utilisateur = self.__dict__['data']['utilisateur'][0]
		utilisateur = User.objects.get(id=utilisateur)
		egaux = check_password(password,utilisateur.password)
		if egaux == False :
			raise ValidationError(('le mot de passe ne correspond pas'))
		return password

	class Meta:
		model = EmissionSurCompteTrader
		fields = '__all__'

class EmissionSurCompteConsommateurForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_mdp(self):
		password = self.cleaned_data['password']
		trader = self.__dict__['data']['trader'][0]
		trader = Trader.objects.get(id=trader)
		egaux = check_password(password, trader.user.password)
		if egaux == False:
			raise ValidationError(('le mot de passe ne correspond pas'))
		return password

	class Meta:
		model = EmissionSurCompteConsommateur
		fields = '__all__'
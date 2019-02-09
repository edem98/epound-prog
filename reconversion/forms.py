from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from reconversion.models import ReconversionEntrepriseCommerciale, ReconversionConsommateur


class ReconversionEntrepriseCommercialeForm(forms.ModelForm):
	"""docstring for ReservationOnLineForm"""
	def clean_mdp(self):
		mdp = self.cleaned_data['mdp']
		operateur = self.__dict__['data']['operateur'][0]
		operateur = User.objects.get(id=operateur)
		if mdp != operateur.password :
			raise ValidationError(('le mot de passe ne correspond pas'))
		return mdp

	class Meta():
		model = ReconversionEntrepriseCommerciale
		fields = '__all__'
		widgets =	{
					'mot_de_passe': forms.PasswordInput(),
					}

class ReconversionConsommateurForm(forms.ModelForm):
	"""docstring for ReservationOnLineForm"""
	def clean_mdp(self):
		password = self.cleaned_data['mdp']
		operateur = self.__dict__['data']['operateur'][0]
		operateur = User.objects.get(id=operateur)
		egaux = check_password(password, operateur.password)
		if egaux == False:
			raise ValidationError(('le mot de passe ne correspond pas'))
		return password

	class Meta():
		model = ReconversionConsommateur
		fields = '__all__'
		widgets =	{
					'mot_de_passe': forms.PasswordInput(),
					}
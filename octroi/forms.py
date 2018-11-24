from django import forms
from django.forms import ModelForm
from octroi.models import OctroiCredit
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class OctroiCreditForm(forms.ModelForm):
	"""docstring for ReservationOnLineForm"""
	def clean_mot_de_passe(self):
		mot_de_passe = self.cleaned_data['mot_de_passe']
		operateur = self.__dict__['data']['operateur'][0]
		operateur = User.objects.get(id=operateur)
		egaux = check_password(mot_de_passe,operateur.password)
		if egaux == False :
			raise ValidationError(('le mot de passe ne correspond pas'))
		return mot_de_passe

	class Meta():
		model = OctroiCredit
		fields = '__all__'
		widgets =	{
					'mot_de_passe': forms.PasswordInput(),
					}
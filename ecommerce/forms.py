from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from membre.models import ConsommateurParticulier

class LoginForm(forms.Form):
	"""docstring for ReservationOnLineForm"""
	telephone = forms.CharField(label='Telephone', max_length=100,
								widget=forms.TextInput(attrs={
									'class': 'fadeIn second form-control',
									'id': 'login',
									'name': 'telephone',
									'placeholder': 'Téléphone',
								}))
	password = forms.CharField(label='Mot de passe', max_length=100,
								widget=forms.TextInput(attrs={
									'class': 'fadeIn third form-control',
									'id': 'password',
									'name': 'password',
									'placeholder': 'Mot de Passe',
								}))

	def clean_telephone(self):
		telephone = self.cleaned_data['telephone']
		try:
			user = ConsommateurParticulier.objects.get(telephone=telephone)
		except ConsommateurParticulier.DoesNotExist:
			raise ValidationError(("Ce compte n'est pas enregistrer"))
		return telephone

	def clean_password(self):
		password = self.cleaned_data['password']
		if password:
			return password.lower()
		else:
			raise ValidationError(('Votre mot de passe est incorrect'))



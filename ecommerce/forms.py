from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from membre.models import ConsommateurParticulier
from .models import *


class LoginForm(forms.Form):
    """docstring for ReservationOnLineForm"""
    telephone = forms.CharField(label='Telephone', max_length=100,
                                widget=forms.TextInput(attrs={
                                    'class': 'fadeIn second form-control',
                                    'id': 'login',
                                    'name': 'telephone',
                                    'placeholder': 'Téléphone',
                                }))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'fadeIn second form-control',
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
            return password
        else:
            raise ValidationError(('Votre mot de passe est incorrect'))


class AddProductTrocForm(forms.ModelForm):
    class Meta():
        model = ProduitTroc
        fields = [
            'image_produit',
            'nom',
            'prix',
            'premier_produit_souhaite',
            'second_produit_souhaite',
            'dernier_produit_souhaite'
        ]
        widgets = {
            'nom': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_nom',
                }
            ),
            'prix': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_prix',
                }
            ),
            'image_produit': forms.ClearableFileInput(
                attrs={
                    'class': 'custom-file-input',
                    'id': 'id_image_produit',
                    'type': 'file',
                }
            ),
            'premier_produit_souhaite': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_premier_produit_souhaite',
                }
            ),
            'second_produit_souhaite': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_second_produit_souhaite',
                }
            ),
            'dernier_produit_souhaite': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_dernier_produit_souhaite',
                }
            ),
        }

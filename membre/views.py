from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from utils import envoyer_sms
from membre.models import Membre,EntrepriseCommerciale, ConsommateurParticulier


def retourner_taux_membre(request):
	data = {}
	code_membre = request.GET.get('code_membre')
	membre = Membre.objects.get(code_membre = code_membre)
	if 'compte_trader_id' in membre.__dict__:
		taux_gain = membre.compte_trader.taux_gain
		data = {
		'taux': taux_gain,
		}
	elif 'compte_consommateur_id' in membre.__dict__:
		taux_gain = membre.compte_consommateur.taux_gain
		data = {
		'taux': taux_gain,
		}
	return JsonResponse(data)


def retourner_entreprise_info(request):
	data = {}
	id = request.GET.get('id')
	entreprise = EntrepriseCommerciale.objects.get(id = id)
	epounds_dispo = entreprise.compte_entreprise_commercial.compte_business.solde
	data = {
		'epounds_dispo': epounds_dispo,
		}
	return JsonResponse(data)


def retourner_consommateur_info(request):
	id = request.GET.get('id')
	membre = Membre.objects.get(id = id)
	epounds_dispo = membre.compte_consommateur.solde
	data = {
		'epounds_dispo': epounds_dispo,
		}
	return JsonResponse(data)


@csrf_exempt
def generer_mot_de_passe_consommateur(request, id):

	consommateur = ConsommateurParticulier.objects.get(id=id)
	user = consommateur.user
	password = BaseUserManager().make_random_password(4)
	consommateur.mdp = password
	consommateur.save()
	user.set_password(password)
	user.save()
	message = "Votre nouveau mot de passe est: "+ consommateur.mdp
	destinataire = "228" + consommateur.telephone
	try:
		envoyer_sms(message, destinataire)
	except Exception as e:
		print(e)
	finally:
		data = {
			'password': password,
		}
		return JsonResponse(data)

@csrf_exempt
def generer_mot_de_passe_trader(request, id):

	trader = Trader.objects.get(id=id)
	user = trader.user
	password = BaseUserManager().make_random_password(4)
	trader.mdp = password
	trader.save()
	user.set_password(password)
	user.save()
	message = "Votre nouveau mot de passe est: "+ trader.mdp
	destinataire = "228" + trader.telephone
	try:
		envoyer_sms(message, destinataire)
	except Exception as e:
		print(e)
	finally:
		data = {
			'password': password,
		}
		return JsonResponse(data)

@csrf_exempt
def generer_mot_de_passe_vendeur(request, id):

	vendeur = EntrepriseCommerciale.objects.get(id=id)
	user = vendeur.user
	password = BaseUserManager().make_random_password(4)
	vendeur.mdp = password
	vendeur.save()
	user.set_password(password)
	user.save()
	message = "Votre nouveau mot de passe est: "+ vendeur.mdp
	destinataire = "228" + vendeur.telephone
	try:
		envoyer_sms(message, destinataire)
	except Exception as e:
		print(e)
	finally:
		data = {
			'password': password,
		}
		return JsonResponse(data)

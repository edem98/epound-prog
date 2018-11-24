from django.shortcuts import render
from django.http import JsonResponse
from membre.models import Membre,EntrepriseCommerciale

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
	nom_membre = request.GET.get('nom_membre')
	print(nom_membre)
	entreprise = EntrepriseCommerciale.objects.get(id = nom_membre)
	epounds_dispo = entreprise.compte_entreprise_commercial.compte_business.solde
	data = {
		'epounds_dispo': epounds_dispo,
		}
	return JsonResponse(data)


def retourner_consommateur_info(request): 
	data = {}
	code_membre = request.GET.get('code_membre')
	membre = Membre.objects.get(code_membre = code_membre)
	epounds_dispo = membre.compte_consommateur.solde
	data = {
		'epounds_dispo': epounds_dispo,
		}
	return JsonResponse(data)
from django.db import models
from membre.models import *
from django.contrib.auth.models import User
from compte.models import CompteGrenier
from django.contrib.auth.hashers import check_password

class ReconversionEntrepriseCommerciale(models.Model):
	"""
		cette classe permet de vendre des unités e-pounds
		aux traders et aux gros consommateurs
	"""
	operateur = models.ForeignKey(User,
				verbose_name = 'Opérateur',
				on_delete=models.CASCADE,
				related_name ='operateur',
				null = True,
				blank = False)

	beneficiaire = models.ForeignKey(EntrepriseCommerciale,verbose_name = "Bénéficiaire",
									on_delete = models.DO_NOTHING,null = True)
	epounds_disponible = models.PositiveIntegerField(verbose_name = "Recette",null = True)
	epounds_a_reconvertir = models.PositiveIntegerField(verbose_name = "Prélevement",null = True)
	montant_a_prelever = models.PositiveIntegerField(verbose_name = "e-pounds à prélever",null = True)
	montant_en_cfa = models.PositiveIntegerField(verbose_name = "Réglement",null = True)
	montant_virer_sur_compte_conso = models.PositiveIntegerField(verbose_name = "e-pounds à transférer sur le compte e-c",
		null = True)
	mot_de_passe = models.CharField(max_length = 100,verbose_name = "Mot de passe",null = True)

	def save(self, *args, **kwargs):
		if self.mot_de_passe == self.beneficiaire.mdp:
			compte_grenier = CompteGrenier.load()	
			# ajout des 5% du compte buisiness au compte grenier
			self.montant_a_prelever = self.montant_a_reconvertir*0.05
			compte_grenier.solde += self.montant_a_prelever
			compte_grenier.save()
			# retrait des epounds à reconvertir
			compte_entreprise_commercial = self.beneficiaire.compte_entreprise_commercial
			compte_entreprise_commercial.compte_business.solde -= self.epounds_a_reconvertir
			compte_entreprise_commercial.compte_business.save()
			# transfère des 30% après retrait des 5% du compte business sur le compte conso
			self.montant_virer_sur_compte_conso = (self.epounds_a_reconvertir - self.montant_a_prelever)*0.3
			compte_entreprise_commercial.compte_consommateur.solde += self.montant_virer_sur_compte_conso
			compte_entreprise_commercial.compte_consommateur.save()
			# mise a jour du compte de l'entreprise
			compte_entreprise_commercial.save()
			self.montant_en_cfa = (self.epounds_a_reconvertir - self.montant_a_prelever)*0.7
		super(ReconversionEntrepriseCommerciale,self).save(*args, **kwargs)  # On enregistre la nouvelle instance.
		

	class Meta():
		verbose_name = "Reconversion d'unités d'entreprise"
		verbose_name_plural = "Reconversions d'unités d'entreprises"


class ReconversionConsommateur(models.Model):
	"""
		cette classe permet de vendre des unités e-pounds
		aux traders et aux gros consommateurs
	"""
	operateur = models.ForeignKey(User,
				verbose_name = 'Opérateur',
				on_delete=models.CASCADE,
				related_name ='operateur_trader',
				null = True,
				blank = False)

	beneficiaire = models.ForeignKey(Consommateur,verbose_name = "Bénéficiaire",
									on_delete = models.DO_NOTHING,null = True)
	epounds_disponible = models.PositiveIntegerField(verbose_name = "Unités e-pounds disponibles",null = True)
	epounds_a_reconvertir = models.PositiveIntegerField(verbose_name = "Unités e-pounds à reconvertir",
		null = True)
	montant_a_prelever = models.PositiveIntegerField(verbose_name = "e-pounds à prélever",null = True)
	montant_en_cfa = models.PositiveIntegerField(verbose_name = "Montant rendu en cfa",null = True)
	mot_de_passe = models.CharField(max_length = 100,verbose_name = "Mot de passe",null = True)

	def save(self, *args, **kwargs):
		if self.mot_de_passe == self.beneficiaire.mdp:
			compte_grenier = CompteGrenier.load()
			# ajout des 40% du compte consommateur au compte grenier	
			compte_grenier.solde += self.montant_a_prelever
			compte_grenier.save()
			# retrait du montant à reconvertir
			compte_consommateur = self.beneficiaire.compte_consommateur
			compte_consommateur.solde -= self.epounds_a_reconvertir
			compte_consommateur.save() 
		super(ReconversionConsommateur,self).save(*args, **kwargs)  # On enregistre la nouvelle instance.
		

	class Meta():
		verbose_name = "Reconversion d'un Consommateur"
		verbose_name_plural = "Reconversions des Consommateurs"


from django.db import models
from membre.models import *
from django.contrib.auth.models import User
from compte.models import CompteBeta, CompteGrenier
from django.contrib.auth.hashers import check_password
from django.utils import timezone

class OctroiCredit(models.Model):
	"""
		cette classe permet de vendre des unités e-pounds
		aux traders et aux gros consommateurs
	"""
	operateur = models.ForeignKey(User,
				verbose_name = 'Opérateur',
				on_delete=models.CASCADE,
				related_name ='octroyeur',
				null = True,
				blank = False)

	beneficiaire = models.ForeignKey(EntrepriseCommerciale,verbose_name = "Bénéficiaire",
									on_delete = models.DO_NOTHING,null = True)
	montant_pret = models.PositiveIntegerField(verbose_name = "Montant du prêt",null = True)
	montant_prelever_sur_grenier = models.PositiveIntegerField(verbose_name="Montant prélever sur le compte grenier",null=True,editable=False)
	montant_prelever_sur_beta = models.PositiveIntegerField(verbose_name = "Montant à prélever sur le compte bêta",null = True,editable=False)
	delais_rembousement = models.PositiveIntegerField(verbose_name = "Délais de remboursement(nombre de mois)",
		null = True)
	reste = models.PositiveIntegerField(verbose_name = "Reste à rembourser",null = True,editable=True)
	mot_de_passe = models.CharField(max_length = 100,verbose_name = "Mot de passe",null = True)
	date_butoir_payement = models.DateTimeField(verbose_name = "Date butoir du payement",null = True, editable = False)
	date_octroi = models.DateTimeField(verbose_name = "Date d'octroi du crédit",auto_now_add=True)
	reboursser = models.BooleanField(default=False,verbose_name="Octroi rembourser")

	def save(self, *args, **kwargs):
		egaux = check_password(self.mot_de_passe,self.operateur.password)
		if egaux:
			compte_grenier = CompteGrenier.load()
			compte_beta = CompteBeta.load()
			if compte_grenier.recette > self.montant_pret:
				compte_grenier.recette -= self.montant_pret
				compte_grenier.save()
				self.montant_prelever_sur_grenier = self.montant_pret
				self.montant_prelever_sur_beta = 0
				#crédité le compte du beneficiaire
				self.beneficiaire.compte_entreprise_commercial.compte_consommateur.solde += self.montant_pret
				self.beneficiaire.compte_entreprise_commercial.compte_consommateur.save()
			else:
				gap = self.montant_pret - compte_grenier.recette
				# debit du compte grenier
				compte_grenier.recette -= self.montant_pret - gap
				compte_grenier.save()
				self.montant_prelever_sur_grenier = self.montant_pret - gap
				# debit du compte beta
				compte_beta.solde -= gap
				compte_beta.save()
				self.montant_prelever_sur_beta = gap
				# crédité le compte du beneficiaire
				self.beneficiaire.compte_entreprise_commercial.compte_consommateur.solde += self.montant_pret
				self.beneficiaire.compte_entreprise_commercial.compte_consommateur.save()
		#definir la date butoir
		self.date_butoir_payement = timezone.now() + timezone.timedelta(days = self.delais_rembousement*30)
		super(OctroiCredit,self).save(*args, **kwargs)  # On enregistre la nouvelle instance.
		

	class Meta():
		verbose_name = "Octroi de Crédit"
		verbose_name_plural = "Octrois de Crédits"


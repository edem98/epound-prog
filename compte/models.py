from django.db import models
from polymorphic.models import PolymorphicModel
from utils import TimeStamp
from dashboard.models import Creance 
from utils import SingletonModel
import datetime


class CompteAlpha(SingletonModel):
	proprietaire = models.CharField(max_length = 100,verbose_name = "Propriétaire du compte",
									default ='e-pounds Corporation')
	solde = models.PositiveIntegerField(verbose_name = "Solde e-pounds",default = 10000000)

	def __str__(self):
		return "Compte Alpha"

	class Meta():
		verbose_name = "Compte Alpha"
		verbose_name_plural = "Compte Alpha"

class CompteBeta(SingletonModel):
	proprietaire = models.CharField(max_length = 100,verbose_name = "Propriétaire du compte",
									default ='e-pounds Corporation')
	solde = models.PositiveIntegerField(verbose_name = "Solde e-pounds",default = 10000000)

	def __str__(self):
		return "Compte Bêta"

	class Meta():
		verbose_name = "Compte Bêta"
		verbose_name_plural = "Compte Bêta"

class CompteGrenier(SingletonModel):
	fonte = models.PositiveIntegerField(verbose_name="Fonte", null=True)
	prelevement_reconversion = models.PositiveIntegerField(verbose_name="Prélevement sur Reconversion",null=True)
	prelevement_vendeur = models.PositiveIntegerField(verbose_name="Prélevement sur Vendeur", null=True)
	montant_reconverti_local = models.PositiveIntegerField(verbose_name="cumul des 70% des reconversions vendeurs", null=True)
	recette = models.PositiveIntegerField(verbose_name = "Destruction Monaitaire",default = 0)


	def __str__(self):
		return "Compte Grenier"

	class Meta():
		verbose_name = "Compte Grenier"
		verbose_name_plural = "Compte Grenier"
			
class Compte(PolymorphicModel,TimeStamp):
	solde = models.PositiveIntegerField(default = 0)
	date_expiration = models.DateTimeField(verbose_name = "Date d'expiration",
	default = datetime.datetime.now()+ datetime.timedelta(720))
	actif = models.BooleanField(verbose_name = 'En activité',default = True,)

	def __str__(self):
		return "identifiant du compte : "+ str(self.id)

	class Meta():
		verbose_name = "Compte"


class CompteTrader(Compte):
	taux_gain = models.FloatField(verbose_name = "Taux d'intérêt",
											editable = False,default = 1.1)
	class Meta():
		verbose_name = "Compte Trader"

class CompteConsommateur(Compte):
	TAUX_GAIN = 50
	TAUX_PERTE = 40
	TAUX_FONTE_MENSUEL = 2
	
	class Meta():
		verbose_name = "Compte Consommateur"

class CompteBusiness(Compte):
	TAUX_CONTRIBUTION = 5
	TAUX_RECONVERSION = 70
	
	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id != None:
			entreprise = self.compteVente_vers_parent.compteEntreprise_vers_entreprise
			print("Entreprise"+str(entreprise))
			#mise a jour de la Creance
			creance = Creance.objects.get(entreprise_associer = entreprise)
			print(creance)
			creance.epounds_retrancher = (self.solde*5)/100
			creance.voulume_convertible = ((self.solde - creance.epounds_retrancher)*70)/100
			creance.volume_retransferer = ((self.solde - creance.epounds_retrancher)*30)/100
			super(CompteBusiness,self).save(*args, **kwargs)
			creance.save()
		super(CompteBusiness,self).save(*args, **kwargs)

	class Meta():
		verbose_name = 'Compte Vente'

class CompteEntrepriseCommerciale(Compte):
	compte_consommateur = models.OneToOneField(CompteConsommateur,
								verbose_name="Compte Achat",
								on_delete=models.CASCADE,
								related_name = "conso_vers_entreprise")
	compte_business = models.OneToOneField(CompteBusiness,
								verbose_name ="Compte Vente",
								on_delete=models.CASCADE,
								related_name = "vente_vers_entreprise")
	credit = models.PositiveIntegerField(verbose_name ="Credit",default=0)
	TAUX_REMBOURSEMENT = 0

	class Meta():
		verbose_name = "Compte Entreprise Commerciale"
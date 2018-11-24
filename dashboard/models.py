from django.db import models
from django.db.models import Sum
from utils import SingletonModel


class CreanceTotal(SingletonModel):
	total_epounds_consommateur = models.PositiveIntegerField(default=0,verbose_name="Cumul du solde des comptes consommateurs")
	total_epounds = models.PositiveIntegerField(default=0,verbose_name="Cumul du solde des comptes vendeurs")
	epounds_retrancher = models.PositiveIntegerField(verbose_name = "Prélevement reconversion (5%)",default=0)
	voulume_convertible = models.PositiveIntegerField(verbose_name = "Reconversion (70%)",
														default =0)
	volume_retransferer = models.PositiveIntegerField(verbose_name ="epounds retransferés sur les comptes e-c (30%)",
														default = 0)

	class Meta:
		verbose_name = "Creance dûe"
		verbose_name_plural = "Creance dûe"

class Creance(models.Model):

	entreprise_associer = models.OneToOneField('membre.EntrepriseCommerciale',verbose_name="Entreprise associée",
												on_delete = models.CASCADE,null =True,)
	epounds_retrancher = models.PositiveIntegerField(verbose_name = "epounds retranchés",default=0)
	voulume_convertible = models.PositiveIntegerField(verbose_name = "epounds convertibles en monnaie local",
														default =0)
	volume_retransferer = models.PositiveIntegerField(verbose_name ="epounds retransferés sur le comptes e-c",
														default = 0)

	def save(self, *args, **kwargs):
		super(Creance,self).save(*args, **kwargs)
		creance_total = CreanceTotal.load()
		CompteBusiness = type(self.entreprise_associer.compte_entreprise_commercial.compte_business)
		#mon_compte_business = self.entreprise_associer.compte_entreprise_commercial
		total = CompteBusiness.objects.aggregate(cumul = Sum('solde'))
		print(total)
		
		creance_total.total_epounds = total['cumul']
		creance_total.epounds_retrancher = (creance_total.total_epounds * 5)/100
		creance_total.voulume_convertible = ((creance_total.total_epounds - creance_total.epounds_retrancher)*70)/100
		creance_total.volume_retransferer = ((creance_total.total_epounds - creance_total.epounds_retrancher)*30)/100
		
		creance_total.save()

class CreanceMonetaire(SingletonModel):

	cumul_bonification = models.PositiveIntegerField(default=0,verbose_name="Cumul des bonnifications (50%)")
	compte_beta = models.PositiveIntegerField(default=0,verbose_name="Solde du compte bêta")
	compte_grenier = models.PositiveIntegerField(default=0,verbose_name="Solde du compte grenier")
	solde = models.PositiveIntegerField(default=0,verbose_name="Solde")

	def save(self,*args,**kwargs):
		self.solde = self.cumul_bonification+self.compte_beta-self.compte_grenier
		super(CreanceMonetaire,self).save(*args,**kwargs)

	class Meta:
		verbose_name = "Créance Monétaire"
		verbose_name_plural = "Créance Monétaire"

class Remboursement(models.Model):

	entreprise = models.OneToOneField('membre.EntrepriseCommerciale', verbose_name="Entreprise",
											   on_delete=models.CASCADE,null=True,)
	montant_emprunter =  models.PositiveIntegerField(verbose_name="Montant emprunter",null=True,)
	credit_actuel = models.PositiveIntegerField(verbose_name="Crédit actuel",null=True,)
	montant_rembourser = models.PositiveIntegerField(verbose_name="Montant rembouser",null=True,)
	reste = models.PositiveIntegerField(verbose_name="Reste à payer",null=True,)
	date_remboursement = models.DateTimeField(verbose_name="Date de remboursement",auto_now_add=True,)

class IndiceDeConversion(SingletonModel):

	total_reconversion = models.PositiveIntegerField(verbose_name="e-pounds reconverties en monnaie locale",null = True,)
	total_acheter = models.PositiveIntegerField(verbose_name="e-pounds achetés",null=True,)
	taux = models.DecimalField(verbose_name="Indice", max_digits=5, decimal_places=2,null=True,)

	class Meta:
		verbose_name = "Indice de Conversion"
		verbose_name_plural = "Indice de Conversion"

class ConsommationMensuelMoyenneConsommateurActuel(SingletonModel):

	mois = models.CharField(verbose_name="Mois actuel",max_length=50,null=True,)
	epound_utiliser = models.PositiveIntegerField(verbose_name="cumul des unités e-pounds utilisées à la consommation",null=True)
	date_debut_consommation = models.DateField(verbose_name="Début de consommation",null = True,)

	class Meta:
		verbose_name = "Consommation mensuel moyenne actuel des Consommateurs"
		verbose_name_plural = "Consommation mensuel moyenne actuel des Consommateurs"

class ConsommationMensuelMoyenneConsommateur(models.Model):

	mois = models.CharField(verbose_name="Mois",max_length=50,null=True,)
	epound_utiliser = models.PositiveIntegerField(verbose_name="cumul des unités e-pounds utilisées à la consommation", null=True)
	nombre_mois = models.PositiveIntegerField(verbose_name="Nombre de mois",null=True)
	date = models.DateField(verbose_name="Date",auto_now_add=True,null=True,)

	class Meta:
		verbose_name = "Consommation mensuel moyenne des Consommateurs"
		verbose_name_plural = "Consommation mensuel moyenne des Consommateurs"

class ConsommationMensuelMoyenneVendeurActuel(SingletonModel):

	mois = models.CharField(verbose_name="Mois actuel",max_length=50,null=True,)
	epound_utiliser = models.PositiveIntegerField(verbose_name="cumul des unités e-pounds utilisées à la consommation",											  null=True)
	date_debut_consommation = models.DateField(verbose_name="Début de consommation", null=True, )

	class Meta:
		verbose_name = "Consommation mensuel moyenne actuel des Vendeurs"
		verbose_name_plural = "Consommation mensuel moyenne actuel des Vendeurs"

class ConsommationMensuelMoyenneVendeur(models.Model):

	mois = models.CharField(verbose_name="Mois",max_length=50,null=True,)
	epound_utiliser = models.PositiveIntegerField(verbose_name="cumul des unités e-pounds utilisées à la consommation", null=True)
	nombre_mois = models.PositiveIntegerField(verbose_name="Nombre de mois",null=True)
	date = models.DateField(verbose_name="Date",auto_now_add=True,null=True,)

	class Meta:
		verbose_name = "Consommation mensuel moyenne des Vendeurs"
		verbose_name_plural = "Consommation mensuel moyenne des Vendeurs"

class TauxAbsorbtionGlobal(SingletonModel):

	epound_detenus = models.PositiveIntegerField(verbose_name="unités e-ponds détenues par l’ensemble des consommateurs",null=True)
	epound_consommer = models.PositiveIntegerField(verbose_name="unités e-pounds utilisées à la consommation au cours du mois",null=True)
	mois = models.CharField(max_length=30,verbose_name="Mois",null=True,)

	class Meta:
		verbose_name = "Taux d'absorbtion global"
		verbose_name_plural = "Taux d'absorbtion global"

class TauxAbsorbtionGlobalMensuel(models.Model):

	epound_detenus = models.PositiveIntegerField(
		verbose_name="unités e-ponds détenues par l’ensemble des consommateurs", null=True)
	epound_consommer = models.PositiveIntegerField(
		verbose_name="unités e-pounds utilisées à la consommation au cours du mois", null=True)
	mois = models.CharField(max_length=30, verbose_name="Mois", null=True, )
	date = models.DateField(auto_now_add=True,null=True)

	class Meta:
		verbose_name = "Taux d'absorbtion mensuel"
		verbose_name_plural = "Taux d'absorbtion mensuel"

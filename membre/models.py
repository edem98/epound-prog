from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User, Group
from polymorphic.models import PolymorphicModel
from compte.models import CompteTrader,CompteConsommateur,CompteEntrepriseCommerciale
from utils import TimeStamp
import datetime
from dashboard.models import Creance
from django.contrib.auth.hashers import make_password

class Membre(PolymorphicModel,TimeStamp):
	user = models.OneToOneField(User,on_delete=models.CASCADE,null = True,blank = True)
	nom = models.CharField(max_length = 100,verbose_name = 'Nom',null = True,)
	code_membre = models.PositiveIntegerField(unique = True,verbose_name ='Code membre',null = True,)
	mdp = models.CharField(max_length = 80, verbose_name ='Mot de passe',null = True)
	telephone = models.CharField(max_length =8,verbose_name ="Téléphone",null = True)
	email = models.EmailField(max_length = 254,null = True)
	date_expiration = models.DateTimeField(verbose_name = "Date d'expiration",
	default = datetime.datetime.now()+ datetime.timedelta(720))
	actif = models.BooleanField(verbose_name = 'En activité',default = True,)

	def __str__(self):
		return str(self.nom)
	

class Trader(Membre):
	"""
		La classe Trader gère les membres qui ont 
		la fonction de grossiste. Ils peuvent soit 
		être des personnes moraux ou des personnes
		physiques et dispose d'un taux d'interêt de 10%
	"""
	feminin = 'Féminin'
	masculin = 'Masculin'

	liste_sexe = [
		(feminin, 'Féminin'),
		(masculin, 'Masculin'),
	]

	sexe = models.CharField(max_length = 50,
					choices=liste_sexe,
					default=feminin, null = True,verbose_name="Sexe")

	ville_residence = models.CharField(max_length = 150, verbose_name = 'Ville de résidence', null = True)
	# ajout du prénoms au cas ou la personne serait physique
	prenoms = models.CharField(max_length = 150, verbose_name = 'Prénoms', null = True)

	emplacement = models.CharField(max_length=200, verbose_name="Emplacement du Trader", null=True, )
	
	#Compte trader associer
	compte_trader = models.OneToOneField(CompteTrader,on_delete = models.CASCADE,
										verbose_name = 'Compte e-T',null = True)

	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id == None:
			super(Trader,self).save(*args, **kwargs)
			self.code_membre = self.id
			self.user = User(username = str(self.nom)+"-"+str(self.code_membre),
							last_name = str(self.nom),password = make_password(self.mdp))
			self.user.save()
			groupe = Group.objects.get(name="Trader")	
			groupe.user_set.add(self.user)
			self.save(update_fields=['code_membre','compte_trader','user'])
		else:
			return super(Trader,self).save(*args, **kwargs)
	
class Consommateur(Membre,PolymorphicModel):
	"""
		La classe consommateur gère les membres classiques.
		Ils peuvent soit être des personnes moraux ou 
		des personnes physiques. Ils disposent d'un taux de 
		bonnification à l'achat de 50% et d'un taux de perte
		à la reconversion de 40%
	"""

	#definition des pays
	togo = 'TOGO' 
	benin = 'BENIN'
	ghana = 'GHANA'
	feminin = 'Féminin'
	masculin = 'Masculin'

	liste_pays = [
		(togo, 'TOGO'),
		(benin, 'BENIN'),
		(ghana, 'GHANA'),
	]

	liste_sexe = [
		(feminin, 'Féminin'),
		(masculin, 'Masculin'),
	]

	sexe = models.CharField(max_length = 50,
					choices=liste_sexe,
					default=feminin, null = True,verbose_name="Sexe")

	ville_residence = models.CharField(max_length = 150, verbose_name = 'Ville de résidence', null = True)

	nationalite = models.CharField(max_length = 50,
					choices=liste_pays,
					default=togo, null = True,verbose_name="Pays")
	#compte consommateur
	compte_consommateur = models.OneToOneField(CompteConsommateur,on_delete = models.CASCADE,
										verbose_name = 'Compte e-C',null = True)
	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id == None:
			super(Consommateur,self).save(*args, **kwargs)
			self.code_membre = self.id
			self.user = User.objects.create(username = self.telephone+"-"+str(self.code_membre)
							,password = make_password(self.mdp))
			self.compte_consommateur = CompteConsommateur.objects.create()
			groupe = Group.objects.get(name="Consommateur")	
			groupe.user_set.add(self.user)
			self.save(update_fields=['code_membre','compte_consommateur','user'])
		else:
			return super(Consommateur,self).save(*args, **kwargs)

class ConsommateurParticulier(Consommateur):
	#definition de la situation matrimonial
	celibataire = 'Célibataire' 
	marier = 'Marié'

	situation = [
		(celibataire, 'Célibataire'),
		(marier, 'Marié'),
	]

	# ajout du prénoms au cas ou la personne serait physique
	prenoms = models.CharField(max_length = 150, verbose_name = 'Prénoms', null = True)
	# informations supplementaire pour les particuliers
	date_naissance = models.DateField(verbose_name="Date de naissance", null = True)
	lieu_residence = models.CharField(max_length=150,verbose_name="Lieu de résidence", null = True)
	num_carte = models.CharField(max_length=12,verbose_name="Numéro de carte d'indentité", null = True)
	formation = models.CharField(max_length=100,verbose_name="Formation", null = True)
	profession = models.CharField(max_length=100,verbose_name="Profession", null = True)
	situation_matrimoniale = models.CharField(max_length = 50,
					choices=situation,
					default=celibataire, null = True)

	class Meta:
		verbose_name = "Particulier"
		verbose_name_plural = "Particuliers"

	def __str__(self):
		return str(self.nom)+" "+str(self.prenoms)
		
class ConsommateurEntreprise(Consommateur):


	raison_social = models.CharField(max_length = 100,verbose_name = 'Raison sociale', null = True)
	statut_juridique = models.CharField(max_length = 100,verbose_name = 'Statut juridique', null = True)
	objet_social = models.CharField(max_length = 100,verbose_name = 'Objet sociale', null = True)
	capital_social = models.PositiveIntegerField(verbose_name = 'Caplital sociale', null = True)
	numero_rccm = models.CharField(max_length = 100,verbose_name = 'Numéro RCCM', null = True)
	regime_fiscal = models.CharField(max_length = 100,verbose_name = 'Régime fiscal', null = True)
	nif = models.CharField(max_length = 100,verbose_name = 'NIF', null = True)
	siege_social = models.CharField(max_length = 100,verbose_name = 'Siège sociale', null = True)
	numero_compte_bancaire = models.CharField(max_length = 100,verbose_name = 'Numéro de compte bancaire', null = True)
	responsable = models.CharField(max_length = 100,verbose_name = 'Responsable', null = True)


	def __str__(self):
		return str(self.raison_social)

	class Meta:
		verbose_name = "Entreprise"
		verbose_name_plural = "Entreprises"

class EntrepriseCommerciale(Membre):

	"""
		Cette classe gère les entreprises commerciales
		partenaires de Epound.Ce sont les vendeurs ou Offreurs
		de biens et de services sur le réseau ; offrant leurs
		produits contre les unités e-pounds des Consommateurs.
		Elles disposent franchise leur donne droit à 
		l’obtention d’un compte e-b, d’un compte e-c.
		avec un taux de contribution mensuel de 5%
	"""
	es = 'es'
	em = 'em'
	snc = 'SNC'
	scs = 'SCS'
	sarl ='SARL'
	sa = 'SA'
	sep = 'SEP'
	spas = 'SPAS'
	anonyme = 'Société anonyme'

	type = [
		(es, 'es'),
		(em, 'em'),
	]

	nature = [
		(etablissement, 'Etablissement'),
		(snc, 'SNC'),
		(scs, 'SCS'),
		(sarl, 'SARL'),
		(sarl, 'SARL'),
		(sarl, 'SARL'),
		(sarl, 'SARL'),
		(anonyme, 'Société anonyme'),
	]

	besoin_fondamental = models.ForeignKey('ecommerce.ExpressionBesoin', on_delete=models.CASCADE,
									verbose_name="Domaine d'activité",
									null=True,
									blank=True,
									)

	besoin_gere = models.ForeignKey('ecommerce.SpécificationBesoin',on_delete = models.CASCADE,
									verbose_name = "Domaine d'activité",
									null = True,
									blank = True,
									)

	compte_entreprise_commercial = models.OneToOneField(CompteEntrepriseCommerciale,
									on_delete = models.CASCADE,
									verbose_name = 'Compte e-B',
									related_name = 'compteEntreprise_vers_entreprise',
									null = True)
	emplacement = models.CharField(max_length =200, verbose_name="Emplacement du Vendeur",null=True,)
	slug = models.SlugField(verbose_name="Etiquette",null=True,max_length=80)
	banniere_principal = models.ImageField(upload_to='banniere principal/', null=True, blank=True)
	banniere_secondaire = models.ImageField(upload_to='banniere secondaire/', null=True, blank=True)
	banniere_trois = models.ImageField(upload_to='banniere trois/', null=True, blank=True)
	banniere_quatre = models.ImageField(upload_to='banniere quatre/', null=True, blank=True)
	banniere_cinq = models.ImageField(upload_to='banniere cinq/', null=True, blank=True)
	type_market = models.CharField(max_length = 50,choices=type,default=es, null = True)
	nature_jurique = models.CharField(max_length = 150,choices=nature,default=snc, null = True)
	numero_rccm = models.CharField(max_length=100, verbose_name='Numéro RCCM', null=True)
	regime_fiscal = models.CharField(max_length=100, verbose_name='Régime fiscal', null=True)
	nif = models.CharField(max_length=100, verbose_name='NIF', null=True)
	siege_social = models.CharField(max_length=100, verbose_name='Siège sociale', null=True)
	numero_cnss = models.CharField(max_length=100, verbose_name='Numéro de CNSS', null=True)
	responsable = models.CharField(max_length=100, verbose_name='Nom et Prénoms du Responsable', null=True)


	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id == None:
			super(EntrepriseCommerciale,self).save(*args, **kwargs)
			self.code_membre = self.id
			creance = Creance.objects.create(entreprise_associer = self)
			creance.save()
			self.user = User(username = str(self.nom)+"-"+str(self.code_membre),
							last_name = str(self.nom),password = make_password(self.mdp))
			self.user.save()
			groupe = Group.objects.get(name="Commercial")	
			groupe.user_set.add(self.user)
			self.save(update_fields=['code_membre','compte_entreprise_commercial','user'])
		else:
			return super(EntrepriseCommerciale,self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		#suppression du compte associér a ce vendeur
		self.compte_entreprise_commercial.delete()
		super(EntrepriseCommerciale,self).delete(*args, **kwargs)

	
	def __str__(self):
		return str(self.nom)
	class Meta:
		verbose_name = "Vendeur"
		verbose_name_plural = "Vendeurs"


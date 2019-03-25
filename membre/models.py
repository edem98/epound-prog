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
	code_membre = models.CharField(max_length=50,unique = True,verbose_name ='Code membre',null = True,blank =True)
	mdp = models.CharField(max_length = 80, verbose_name ='Mot de passe',null = True)
	telephone = models.CharField(max_length =8,verbose_name ="Téléphone",null = True,unique = True)
	email = models.EmailField(max_length = 254,null = True,unique = True)
	date_desactivation = models.DateField(verbose_name="Date de desactivation", null=True, blank=True)
	date_expiration = models.DateField(verbose_name = "Date d'expiration",null = True,blank =True)
	actif = models.BooleanField(verbose_name = 'En activité',default = True,)

	def __str__(self):
		return str(self.code_membre)

	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id == None:
			super(Membre,self).save(*args, **kwargs)
			self.date_expiration = self.date_add.date() + datetime.timedelta(720)
			self.date_desactivation = self.date_add.date() + datetime.timedelta(360)
			self.save(update_fields=['date_expiration',])
		else:
			return super(Membre,self).save(*args, **kwargs)
	
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
					default=feminin, null = True,verbose_name="Sexe",blank =True)

	ville_residence = models.CharField(max_length = 150, verbose_name = 'Ville de résidence', null = True,blank =True)

	nationalite = models.CharField(max_length = 50,
					choices=liste_pays,
					default=togo, null = True,verbose_name="Pays",blank =True)
	#compte consommateur
	compte_consommateur = models.OneToOneField(CompteConsommateur,on_delete = models.CASCADE,
										verbose_name = 'Compte e-C',null = True)
	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id == None:
			super(Consommateur,self).save(*args, **kwargs)
			self.code_membre = self.id
			self.user = User.objects.create(username = self.telephone+"_"+str(self.code_membre)
							,password = make_password(self.mdp))
			self.compte_consommateur = CompteConsommateur.objects.create()
			groupe = Group.objects.get(name="Consommateur")	
			groupe.user_set.add(self.user)
			self.save(update_fields=['code_membre','compte_consommateur','user'])
		else:
			return super(Consommateur,self).save(*args, **kwargs)

	def __str__(self):
		return self.nom

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
	date_naissance = models.DateField(verbose_name="Date de naissance", null = True,blank =True)
	lieu_residence = models.CharField(max_length=150,verbose_name="Lieu de résidence", null = True,blank =True)
	num_carte = models.CharField(max_length=12,verbose_name="Numéro de carte d'indentité", null = True,unique=True)
	formation = models.CharField(max_length=100,verbose_name="Formation", null = True,blank =True)
	profession = models.CharField(max_length=100,verbose_name="Profession", null = True,blank =True)
	situation_matrimoniale = models.CharField(max_length = 50,
					choices=situation,
					default=celibataire, null = True,blank =True)

	class Meta:
		verbose_name = "Particulier"
		verbose_name_plural = "Particuliers"

	def __str__(self):
		return str(self.nom)+" "+str(self.prenoms)
		
class ConsommateurEntreprise(Consommateur):


	raison_social = models.CharField(max_length = 100,verbose_name = 'Raison sociale', null = True)
	statut_juridique = models.CharField(max_length = 100,verbose_name = 'Statut juridique', null = True)
	objet_social = models.CharField(max_length = 100,verbose_name = 'Objet sociale', null = True,blank =True)
	capital_social = models.PositiveIntegerField(verbose_name = 'Caplital sociale', null = True,blank =True)
	numero_rccm = models.CharField(max_length = 100,verbose_name = 'Numéro RCCM', null = True,blank =True)
	regime_fiscal = models.CharField(max_length = 100,verbose_name = 'Régime fiscal', null = True,blank =True)
	nif = models.CharField(max_length = 100,verbose_name = 'NIF', null = True,blank =True)
	siege_social = models.CharField(max_length = 100,verbose_name = 'Siège sociale', null = True)
	numero_compte_bancaire = models.CharField(max_length = 100,verbose_name = 'Numéro de compte bancaire', null = True,blank =True)
	responsable = models.CharField(max_length = 100,verbose_name = 'Responsable', null = True)


	def __str__(self):
		return str(self.raison_social)

	class Meta:
		verbose_name = "Entreprise"
		verbose_name_plural = "Entreprises"

class Partenaire(models.Model):
	"""
	classe gerant les partennaire de epound
	"""
	nom = models.CharField(max_length=200,verbose_name="Nom du partenaire",null = True)
	logo = models.ImageField(upload_to='logo_partenaire/', null=True, blank=True)

class Ville(TimeStamp):
	"""
	Ville oû epound corpoation est en activite
	"""
	nom = models.CharField(max_length = 100,verbose_name = 'Nom de la ville',null = True,)

	def __str__(self):
		return self.nom

class Quartier(TimeStamp):
	"""
	Ville oû epound corpoation est en activite
	"""
	ville = models.ForeignKey(Ville,on_delete=models.CASCADE,related_name="ville_appartenance",null=True)
	nom = models.CharField(max_length = 100,verbose_name = 'Nom du quartier',null = True,)

	def __str__(self):
		return self.nom

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
	etablissement = 'Etablissement'
	es = 'es'
	em = 'em'
	snc = 'SNC'
	scs = 'SCS'
	sarl = 'SARL'
	sa = 'SA'
	sep = 'SEP'
	spas = 'SPAS'

	type = [
		(es, 'es'),
		(em, 'em'),
	]

	nature = [
		(etablissement, 'Etablissement'),
		(snc, 'SNC'),
		(scs, 'SCS'),
		(sa, 'SA'),
		(sarl, 'SARL'),
		(sep, 'SEP'),
		(spas, 'SPAS'),
	]

	besoin_fondamental = models.ForeignKey('ecommerce.ExpressionBesoin', on_delete=models.CASCADE,
										   verbose_name="Domaine d'activité",
										   null=True,
										   blank=True,
										   )

	besoin_gere = models.ForeignKey('ecommerce.SpécificationBesoin', on_delete=models.CASCADE,
									verbose_name="Sous domaine d'activité",
									null=True,
									blank=True,
									)

	compte_entreprise_commercial = models.OneToOneField(CompteEntrepriseCommerciale,
														on_delete=models.CASCADE,
														verbose_name='Compte e-B',
														related_name='compteEntreprise_vers_entreprise',
														null=True
														)

	objet_social = models.TextField(verbose_name="Objet social", null=True, blank=True, )
	emplacement = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name="quartier_entreprise", null=True)
	slug = models.SlugField(verbose_name="Etiquette", null=True, max_length=80)
	banniere_principal = models.ImageField(upload_to='banniere principal/', null=True, blank=True)
	banniere_secondaire = models.ImageField(upload_to='banniere secondaire/', null=True, blank=True)
	banniere_trois = models.ImageField(upload_to='banniere trois/', null=True, blank=True)
	banniere_quatre = models.ImageField(upload_to='banniere quatre/', null=True, blank=True)
	banniere_cinq = models.ImageField(upload_to='banniere cinq/', null=True, blank=True)
	type_market = models.CharField(max_length=50, choices=type, default=es, null=True)
	nature_jurique = models.CharField(max_length=150, choices=nature, default=snc, null=True, blank=True)
	numero_rccm = models.CharField(max_length=100, verbose_name='Numéro RCCM', null=True, blank=True)
	regime_fiscal = models.CharField(max_length=100, verbose_name='Régime fiscal', null=True, blank=True)
	nif = models.CharField(max_length=100, verbose_name='NIF', null=True, blank=True)
	num_cfe = models.CharField(max_length=100, verbose_name='Numéro CFE', null=True, blank=True)
	date_creation = models.DateField(max_length=100, verbose_name='Date Création', null=True, blank=True)
	siege_social = models.CharField(max_length=100, verbose_name='Siège sociale', null=True, blank=True)
	numero_cnss = models.CharField(max_length=100, verbose_name='Numéro de CNSS', null=True, blank=True)
	responsable = models.CharField(max_length=100, verbose_name='Nom et Prénoms du Responsable', null=True)
	contact_1 = models.CharField(max_length=8, verbose_name="Contact 1", null=True, blank=True)
	contact_2 = models.CharField(max_length=8, verbose_name="Contact 2", null=True, blank=True)

	def save(self, *args, **kwargs):
		# recuperation de l'entreprise associér a ce compte
		if self.id == None:

			self.user = User(username=str(self.nom) + "-" + str(self.code_membre),
							 last_name=str(self.nom), password=make_password(self.mdp))
			self.user.save()
			groupe = Group.objects.get(name="Commercial")
			groupe.user_set.add(self.user)
			super(EntrepriseCommerciale, self).save(*args, **kwargs)
			self.code_membre = self.id
			creance = Creance.objects.create(entreprise_associer=self)
			creance.save()
			super(EntrepriseCommerciale, self).save(*args, **kwargs)
		else:
			print(str(self.id)+"------------------------------------------------------------------")
			# mise a jour de la Creance
			creance = Creance.objects.get(entreprise_associer=self)
			creance.epounds_retrancher = (self.compte_entreprise_commercial.compte_business.solde * 5) / 100
			creance.voulume_convertible = ((self.compte_entreprise_commercial.compte_business.solde - creance.epounds_retrancher) * 70) / 100
			creance.volume_retransferer = ((self.compte_entreprise_commercial.compte_business.solde - creance.epounds_retrancher) * 30) / 100
			creance.save()
			return super(EntrepriseCommerciale, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		# suppression du compte associér a ce vendeur
		self.compte_entreprise_commercial.delete()
		super(EntrepriseCommerciale, self).delete(*args, **kwargs)

	def __str__(self):
		return str(self.nom)

	class Meta:
		verbose_name = "Vendeur"
		verbose_name_plural = "Vendeurs"

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

	emplacement = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name="quartier_trader", null=True)

	sexe = models.CharField(max_length = 50,
					choices=liste_sexe,
					default=feminin, null = True,verbose_name="Sexe",blank =True)

	ville_residence = models.CharField(max_length = 150, verbose_name = 'Ville de résidence', null = True,blank =True)
	# ajout du prénoms au cas ou la personne serait physique
	prenoms = models.CharField(max_length = 150, verbose_name = 'Prénoms', null = True)


	#Compte trader associer
	compte_trader = models.OneToOneField(CompteTrader,on_delete = models.CASCADE,
										verbose_name = 'Compte e-T',null = True)

	def save(self, *args, **kwargs):
		#recuperation de l'entreprise associér a ce compte
		if self.id == None:
			super(Trader,self).save(*args, **kwargs)
			self.code_membre = self.id
			self.user = User(username = str(self.nom)+"_"+str(self.code_membre),
							last_name = str(self.nom),password = make_password(self.mdp))
			self.user.save()
			groupe = Group.objects.get(name="Trader")
			groupe.user_set.add(self.user)
			self.save(update_fields=['code_membre','compte_trader','user'])
		else:
			return super(Trader,self).save(*args, **kwargs)
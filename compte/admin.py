from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from compte.models import *
from compte.forms import *
from membre.models import EntrepriseCommerciale,Consommateur,Trader

@admin.register(Compte)
class CompteAdmin(PolymorphicParentModelAdmin):
	base_model =  Compte 
	child_models = (CompteTrader, CompteConsommateur, CompteEntrepriseCommerciale)
	list_filter = (PolymorphicChildModelFilter,)
	list_display = ['titulaire','solde','date_expiration','polymorphic_ctype_id']

	def titulaire(self,obj):
		if obj.polymorphic_ctype_id == 13:
			try:
				compte_entreprise = CompteEntrepriseCommerciale.objects.get( id = obj.id)
				entreprise = compte_entreprise.compteEntreprise_vers_entreprise
				return entreprise.nom
			except Exception as e:
				print(e)
		elif obj.polymorphic_ctype_id == 12:
			try:
				compte_conso = CompteConsommateur.objects.get(id = obj.id)
				entreprise = compte_conso.conso_vers_entreprise.compteEntreprise_vers_entreprise
				print(entreprise.nom)
				return entreprise.nom
			except Exception as e:
				print(e)
			consommateur = Consommateur.objects.get(compte_consommateur = obj)
			if 'numero_rccm' in consommateur.__dict__ :
				return str(consommateur.raison_social)
			elif 'prenoms' in consommateur.__dict__:
				return str(consommateur.nom)+" "+str(consommateur.prenoms)
		elif obj.polymorphic_ctype_id == 11:
			compte_vente = CompteBusiness.objects.get(id = obj.id)
			entreprise = compte_vente.vente_vers_entreprise.compteEntreprise_vers_entreprise
			return entreprise.nom
		elif obj.polymorphic_ctype_id == 14:
			compte_trader = CompteTrader.objects.get(id = obj.id)
			trader = Trader.objects.get(compte_trader = compte_trader)
			if trader.prenoms != "":
				return trader.nom+ " "+trader.prenoms
			else:
				return trader.nom
		else:
			return "En recherche"
	titulaire.short_description = "Titulaire du Compte"

@admin.register(CompteTrader)
class CompteTraderAdmin(PolymorphicChildModelAdmin):
	base_model = CompteTrader
	search_fields = ['date_expiration']
	list_display = ['titulaire','solde','date_expiration',]

	def titulaire(self,obj):
		compte_trader = CompteTrader.objects.get(id = obj.id)
		trader = Trader.objects.get(compte_trader = compte_trader)
		if trader.prenoms != "":
			return trader.nom+ " "+trader.prenoms
		else:
			return trader.nom
		
	titulaire.short_description = "Titulaire du Compte"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = CompteTraderForm
		return super().get_form(request, obj, **kwargs)

	def renitialiser_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(solde=0)
		if compte_mise_a_jour == 1:
			message_bit = "Le solde du compte sélectionner a été mis à zéro"
		else:
			message_bit = "le solde de %s comptes ont été mis à zéro." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	renitialiser_compte.short_description = "changer le status des voitures en : Louer"

	def desactiver_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(actif=False)
		if compte_mise_a_jour == 1:
			message_bit = "Le compte sélectionner a été désactiver"
		else:
			message_bit = "Les %s comptes sélectionnées ont été désactivés." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	desactiver_compte.short_description = "Désactiver les comptes"

	def activer_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(actif=False)
		if compte_mise_a_jour == 1:
			message_bit = "Le compte sélectionner a été activer"
		else:
			message_bit = "Les %s comptes sélectionnées ont été activés." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	activer_compte.short_description = "Activer les comptes"

	actions = [renitialiser_compte,desactiver_compte,activer_compte]

@admin.register(CompteConsommateur)
class CompteConsommateurAdmin(PolymorphicChildModelAdmin):
	base_model = CompteConsommateur
	search_fields = ['date_expiration','depense_epound_mensuel']
	list_display = ['titulaire','solde','depense_epound_mensuel','date_expiration',]

	def titulaire(self,obj):
		try:
			entreprise = obj.conso_vers_entreprise.compteEntreprise_vers_entreprise
			return entreprise.nom
		except Exception as e:
			pass
		consommateur = Consommateur.objects.get(compte_consommateur = obj)
		if "raison_social" in consommateur.__dict__ :
			return consommateur.raison_social
		else:
			return str(consommateur.nom) +" "+ str(consommateur.prenoms)
	
	titulaire.short_description = "Titulaire du Compte"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = CompteConsommateurForm
		return super().get_form(request, obj, **kwargs)

	def renitialiser_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(solde=0)
		if compte_mise_a_jour == 1:
			message_bit = "Le solde du compte sélectionner a été mis à zéro"
		else:
			message_bit = "le solde de %s comptes ont été mis à zéro." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	renitialiser_compte.short_description = "Mettre a zéro le solde"

	def desactiver_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(actif=False)
		if compte_mise_a_jour == 1:
			message_bit = "Le compte sélectionner a été désactiver"
		else:
			message_bit = "Les %s comptes sélectionnées ont été désactivés." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	desactiver_compte.short_description = "Désactiver les comptes"

	def activer_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(actif=False)
		if compte_mise_a_jour == 1:
			message_bit = "Le compte sélectionner a été activer"
		else:
			message_bit = "Les %s comptes sélectionnées ont été activés." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	activer_compte.short_description = "Activer les comptes"

	actions = [renitialiser_compte,desactiver_compte,activer_compte]

@admin.register(CompteBusiness)
class CompteBusinessAdmin(PolymorphicChildModelAdmin):
	base_model = CompteBusiness
	search_fields = ['date_expiration']
	list_display = ['titulaire','solde','date_expiration',]

	def titulaire(self,obj):
		compte_vente = CompteBusiness.objects.get(id = obj.id)
		entreprise = compte_vente.vente_vers_entreprise.compteEntreprise_vers_entreprise
		print(str(entreprise))
		return entreprise.nom
	titulaire.short_description = "Titulaire du Compte"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = CompteConsommateurForm
		return super().get_form(request, obj, **kwargs)

	def renitialiser_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(solde=0)
		if compte_mise_a_jour == 1:
			message_bit = "Le solde du compte sélectionner a été mis à zéro"
		else:
			message_bit = "le solde de %s comptes ont été mis à zéro." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	renitialiser_compte.short_description = "Mettre a zéro le solde"

	def desactiver_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(actif=False)
		if compte_mise_a_jour == 1:
			message_bit = "Le compte sélectionner a été désactiver"
		else:
			message_bit = "Les %s comptes sélectionnées ont été désactivés." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	desactiver_compte.short_description = "Désactiver les comptes"

	def activer_compte(self, request, queryset):
		compte_mise_a_jour = queryset.update(actif=False)
		if compte_mise_a_jour == 1:
			message_bit = "Le compte sélectionner a été activer"
		else:
			message_bit = "Les %s comptes sélectionnées ont été activés." % compte_mise_a_jour
		self.message_user(request, "%s " % message_bit)

	activer_compte.short_description = "Activer les comptes"

	actions = [renitialiser_compte,desactiver_compte,activer_compte]

@admin.register(CompteEntrepriseCommerciale)
class CompteEntrepriseCommercialeAdmin(PolymorphicChildModelAdmin):
	base_model = CompteEntrepriseCommerciale
	search_fields = ['date_expiration','taux_rembourssement',]
	list_display = ["titulaire",'compte_consommateur_solde',
					'compte_business_solde','date_expiration','credit']

	def titulaire(self,obj):
		entreprise = obj.compteEntreprise_vers_entreprise
		return entreprise.nom
		titulaire.short_description = "Titulaire du Compte"

	def compte_consommateur_solde(self,obj):
		return str(obj.compte_consommateur.solde)
	compte_consommateur_solde.short_description = "solde du compte consommateur"

	def compte_business_solde(self,obj):
		return str(obj.compte_business.solde)
	compte_business_solde.short_description = "solde du compte business"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = CompteEntrepriseCommercialeForm
		return super().get_form(request, obj, **kwargs)

	def supprimer_compte(self, request, queryset):
		queryset.delete()
		message_bit = "Les comptes sélectionnées ont été supprimer."
		self.message_user(request, "%s " % message_bit)

	supprimer_compte.short_description = "Supprimer les comptes"

	actions = [supprimer_compte,]

@admin.register(CompteAlpha)
class CompteAlphaAdmin(admin.ModelAdmin):
	list_display = ['proprietaire','solde',]
	readonly_fields = ['proprietaire','solde',]

	def has_add_permission(self,request):
		return False

@admin.register(CompteGrenier)
class CompteGrenierAdmin(admin.ModelAdmin):
	list_display = ['fonte','prelevement_reconversion','prelevement_vendeur',]
	readonly_fields = ['fonte','prelevement_reconversion','prelevement_vendeur','recette']

	def has_add_permission(self,request):
		return False

@admin.register(CompteBeta)
class CompteBetaAdmin(admin.ModelAdmin):
	list_display = ['proprietaire','solde',]
	readonly_fields = ['proprietaire','solde',]

	def has_add_permission(self,request):
		return False
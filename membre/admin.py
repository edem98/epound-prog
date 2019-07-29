from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from membre.models import *
from membre.forms import *


@admin.register(Membre)
class MembreAdmin(PolymorphicParentModelAdmin):
	base_model = Membre
	child_models = (EntrepriseCommerciale, Trader, ConsommateurParticulier, ConsommateurEntreprise)
	list_filter = (PolymorphicChildModelFilter, 'date_expiration', 'actif',)
	search_fields = ['nom', 'code_membre', 'actif', ]
	list_display = ['nom_membre', 'code_membre', 'date_expiration', ]

	def nom_membre(self, obj):
		membre = Membre.objects.get(id=obj.id)
		if "prenoms" in membre.__dict__:
			return str(membre.nom) + " " + str(membre.prenoms)
		elif "raison_social" in membre.__dict__:
			return membre.raison_social
		else:
			return membre.nom

	nom_membre.short_description = "Utilisateur"

	def desactiver_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "L' utilisateur  sélectionner a été désactiver"
		else:
			message_bit = "Les %s utilisateurs sélectionnées ont été désactivés." % users
		self.message_user(request, "%s " % message_bit)

	desactiver_membre.short_description = "Désactiver les Utilisateurs"

	def activer_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "L'utilisateur sélectionner a été activer"
		else:
			message_bit = "Les %s utilisateurs sélectionnées ont été activés." % users
		self.message_user(request, "%s " % message_bit)

	activer_membre.short_description = "Activer les Utilisateurs"

	actions = [desactiver_membre, activer_membre]


@admin.register(Trader)
class TraderAdmin(PolymorphicChildModelAdmin):
	base_model = Trader
	search_fields = ['nom', 'choix_personne', 'actif', ]
	list_display = ['nom_membre', 'code_membre', 'date_expiration']
	readonly_fields = ['numero_compte_trader', 'solde_compte_trader',
					   'date_expiration_compte_trader', 'activiter_compte_trader', ]
	fieldsets = (
		('Informations Relatifs au Trader', {
			'fields': (
				'user', 'code_membre', 'nom', 'prenoms', 'mdp',  'code_qr', 'telephone', 'email', 'emplacement', 'date_expiration',
				'actif')
		}),
		('Informations Relatifs au Compte e-T', {
			'fields': ('compte_trader', 'numero_compte_trader', 'solde_compte_trader',
					   'date_expiration_compte_trader', 'activiter_compte_trader',),
		}),
	)

	def solde_compte_trader(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_trader.solde)

	solde_compte_trader.short_description = "Solde du compte"

	def numero_compte_trader(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_trader.id)

	numero_compte_trader.short_description = "Identifiant du compte"

	def date_expiration_compte_trader(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_trader.date_expiration)

	date_expiration_compte_trader.short_description = "Date d'expiration"

	def activiter_compte_trader(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_trader.actif)

	activiter_compte_trader.short_description = "En activité"

	def nom_membre(self, obj):
		membre = Membre.objects.get(id=obj.id)
		if "prenoms" in membre.__dict__:
			return membre.nom + " " + str(membre.prenoms)
		else:
			return membre.nom

	nom_membre.short_description = "membre"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = TraderForm
		return super().get_form(request, obj, **kwargs)

	def desactiver_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "Le Trader  sélectionner a été désactiver"
		else:
			message_bit = "Les %s Traders sélectionnées ont été désactivés." % users
		self.message_user(request, "%s " % message_bit)

	desactiver_membre.short_description = "Désactiver les Traders"

	def activer_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "Le Trader sélectionner a été activer"
		else:
			message_bit = "Les %s Traders sélectionnées ont été activés." % users
		self.message_user(request, "%s " % message_bit)

	activer_membre.short_description = "Activer les Traders"

	actions = [desactiver_membre, activer_membre]


@admin.register(Consommateur)
class ConsommateurAdmin(PolymorphicParentModelAdmin, PolymorphicChildModelAdmin):
	base_model = Consommateur
	search_fields = ['nom', 'code_membre', 'actif', 'telephone']
	child_models = (ConsommateurParticulier, ConsommateurEntreprise)
	list_filter = (PolymorphicChildModelFilter,)
	list_display = ['nom_membre', 'telephone', 'code_membre', 'nationalite', 'compte_consommateur', 'code_qr']

	def nom_membre(self, obj):
		membre = Membre.objects.get(id=obj.id)
		if "prenoms" in membre.__dict__:
			return str(membre.nom) + " " + str(membre.prenoms)
		elif "raison_social" in membre.__dict__:
			return membre.raison_social
		else:
			return str(membre.nom)

	nom_membre.short_description = "Membre"


@admin.register(ConsommateurParticulier)
class ConsommateurParticulierAdmin(PolymorphicChildModelAdmin):
	base_model = ConsommateurParticulier
	search_fields = ['nom', 'code_membre', 'actif', 'telephone', 'profession']
	list_display = ['nom', 'prenoms', 'code_membre', 'mdp', 'telephone', 'num_carte',  'code_qr']
	list_filter = ['actif', 'sexe', 'nationalite', 'situation_matrimoniale']
	readonly_fields = ['solde_compte_consommateur', 'depense_mensuel',
					   'date_expiration_compte_consommateur', 'activiter_compte_consommateur', 'code_membre']

	fieldsets = (
		("Informations Relatifs à l'utilisateur", {
			'fields': ('user', 'code_membre', 'mdp',  'code_qr', 'nom', 'prenoms', 'date_naissance',
					   'lieu_residence', 'telephone', 'email', 'num_carte', 'formation',
					   'profession', 'situation_matrimoniale', 'nationalite', 'date_expiration'),
		}),
		('Informations Relatifs à son Compte e-C', {
			'fields': ('compte_consommateur', 'solde_compte_consommateur', 'depense_mensuel',
					   'date_expiration_compte_consommateur', 'activiter_compte_consommateur',),
		}),
	)

	def solde_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.solde)

	solde_compte_consommateur.short_description = "Solde du compte"

	def depense_mensuel(self, obj):
		return str(obj.compte_consommateur.depense_epound_mensuel)

	depense_mensuel.short_description = "Dépense du mois actuel"

	def date_expiration_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.date_expiration)

	date_expiration_compte_consommateur.short_description = "Date d'expiration"

	def activiter_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.actif)

	activiter_compte_consommateur.short_description = "En activité"

	def nom_membre(self, obj):
		membre = Membre.objects.get(id=obj.id)
		if "prenoms" in membre.__dict__:
			return membre.nom + " " + str(membre.prenoms)
		else:
			return membre.nom

	nom_membre.short_description = "Membre"

	def desactiver_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "Le Consommateur  sélectionner a été désactiver"
		else:
			message_bit = "Les %s Consommateurs sélectionnées ont été désactivés." % users
		self.message_user(request, "%s " % message_bit)

	desactiver_membre.short_description = "Désactiver les Consommateurs"

	def activer_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "Le Consommateur sélectionner a été activer"
		else:
			message_bit = "Les %s Consommateurs sélectionnées ont été activés." % users
		self.message_user(request, "%s " % message_bit)

	activer_membre.short_description = "Activer les Consommateurs"

	actions = [desactiver_membre, activer_membre]

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = ConsommateurParticulierForm
		return super().get_form(request, obj, **kwargs)


@admin.register(ConsommateurEntreprise)
class ConsommateurEntrepriseAdmin(PolymorphicChildModelAdmin):
	base_model = ConsommateurEntreprise
	search_fields = ['nom', 'code_membre''actif', ]
	list_display = ['raison_social', 'statut_juridique', 'nif', 'siege_social', ]

	readonly_fields = ['numero_compte_consommateur', 'solde_compte_consommateur',
					   'date_expiration_compte_consommateur', 'activiter_compte_consommateur', ]

	fieldsets = (
		("Informations Relatifs à l'Entreprise", {
			'fields': ('user', 'mdp', 'raison_social', 'telephone', 'statut_juridique', 'objet_social',
					   'capital_social', 'numero_rccm', 'regime_fiscal', 'nif',
					   'siege_social', 'numero_compte_bancaire', 'responsable', 'date_expiration'),
		}),
		('Informations Relatifs au Compte e-C', {
			'fields': ('compte_consommateur', 'numero_compte_consommateur', 'solde_compte_consommateur',
					   'date_expiration_compte_consommateur', 'activiter_compte_consommateur',),
		}),
	)

	def solde_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.solde)

	solde_compte_consommateur.short_description = "Solde du compte"

	def numero_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.numero_compte)

	numero_compte_consommateur.short_description = "Numéro de compte"

	def date_expiration_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.date_expiration)

	date_expiration_compte_consommateur.short_description = "Date d'expiration"

	def activiter_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_consommateur.actif)

	activiter_compte_consommateur.short_description = "En activité"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = ConsommateurForm
		return super().get_form(request, obj, **kwargs)


@admin.register(EntrepriseCommerciale)
class EntrepriseCommercialeAdmin(PolymorphicChildModelAdmin):
	base_model = EntrepriseCommerciale
	prepopulated_fields = {"slug": ("nom",)}
	search_fields = ['nom', 'code_membre', 'telephone', 'nif', 'num_cfe', 'numero_cnss']
	list_filter = ['actif', 'emplacement', 'type_market', 'nature_jurique']
	list_display = ['nom', 'besoin_gere', 'recette', 'prelevement', 'creance_dues', 'telephone', 'email', 'code_qr']
	readonly_fields = ['numero_compte_consommateur', 'solde_compte_consommateur',
					   'date_expiration_compte_consommateur', 'activiter_compte_consommateur',
					   'numero_compte_business', 'solde_compte_business',
					   'date_expiration_compte_business', 'activiter_compte_business', ]
	fieldsets = (
		("Compte d'entreprise", {
			'fields': ('compte_entreprise_commercial',),
		}),
		("Informations entreprise", {
			'fields': ('besoin_fondamental', 'besoin_gere', 'nom', 'emplacement', 'mdp', 'code_qr',
					   'telephone', 'contact_1', 'contact_2', 'email', 'slug', 'objet_social', 'nature_jurique',
					   'numero_rccm', 'regime_fiscal', 'nif', 'siege_social',
					   'numero_cnss', 'responsable', 'banniere_principal',
					   'banniere_secondaire', 'banniere_trois', 'banniere_quatre',
					   'banniere_cinq', 'date_expiration', 'actif', 'type_market',
					   )
		}),
		('Informations  Compte e-C', {
			'fields': ('numero_compte_consommateur', 'solde_compte_consommateur',
					   'date_expiration_compte_consommateur', 'activiter_compte_consommateur',),
		}),
		('Informations  Compte e-B', {
			'fields': ('numero_compte_business', 'solde_compte_business',
					   'date_expiration_compte_business', 'activiter_compte_business',),
		}),
	)

	# fonction traitant l'affichage du compte consommateurs lié

	def recette(self, obj):
		entreprise = EntrepriseCommerciale.objects.get(id=obj.id)
		return str(entreprise.compte_entreprise_commercial.compte_business.solde)

	recette.short_description = "Recette"

	def prelevement(self, obj):
		entreprise = EntrepriseCommerciale.objects.get(id=obj.id)
		return str(int(entreprise.compte_entreprise_commercial.compte_business.solde * 0.05))

	prelevement.short_description = "Prélevement"

	def creance_dues(self, obj):
		entreprise = EntrepriseCommerciale.objects.get(id=obj.id)
		return str(int(entreprise.compte_entreprise_commercial.compte_business.solde * 0.70))

	creance_dues.short_description = "Créances dues"

	def solde_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_consommateur.solde)

	solde_compte_consommateur.short_description = "Solde du compte"

	def numero_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_consommateur.id)

	numero_compte_consommateur.short_description = "Identifiant de compte"

	def date_expiration_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_consommateur.date_expiration)

	date_expiration_compte_consommateur.short_description = "Date d'expiration"

	def activiter_compte_consommateur(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_consommateur.actif)

	activiter_compte_consommateur.short_description = "En activité"

	# fonction traitant l'affichage du compte business lié
	def solde_compte_business(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_business.solde)

	solde_compte_business.short_description = "Solde du compte"

	def numero_compte_business(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_business.id)

	numero_compte_business.short_description = "Identifiant de compte"

	def date_expiration_compte_business(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_business.date_expiration)

	date_expiration_compte_business.short_description = "Date d'expiration"

	def activiter_compte_business(self, obj):
		membre = Membre.objects.get(id=obj.id)
		return str(membre.compte_entreprise_commercial.compte_business.actif)

	activiter_compte_business.short_description = "En activité"

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = EntrepriseCommercialeForm
		return super().get_form(request, obj, **kwargs)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		id = str(request)
		if "change" in id:
			id = int(id.split("/")[4])
			if db_field.name == "compte_entreprise_commercial":
				entreprise = EntrepriseCommerciale.objects.get(pk=id)
				id_compte = entreprise.compte_entreprise_commercial.id
				kwargs["queryset"] = CompteEntrepriseCommerciale.objects.filter(id=id_compte)
			return super().formfield_for_foreignkey(db_field, request, **kwargs)
		else:
			if db_field.name == "compte_entreprise_commercial":
				kwargs["queryset"] = CompteEntrepriseCommerciale.objects.all()
			return super().formfield_for_foreignkey(db_field, request, **kwargs)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def desactiver_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "Le vendeur  sélectionner a été désactiver"
		else:
			message_bit = "Les %s vendeurs sélectionnées ont été désactivés." % users
		self.message_user(request, "%s " % message_bit)

	desactiver_membre.short_description = "Désactiver les Vendeur"

	def activer_membre(self, request, queryset):
		users = queryset.update(actif=False)
		if users == 1:
			message_bit = "Le vendeur sélectionner a été activer"
		else:
			message_bit = "Les %s vendeurs sélectionnées ont été activés." % users
		self.message_user(request, "%s " % message_bit)

	activer_membre.short_description = "Activer les Vendeur"

	actions = [desactiver_membre, activer_membre]




@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
	search_fields = ['nom', ]
	list_display = ['nom', 'logo', ]


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
	search_fields = ['nom', ]
	list_display = ['nom', ]


@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
	search_fields = ['nom', ]
	list_display = ['ville', 'nom', ]

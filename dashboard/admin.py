from django.contrib import admin
from dashboard.models import *
from django.utils import timezone


@admin.register(Creance)
class CreanceAdmin(admin.ModelAdmin):
	list_display = ['entreprise_associer','epounds_retrancher','voulume_convertible',
					'volume_retransferer',]
	
	autocomplete_fields = ['entreprise_associer',]
	search_fields = ['entreprise_associer',]

	# def has_add_permission(self, request):
	# 	return False

@admin.register(CreanceTotal)
class CreanceTotalAdmin(admin.ModelAdmin):

	list_display = ['total_epounds_consommateur','total_epounds','epounds_retrancher','voulume_convertible',
					'volume_retransferer',]

	# def has_add_permission(self, request):
	# 	return False

@admin.register(CreanceMonetaire)
class CreanceMonetaireAdmin(admin.ModelAdmin):

	list_display = ['cumul_bonification','compte_beta','compte_grenier','solde',]

	# def has_add_permission(self, request):
	# 	return False

@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):

	list_display = ['entreprise','montant_emprunter','credit_actuel','montant_rembourser','reste','date_remboursement']

	# def has_add_permission(self, request):
	# 	return False

@admin.register(IndiceDeConversion)
class IndiceDeConversionAdmin(admin.ModelAdmin):

	list_display = ['taux', 'total_reconversion', 'total_acheter',]

	# def has_add_permission(self, request):
	# 	return False

@admin.register(ConsommationMensuelMoyenneConsommateurActuel)
class ConsommationMensuelMoyenneConsommateurActuelAdmin(admin.ModelAdmin):

	def nombre_de_mois(self,obj):
		date = obj.date_debut_consommation-timezone.now().date()
		if date.days < 1:
			return 0
		else:
			return  int(date.days/30)

	def rapport(self,obj):
		if self.nombre_de_mois(obj) == 0:
			return 0
		return obj.epound_utiliser/self.nombre_de_mois(obj)

	list_display = ['mois','epound_utiliser', 'nombre_de_mois', 'rapport', ]

	# def has_add_permission(self, request):
	# 	return False

@admin.register(ConsommationMensuelMoyenneConsommateur)
class ConsommationMensuelMoyenneConsommateurAdmin(admin.ModelAdmin):

	def rapport(self,obj):
		return round(obj.epound_utiliser/obj.nombre_mois,2)

	list_display = ['mois','epound_utiliser', 'nombre_mois', 'rapport',]

	# def has_add_permission(self, request):
	# 	return False


@admin.register(ConsommationMensuelMoyenneVendeurActuel)
class ConsommationMensuelMoyenneVendeurActuelAdmin(admin.ModelAdmin):

	def nombre_de_mois(self,obj):
		date = obj.date_debut_consommation-timezone.now().date()
		if date.days < 1:
			return 0
		else:
			return  int(date.days/30)

	def rapport(self,obj):
		if self.nombre_de_mois(obj) == 0:
			return 0
		return obj.epound_utiliser/self.nombre_de_mois(obj)

	list_display = ['mois','epound_utiliser', 'nombre_de_mois', 'rapport',]

	# def has_add_permission(self, request):
	# 	return False


@admin.register(ConsommationMensuelMoyenneVendeur)
class ConsommationMensuelMoyenneVendeurAdmin(admin.ModelAdmin):

	def rapport(self,obj):
		return round(obj.epound_utiliser/obj.nombre_mois,2)

	list_display = ['mois','epound_utiliser', 'nombre_mois', 'rapport',]

	# def has_add_permission(self, request):
	# 	return False

@admin.register(TauxAbsorbtionGlobal)
class TauxAbsorbtionGlobalAdmin(admin.ModelAdmin):

	list_display = ['mois','epound_detenus','epound_consommer','rapport']

	def rapport(self,obj):
		return obj.epound_detenus/obj.epound_consommer

	# def has_add_permission(self, request):
	# 	return False


@admin.register(TauxAbsorbtionGlobalMensuel)
class TauxAbsorbtionGlobalMensuelAdmin(admin.ModelAdmin):

	list_display = ['mois','epound_detenus','epound_consommer','rapport',]

	def rapport(self,obj):
		return obj.epound_detenus/obj.epound_consommer

	# def has_add_permission(self, request):
	# 	return False
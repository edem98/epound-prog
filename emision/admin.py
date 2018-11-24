from django.contrib import admin
from emision.models import *
from emision.forms import *
from membre.models import Membre

@admin.register(EmissionUnites)
class EmissionUnitesAdmin(admin.ModelAdmin):
	list_display = ['beneficiaire','montant_debouse','unite_epound_correspondant',]
	autocomplete_fields = ['beneficiaire',]
	search_fields = ['beneficiaire','unite_epound_correspondant','montant_debouse']

	# def membre_beneficiaire(self,obj):
	# 	membre = Membre.objects.get(id = obj.id)
	# 	if "prenoms" in membre.__dict__:
	# 		return membre.nom +" "+str(membre.prenoms)
	# 	else:
	# 		return membre.nom
	# membre_beneficiaire.short_description = "Bénéficiaire"

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "operateur":
			kwargs["queryset"] = User.objects.filter(id=request.user.id)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_changeform_initial_data(self, request):
		return {'operateur': request.user}

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = EmissionForm
		return super().get_form(request, obj, **kwargs)

	class Media:
		js = ("js/correspondance_epound.js",)
	

@admin.register(EmissionSurCompteAlpha)
class EmissionSurCompteAlphaAdmin(admin.ModelAdmin):
	list_display = ['utilisateur', 'montant','date_emission' ]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "utilisateur":
			kwargs["queryset"] = User.objects.filter(id=request.user.id)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_changeform_initial_data(self, request):
		return {'utilisateur': request.user}

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = EmissionSurCompteAlphaForm
		return super().get_form(request, obj, **kwargs)

@admin.register(EmissionSurCompteTrader)
class EmissionSurCompteTraderAdmin(admin.ModelAdmin):
	list_display = ['utilisateur', 'trader','montant','bonification','date_emission']

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "utilisateur":
			kwargs["queryset"] = User.objects.filter(id=request.user.id)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_changeform_initial_data(self, request):
		return {'utilisateur': request.user}

	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = EmissionSurCompteTraderForm
		return super().get_form(request, obj, **kwargs)

@admin.register(EmissionSurCompteConsommateur)
class EmissionSurCompteConsommateurAdmin(admin.ModelAdmin):
	list_display = ['trader', 'consommateur','montant','bonification','date_emission']


	def get_form(self, request, obj=None, **kwargs):
		kwargs['form'] = EmissionSurCompteConsommateurForm
		return super().get_form(request, obj, **kwargs)

@admin.register(CreationParticulierParTrader)
class CreationParticulierParTraderAdmin(admin.ModelAdmin):
	list_display = ['trader','solde_initial','telephone','solde_actuel','date_emission',]


	def solde_actuel(self,obj):
		trader = Trader.objects.get(id = obj.trader.id)
		return str(trader.compte_trader.solde)
	solde_actuel.short_description = "Solde après émission de code"
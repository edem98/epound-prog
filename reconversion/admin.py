from django.contrib import admin
from reconversion.models import *
from membre.models import EntrepriseCommerciale, Consommateur
from reconversion.forms import *

@admin.register(ReconversionEntrepriseCommerciale)
class ReconversionEntrepriseCommercialeAdmin(admin.ModelAdmin):
	list_display = ['operateur','beneficiaire','epounds_disponible',
					'epounds_a_reconvertir','montant_a_prelever',
					'montant_en_cfa','montant_virer_sur_compte_conso',]
	list_filter = ['operateur', 'beneficiaire']
	autocomplete_fields = ('beneficiaire',)
	search_fields = ['beneficiaire','operateur',]

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
		kwargs['form'] = ReconversionEntrepriseCommercialeForm
		return super().get_form(request, obj, **kwargs)

	class Media:
		js = ("js/reconversion_entreprise.js",)

@admin.register(ReconversionConsommateur)
class ReconversionConsommateurAdmin(admin.ModelAdmin):
	list_display = ['operateur','beneficiaire','epounds_disponible',
					'epounds_a_reconvertir','montant_a_prelever',
					'montant_en_cfa',]
	autocomplete_fields = ['beneficiaire',]
	search_fields = ['beneficiaire','montant_en_cfa','operateur',]

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
		kwargs['form'] = ReconversionConsommateurForm
		return super().get_form(request, obj, **kwargs)

	class Media:
		js = ("js/reconversion_consommateur.js",)
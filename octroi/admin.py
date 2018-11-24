from django.contrib import admin
from octroi.models import OctroiCredit
from octroi.forms import OctroiCreditForm
from django.contrib.auth.models import User

@admin.register(OctroiCredit)
class OctroiCreditAdmin(admin.ModelAdmin):
	list_display = ['operateur','beneficiaire',
	'montant_pret','montant_prelever_sur_grenier','montant_prelever_sur_beta','date_butoir_payement','date_octroi']
	autocomplete_fields = ['beneficiaire',]
	search_fields = ['beneficiaire','epounds_disponible','montant_prelever_sur_beta']

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
		kwargs['form'] = OctroiCreditForm
		return super().get_form(request, obj, **kwargs)

	class Media:
		js = ("js/octroi_credit.js",)
	


from django.contrib import admin
from .models import *
from daterange_filter.filter import DateRangeFilter

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
	list_display = ['entreprise','recette','prelevement',"creance","date_recette",]
	readonly_fields = ['entreprise','recette','prelevement',"creance","date_recette",]
	search_fields = ["entreprise","date_recette",]
	list_filter = ['entreprise','date_recette',]

	def has_add_permission(self,request):
		return False

@admin.register(RecetteMensuel)
class RecetteMensuelAdmin(admin.ModelAdmin):
	list_display = ['entreprise','recette','prelevement',"creance","mois","date_recette",]
	readonly_fields = ['entreprise','recette','prelevement',"creance","mois","date_recette",]
	list_filter = ['entreprise','mois',('date_recette',DateRangeFilter),]

	def has_add_permission(self, request):
		return False

@admin.register(RecetteAnnuel)
class RecetteAnnuelAdmin(admin.ModelAdmin):
	list_display = ['entreprise', 'recette', 'prelevement', "creance", "date_recette", ]
	readonly_fields = ['entreprise', 'recette', 'prelevement', "creance", "date_recette", ]
	search_fields = ["entreprise", "date_recette", ]
	list_filter = ['entreprise', ('date_recette',DateRangeFilter),]


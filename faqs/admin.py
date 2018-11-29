from django.contrib import admin
from .models import *

@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
	search_fields = ['sujet','slug']
	list_display = ['sujet','slug']
	prepopulated_fields = {"slug": ("sujet",)}

@admin.register(ProblemeSolution)
class ProblemeSolutionAdmin(admin.ModelAdmin):
	search_fields = ['sujet','probleme']
	list_display = ['sujet','probleme','solution','manuel']
	list_filter = ['sujet', ]
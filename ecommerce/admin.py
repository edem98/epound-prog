from django.contrib import admin
from ecommerce.models import *
from django.utils.html import format_html





class ProductAdmin(admin.ModelAdmin):
    list_display = ['nom', 'vendeur','code_article','prix','date_ajout']

class ExpressionBesoinAdmin(admin.ModelAdmin):
    list_display = ['besoin','image_besoin',]

    def image_besoin(self,obj):
        if obj.image_illustratif != None:
            return format_html('<a href="{}" target= "_blank"> <img src="{}" width="80%"/> </a>',
            obj.image_illustratif.url,obj.image_illustratif.url,)
        else:
            return format_html('Aucune image disponible')


class SpécificationBesoinAdmin(admin.ModelAdmin):
    list_display = ['besoin_fondamental','spécification','image_besoin',]

    def image_besoin(self,obj):
        if obj.image_illustratif :
            return format_html('<a href="{}" target= "_blank"> <img src="{}" width="50%"/> </a>',
            obj.image_illustratif.url,obj.image_illustratif.url,)
        else:
            return format_html('Aucune image disponible')

class CategorieAdmin(admin.ModelAdmin):
    list_display = ['specification','nom_categorie','image_categorie',]

    def image_categorie(self,obj):
        if obj.image_categorie :
            return format_html('<a href="{}" target= "_blank"> <img src="{}" width="50%"/> </a>',
            obj.image_categorie.url,obj.image_categorie.url,)
        else:
            return format_html('Aucune image disponible')


admin.site.register(Produit,ProductAdmin)
admin.site.register(ExpressionBesoin,ExpressionBesoinAdmin)
admin.site.register(SpécificationBesoin,SpécificationBesoinAdmin)
admin.site.register(Categorie,CategorieAdmin)
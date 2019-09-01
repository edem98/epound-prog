from django.contrib import admin
from ecommerce.models import *
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ['nom', 'vendeur', 'code_article', 'prix', 'disponible', 'date_ajout']
    search_fields = ['nom', 'code_article', 'prix', ]
    list_filter = ['disponible', 'date_ajout', 'vendeur', 'categorie_besoin', 'categorie']

    def desactiver_produit(self, request, queryset):
        produits = queryset.update(disponible=False)
        if produits == 1:
            message_bit = "Le produit sélectionner a été desactiver"
        else:
            message_bit = "Les %s produits sélectionnées ont été desactivés." % produits
        self.message_user(request, "%s " % message_bit)

    desactiver_produit.short_description = "Desactiver produits selectionners"

    def activer_produit(self, request, queryset):
        produits = queryset.update(disponible=True)
        if produits == 1:
            message_bit = "Le produit sélectionner a été activer"
        else:
            message_bit = "Les %s produits sélectionnées ont été activés." % produits
        self.message_user(request, "%s " % message_bit)

    activer_produit.short_description = "Activer produits selectionners"

    actions = [desactiver_produit, activer_produit, ]


class ExpressionBesoinAdmin(admin.ModelAdmin):
    list_display = ['besoin', 'image_besoin', ]
    search_fields = ['besoin', ]

    def image_besoin(self, obj):
        if obj.image_illustratif != None:
            return format_html('<a href="{}" target= "_blank"> <img src="{}" width="80%"/> </a>',
                               obj.image_illustratif.url, obj.image_illustratif.url, )
        else:
            return format_html('Aucune image disponible')


class SpécificationBesoinAdmin(admin.ModelAdmin):
    list_display = ['besoin_fondamental', 'spécification', 'image_besoin', ]
    list_filter = ['besoin_fondamental', 'spécification', ]
    search_fields = []

    def image_besoin(self, obj):
        if obj.image_illustratif:
            return format_html('<a href="{}" target= "_blank"> <img src="{}" width="50%"/> </a>',
                               obj.image_illustratif.url, obj.image_illustratif.url, )
        else:
            return format_html('Aucune image disponible')


class CategorieAdmin(admin.ModelAdmin):
    list_display = ['specification', 'nom_categorie', 'image_categorie', ]
    search_fields = ['nom_categorie', ]
    list_filter = ['specification', ]

    def image_categorie(self, obj):
        if obj.image_categorie:
            return format_html('<a href="{}" target= "_blank"> <img src="{}" width="50%"/> </a>',
                               obj.image_categorie.url, obj.image_categorie.url, )
        else:
            return format_html('Aucune image disponible')


class ProductTrocAdmin(admin.ModelAdmin):
    list_display = ['nom', 'vendeur', 'code_article', 'prix', 'status', 'date_ajout']
    search_fields = ['nom', 'code_article', 'prix', ]
    list_filter = ['status', 'date_ajout', 'vendeur',]

    def desactiver_produit(self, request, queryset):
        produits = queryset.update(disponible=False)
        if produits == 1:
            message_bit = "Le produit sélectionner a été desactiver"
        else:
            message_bit = "Les %s produits sélectionnées ont été desactivés." % produits
        self.message_user(request, "%s " % message_bit)

    desactiver_produit.short_description = "Desactiver produits selectionners"

    def activer_produit(self, request, queryset):
        produits = queryset.update(disponible=True)
        if produits == 1:
            message_bit = "Le produit sélectionner a été activer"
        else:
            message_bit = "Les %s produits sélectionnées ont été activés." % produits
        self.message_user(request, "%s " % message_bit)

    activer_produit.short_description = "Activer produits selectionners"

    actions = [desactiver_produit, activer_produit, ]


admin.site.register(Produit, ProductAdmin)
admin.site.register(ProduitTroc, ProductTrocAdmin)
admin.site.register(ExpressionBesoin, ExpressionBesoinAdmin)
admin.site.register(SpécificationBesoin, SpécificationBesoinAdmin)
admin.site.register(Categorie, CategorieAdmin)

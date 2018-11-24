from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from archive.models import *



class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    #readonly_fields = LogEntry._meta.get_fields()
    
    list_filter = [
        'user',
        'content_type',
        'action_flag',
    ]

    search_fields = [
        'object_repr',
        'change_message',
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag_',
        'change_message',
    ]

    def has_add_permission(self,request):
        return False

    def has_change_permission(self,request,onj=None):
        return self,request.user.is_superuser and self,request.method != "POST"

    def has_delete_permission(self,request,onj=None):
        return self,request.user.is_superuser and self,request.method != "POST"

    def action_flag_(self,obj):
        flags = {
            1:"Ajout",
            2:"Modification",
            3:"Suppression"
        }
        return flags[obj.action_flag]

    def object_link(self,obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>'% (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args = [obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    
    object_link.allow_tags = True
    object_link.admin_order_fields = 'object_repr'
    object_link.short_description = u'object'
admin.site.register(LogEntry,LogEntryAdmin)

class TransactionInterComsommateurAdmin(admin.ModelAdmin):
    readonly_fields = ['envoyeur','receveur',
                        'montant_envoyer',
                        'date_transaction']
    list_display = ['envoyeur','receveur','montant_envoyer','date_transaction']

    def has_add_permission(self,request):
        return False

class TransactionCommercialComsommateurAdmin(admin.ModelAdmin):
    readonly_fields = ['envoyeur','receveur',
                        'montant_envoyer','solde_apres_transaction',
                        'date_transaction']

    list_display = ['envoyeur','receveur','montant_envoyer','solde_apres_transaction','date_transaction']

    def has_add_permission(self,request):
        return False

class ConversionTraderAdmin(admin.ModelAdmin):
    readonly_fields = ['trader','consommateur',
                        'montant_converti','epounds_transferer',
                        'solde_apres_conversion','date_conversion']

    def bonification(self,obj):
        return str(obj.montant_converti * 0.5)
    bonification.short_description = "Bonnification"

    list_display = ['trader', 'consommateur',
                       'montant_converti','bonification','epounds_transferer',
                       'solde_apres_conversion', 'date_conversion']

    def has_add_permission(self,request):
        return False

class ReconversionTraderAdmin(admin.ModelAdmin):
    readonly_fields = ['trader','consommateur',
                        'epound_reconverti','montant_retourner',
                        'solde_consommateur_apres_reconversion','date_conversion']

    list_display = ['trader', 'consommateur',
                       'epound_reconverti', 'montant_retourner',
                       'solde_consommateur_apres_reconversion', 'date_conversion']

    def has_add_permission(self,request):
        return False

class PayementConsomateurAdmin(admin.ModelAdmin):
    readonly_fields = ['envoyeur','receveur','montant_envoyer','date_transaction',]
    list_display = ['envoyeur','receveur','montant_envoyer','date_transaction',]

    def has_add_permission(self,request):
        return False

class PayementInterCommercialAdmin(admin.ModelAdmin):
    readonly_fields = ['envoyeur', 'receveur', 'montant_envoyer', 'date_transaction', ]
    list_display = ['envoyeur', 'receveur', 'montant_envoyer', 'date_transaction', ]

    def has_add_permission(self,request):
        return False

class CommandeClientAdmin(admin.ModelAdmin):
    readonly_fields = ['client', 'vendeur', 'produit', 'quantite','a_livrer',]
    list_display = ['client', 'vendeur', 'produit', 'quantite','a_livrer', ]

    def has_add_permission(self,request):
        return False

class VendeurVenteAdmin(admin.ModelAdmin):
    readonly_fields = ['numero_acheteur','numero_vendeur','acheteur','vendeur','montant',]
    list_display = ['numero_acheteur','numero_vendeur','montant','acheteur','vendeur',]

    def has_add_permission(self,request):
        return False

admin.site.register(PayementConsomateur,PayementConsomateurAdmin)

admin.site.register(PayementInterCommercial,PayementInterCommercialAdmin)

admin.site.register(TransactionInterComsommateur,TransactionInterComsommateurAdmin)

admin.site.register(TransactionCommercialComsommateur,TransactionCommercialComsommateurAdmin)

admin.site.register(ConversionTrader,ConversionTraderAdmin)

admin.site.register(ReconversionTrader,ReconversionTraderAdmin)

admin.site.register(CommandeClient,CommandeClientAdmin)

admin.site.register(VendeurVente,VendeurVenteAdmin)
from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from membre.models import *
from membre.forms import *


@admin.register(Membre)
class MembreAdmin(PolymorphicParentModelAdmin):
    base_model = Membre
    child_models = (EntrepriseCommerciale, Trader, ConsommateurParticulier, ConsommateurEntreprise)
    list_filter = (PolymorphicChildModelFilter, 'date_expiration', 'actif',)
    search_fields = ['nom', 'code_membre', "code_qr",'actif', ]
    list_display = ['nom_membre', 'code_membre', "mdp", "code_qr",'date_expiration', ]

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

    def rollback_qr_code(self, request, queryset):
        queryset = Membre.objects.all()
        for membre in queryset:
            if membre.code_qr is not None:
                membre.code_qr = BaseUserManager().make_random_password(20)
                membre.save()
                self.message_user(request, "Code Qr regenerer avec succes")

    rollback_qr_code.short_description = "Rollback des qr code des membres"

    def reformater_qr_code(self, request, queryset):
        queryset = Membre.objects.all()
        for membre in queryset:
            if membre.code_qr is not None:
                if len(membre.code_qr) > 20:
                    membre.code_qr = membre.code_qr[0:20:1]
                    membre.save()
                    self.message_user(request, "Code Qr regenerer avec succes")

    reformater_qr_code.short_description = "Reformater le qr code des membres"

    def regenerer_qr_code(self, request, queryset):
        queryset = Membre.objects.all()
        for membre in queryset:
            if membre.code_qr is not None:
                if membre.telephone not in membre.code_qr:
                    membre.code_qr = str(membre.telephone)+"-"+str(membre.code_qr)
                    membre.save()
                    self.message_user(request, "Code Qr regenerer avec succes")

    regenerer_qr_code.short_description = "Regenerer le qr code des membres"

    actions = [desactiver_membre, activer_membre, reformater_qr_code, regenerer_qr_code,]


@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    base_model = Trader
    search_fields = ['nom', 'actif', ]
    list_display = ['nom_membre', "mdp",'code_membre', 'telephone', 'mdp', 'emplacement', 'date_expiration', 'generer_mot_de_passe']
    readonly_fields = ['numero_compte_trader', 'solde_compte_trader',
                       'date_expiration_compte_trader', 'activiter_compte_trader', 'code_membre']

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'js/reset_password.js',  # project static folder
        )

    def generer_mot_de_passe(self, obj):
        return format_html('<a type="button" href="{}" id={} class="password" style="background-color: green; color: '
                           'white;padding: 5px;border: solid 1px white; text-align: center;border-radius: 15px;'
                           ' margin: 1px; display: inline-block;">Générer mot de passe''</a>',
                           reverse_lazy('membre:generer-trader-password', kwargs={'id': obj.id}), obj.id, )

    generer_mot_de_passe.short_description = "Généreration de mot de passe"

    fieldsets = (
        ('Informations Relatifs au Trader', {
            'fields': (
                'user', 'code_membre', 'nom', 'prenoms', 'telephone', 'email', 'emplacement', 'date_expiration',
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
    list_display = ['nom_membre', 'telephone', "mdp",'code_membre', 'nationalite', 'compte_consommateur', ]

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
class ConsommateurParticulierAdmin(admin.ModelAdmin):
    base_model = ConsommateurParticulier
    search_fields = ['nom', 'code_membre', 'actif', 'telephone', 'profession']
    list_display = ['nom', 'prenoms', 'code_membre', 'mdp', 'telephone', 'num_carte', 'generer_mot_de_passe']
    list_filter = ['actif', 'sexe', 'nationalite', 'situation_matrimoniale']
    readonly_fields = ['solde_compte_consommateur', 'depense_mensuel',
                       'date_expiration_compte_consommateur', 'activiter_compte_consommateur', 'code_membre',
                       'code_membre']

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'js/reset_password.js',  # project static folder
        )

    fieldsets = (
        ("Informations Relatifs à l'utilisateur", {
            'fields': ('user', 'code_membre', 'nom', 'prenoms', 'date_naissance',
                       'lieu_residence', 'telephone', 'email', 'num_carte', 'formation',
                       'profession', 'situation_matrimoniale', 'nationalite', 'date_expiration'),
        }),
        ('Informations Relatifs à son Compte e-C', {
            'fields': ('compte_consommateur', 'solde_compte_consommateur', 'depense_mensuel',
                       'date_expiration_compte_consommateur', 'activiter_compte_consommateur',),
        }),
    )

    def generer_mot_de_passe(self, obj):
        return format_html('<a type="button" href="{}" id={} class="password" style="background-color: green; color: '
                           'white;padding: 5px;border: solid 1px white; text-align: center;border-radius: 15px;'
                           ' margin: 1px; display: inline-block;">Générer mot de passe''</a>',
                           reverse_lazy('membre:generer-consommateur-passord', kwargs={'id': obj.id}), obj.id, )

    generer_mot_de_passe.short_description = "Généreration de mot de passe"

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
class ConsommateurEntrepriseAdmin(admin.ModelAdmin):
    base_model = ConsommateurEntreprise
    search_fields = ['nom', 'code_membre''actif', ]
    list_display = ['raison_social', 'statut_juridique', 'nif', 'siege_social', 'code_membre']

    readonly_fields = ['numero_compte_consommateur', 'solde_compte_consommateur',
                       'date_expiration_compte_consommateur', 'activiter_compte_consommateur', ]

    fieldsets = (
        ("Informations Relatifs à l'Entreprise", {
            'fields': ('user', 'raison_social', 'telephone', 'statut_juridique', 'objet_social',
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
class EntrepriseCommercialeAdmin(admin.ModelAdmin):
    base_model = EntrepriseCommerciale
    prepopulated_fields = {"slug": ("nom",)}
    search_fields = ['nom', 'code_membre', 'telephone', 'nif', 'num_cfe', 'numero_cnss']
    list_filter = ['actif', 'emplacement', 'besoin_fondamental', 'nature_jurique']
    list_display = ['user','nom', 'besoin_gere', 'recette', 'prelevement', 'creance_dues', 'telephone', 'mdp', 'email', 'generer_mot_de_passe']
    readonly_fields = ['numero_compte_consommateur', 'solde_compte_consommateur',
                       'date_expiration_compte_consommateur', 'activiter_compte_consommateur',
                       'numero_compte_business', 'solde_compte_business',
                       'date_expiration_compte_business', 'activiter_compte_business', 'code_membre']
    class Media:
        js = (
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'js/reset_password.js',  # project static folder
        )

    def generer_mot_de_passe(self, obj):
        return format_html('<a type="button" href="{}" id={} class="password" style="background-color: green; color: '
                           'white;padding: 5px;border: solid 1px white; text-align: center;border-radius: 15px;'
                           ' margin: 1px; display: inline-block;">Générer mot de passe''</a>',
                           reverse_lazy('membre:generer-vendeur-password', kwargs={'id': obj.id}), obj.id, )

    generer_mot_de_passe.short_description = "Généreration de mot de passe"

    fieldsets = (
        ("Compte d'entreprise", {
            'fields': ('compte_entreprise_commercial',),
        }),
        ("Informations entreprise", {
            'fields': ('besoin_fondamental', 'besoin_gere', 'nom', 'emplacement', 'localisation',
                       'telephone', 'contact_1', 'contact_2', 'email', 'slug', 'objet_social', 'nature_jurique',
                       'numero_rccm', 'regime_fiscal', 'nif', 'siege_social',
                       'numero_cnss', 'responsable', 'banniere_principal',
                       'banniere_secondaire', 'banniere_trois', 'banniere_quatre',
                       'banniere_cinq', 'date_expiration', 'actif', 'type_market',
                       )
        }),
        ('Informations  Compte e-B', {
            'fields' : ('numero_compte_business', 'solde_compte_business',
                        'date_expiration_compte_business', 'activiter_compte_business',),
        }),
        ('Informations  Compte e-C', {
            'fields': ('numero_compte_consommateur', 'solde_compte_consommateur',
                       'date_expiration_compte_consommateur', 'activiter_compte_consommateur',),
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
        users = queryset.update(actif=True)
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

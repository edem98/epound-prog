from rest_framework import serializers
from archive.models import *
from emision.models import CreationParticulierParTrader
from membre.models import *
from compte.models import *
from ecommerce.models import *
from rest_framework import permissions

class CompteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Compte
        fields = ('id','solde','date_expiration','actif',)

class CompteConsommateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompteConsommateur
        fields = ('id','solde','date_expiration','actif',)

class CompteBusinessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompteBusiness
        fields = ('id','solde','date_expiration','actif',)

class CompteTraderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompteTrader
        fields = ('id','solde','date_expiration','actif',)

class CompteEntrepriseCommercialeSerializer(serializers.HyperlinkedModelSerializer):
    compte_consommateur = CompteConsommateurSerializer()
    compte_business = CompteBusinessSerializer()
    class Meta:
        model = CompteEntrepriseCommerciale
        fields = ('id',
                    'solde','credit','date_expiration',
                    'actif','compte_consommateur',
                    'compte_business')

    def create(self,validated_data):
        compte_consommateur = validated_data.pop("compte_consommateur")
        compte_business = validated_data.pop("compte_business")
        compte  = CompteEntrepriseCommerciale.objects.create(compte_business=compte_business,
        compte_consommateur = compte_consommateur,**validated_data)
        return compte
        
class MembreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Membre
        fields = ('id','code_membre','mdp','nom', 
                    'telephone','actif',)

class ParticulierSerializer(serializers.HyperlinkedModelSerializer):
    compte_consommateur = CompteConsommateurSerializer()
    class Meta:
        model = ConsommateurParticulier
        fields = ('id','code_membre','mdp','nom', 
                    'prenoms','telephone','email','lieu_residence',
                    'num_carte','formation','profession',
                    'situation_matrimoniale','compte_consommateur',)

    def create(self,validated_data):
        compte_consommateur = validated_data.pop('compte_consommateur')
        if compte_consommateur:
            validated_data['compte_consommateur'] = CompteConsommateur.objects.create(**compte_consommateur)
            particulier = ConsommateurParticulier.objects.create(**validated_data)
            return particulier

    def update(self, instance, validated_data):
        instance =  ConsommateurParticulier.objects.get(telephone = validated_data.get('telephone'))
        instance.nom = validated_data.get('nom')
        instance.prenoms = validated_data.get('prenoms')
        instance.mdp = validated_data.get('mdp')
        instance.telephone = validated_data.get('telephone')
        instance.email = validated_data.get('email')
        instance.lieu_residence = validated_data.get('lieu_residence')
        instance.num_carte = validated_data.get('num_carte')
        instance.formation = validated_data.get('formation')
        instance.Profession = validated_data.get('profession')
        instance.situation_matrimoniale = validated_data.get('situation_matrimoniale')
        instance.actif = validated_data.get('actif')
        instance.save()
        return instance

class EntrepriseSerializer(serializers.HyperlinkedModelSerializer):
    compte_consommateur = CompteConsommateurSerializer()
    class Meta:
        model = ConsommateurEntreprise
        fields = ('id','code_membre','mdp','nom', 
                'telephone','email','raison_social','statut_juridique',
                'objet_social','capital_social','numero_rccm',
                'regime_fiscal','nif','siege_social',
                'numero_compte_bancaire','responsable','compte_consommateur',)

    def update(self, instance, validated_data):
        instance =  ConsommateurParticulier.objects.get(nom__icontains = validated_data.get('nom'))
        instance.nom = validated_data.get('nom')
        instance.prenoms = validated_data.get('prenoms')
        instance.mdp = validated_data.get('mdp')
        instance.telephone = validated_data.get('telephone')
        instance.email = validated_data.get('email')
        instance.raison_social = validated_data.get('raison_social')
        instance.statut_juridique = validated_data.get('statut_juridique')
        instance.objet_social = validated_data.get('objet_social')
        instance.capital_social = validated_data.get('capital_social')
        instance.numero_rccm = validated_data.get('numero_rccm')
        instance.regime_fiscal = validated_data.get('regime_fiscal')
        instance.nif = validated_data.get('nif')
        instance.siege_social = validated_data.get('siege_social')
        instance._bancaire = validated_data.get('_bancaire')
        instance.responsable = validated_data.get('responsable')
        instance.save()
        return instance

class ConsommateurSerializer(serializers.HyperlinkedModelSerializer):
    compte_consommateur = CompteConsommateurSerializer()
    class Meta:
        model = Membre
        fields = ('id','code_membre','mdp','nom', 
                    'telephone','actif','compte_consommateur',)

class TraderSerializer(serializers.HyperlinkedModelSerializer):
    compte_trader = CompteTraderSerializer()
    class Meta:
        model = Trader
        fields = ('id','code_membre','mdp','nom','prenoms', 
                'telephone','email','compte_trader',)

    def update(self, instance, validated_data): 
        instance =  Trader.objects.get(nom__icontains = validated_data.get('nom'))
        instance.nom = validated_data.get('nom')
        instance.prenoms = validated_data.get('prenoms')
        instance.mdp = validated_data.get('mdp')
        instance.telephone = validated_data.get('telephone')
        instance.email = validated_data.get('email')
        instance.actif = validated_data.get('actif')
        instance.save()
        return instance

class EntrepriseCommercialeSerializer(serializers.HyperlinkedModelSerializer):
    compte_entreprise_commercial = CompteEntrepriseCommercialeSerializer()
    class Meta:
        model = EntrepriseCommerciale
        depth = 1
        fields = ('id','code_membre',
                    'nom','mdp','telephone','email',
                    'actif','compte_entreprise_commercial','type_market')

    def create(self,validated_data):
        compte_entreprise_commercial = validated_data.pop('compte_entreprise_commercial')
        if compte_entreprise_commercial:
            # creation du compte conso
            compte_consommateur = compte_entreprise_commercial.pop('compte_consommateur')
            compte_entreprise_commercial['compte_consommateur'] = CompteConsommateur.objects.create(**compte_consommateur)
            # creation du compte vente
            compte_business = compte_entreprise_commercial.pop('compte_business')
            compte_entreprise_commercial['compte_business'] = CompteBusiness.objects.create(**compte_business)
            compte = CompteEntrepriseCommerciale.objects.create(**compte_entreprise_commercial)
            entreprise = EntrepriseCommerciale.objects.create(
                compte_entreprise_commercial = compte, **validated_data)
            return entreprise

    def update(self, instance, validated_data): 
        instance =  EntrepriseCommerciale.objects.get(nom__icontains = validated_data.get('nom'))
        instance.mdp = validated_data.get('mdp')
        instance.telephone = validated_data.get('telephone')
        instance.email = validated_data.get('email')
        instance.actif = validated_data.get('actif')
        instance.save()
        return instance

class TransactionInterComsommateurSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = ConsommateurSerializer(read_only = True)
    receveur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = TransactionInterComsommateur
        fields = ('numero_envoyeur','numero_receveur','montant_envoyer','date_transaction','envoyeur','receveur')
        

    def create(self,validated_data):
        numero_envoyeur = validated_data.get('numero_envoyeur')
        numero_receveur = validated_data.get('numero_receveur')
        envoyeur = Consommateur.objects.get(telephone = numero_envoyeur)
        receveur = Consommateur.objects.get(telephone = numero_receveur)
        solde = validated_data.get('montant_envoyer')
        transaction = TransactionInterComsommateur.objects.create(envoyeur = envoyeur,receveur = receveur,
                                            montant_envoyer = solde,numero_envoyeur = numero_envoyeur,
                                            numero_receveur = numero_receveur,)
        return transaction

class TransactionCommercialComsommateurSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = EntrepriseCommercialeSerializer(read_only = True)
    receveur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = TransactionCommercialComsommateur
        fields = ('envoyeur','receveur','numero_envoyeur','numero_receveur',
                    'montant_envoyer','date_transaction',)

    def create(self,validated_data):
        envoyeur_code = validated_data.get('envoyeur_code')
        receveur_code = validated_data.get('receveur_code')
        envoyeur = EntrepriseCommerciale.objects.get(code_membre = envoyeur_code)
        receveur = Consommateur.objects.get(code_membre = receveur_code)
        solde = validated_data.get('montant_envoyer')
        transaction = TransactionCommercialComsommateur.objects.create(envoyeur = envoyeur,receveur = receveur,
                                            montant_envoyer = solde,envoyeur_code = envoyeur_code,
                                            receveur_code = receveur_code,)
        return transaction

class ConversionTraderSerializer(serializers.HyperlinkedModelSerializer):
    trader = TraderSerializer(read_only = True)
    consommateur = ConsommateurSerializer(read_only = True)
    class Meta:

        model = ConversionTrader
        fields = ('numero_trader','numero_receveur',
                    'montant_converti','epounds_transferer',
                    'solde_apres_conversion','date_conversion',
                    'trader','consommateur',)

class ReconversionTraderSerializer(serializers.HyperlinkedModelSerializer):
    trader = TraderSerializer(read_only = True)
    consommateur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = ReconversionTrader
        fields = ('numero_trader','numero_receveur',
                    'epound_reconverti','montant_retourner',
                    'solde_consommateur_apres_reconversion',
                    'date_conversion','trader','consommateur',)

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','receiver','message','etat','date_notif','type_notif','sender',)

class PayementInterCommercialSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = EntrepriseCommercialeSerializer(read_only = True)
    recepteur = EntrepriseCommercialeSerializer(read_only = True)
    class Meta:
        model = PayementInterCommercial
        fields = ('id','envoyeur_code','receveur_code',
                    'montant_envoyer','solde_apres_transaction',
                    'date_transaction','envoyeur','recepteur',)

class PayementConsommateurSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = ConsommateurSerializer(read_only = True)
    recepteur = EntrepriseCommercialeSerializer(read_only = True)
    class Meta:
        model = PayementConsomateur
        fields = ('id','telephone_envoyeur','telephone_receveur',
                    'montant_envoyer','solde_apres_transaction',
                    'date_transaction','envoyeur','recepteur',)

class CreationParticulierParTraderSerializer(serializers.HyperlinkedModelSerializer):
    trader = TraderSerializer(read_only = True)
    consommateur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = CreationParticulierParTrader
        fields = ('id','numero_trader','telephone','mdp','trader','consommateur',)

    def create(self,validated_data):
        numero_trader = validated_data.get('numero_trader')
        telephone = validated_data.get('telephone')
        mdp = validated_data.get('mdp')
        consommateur = ConsommateurParticulier(telephone = telephone,mdp = mdp,)
        trader = Trader.objects.get(telephone = numero_trader)
        creation = CreationParticulierParTrader.objects.create(numero_trader = numero_trader,
        telephone = telephone,mdp = mdp,consommateur = consommateur,trader = trader)
        return creation

class CreationEntrepriseParTraderSerializer(serializers.HyperlinkedModelSerializer):
    trader = TraderSerializer(read_only = True)
    consommateur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = CreationEntrepriseParTrader
        fields = ('id','code_trader','telephone','mdp','trader','consommateur',)

    def create(self,validated_data):
        code_trader = validated_data.get('code_trader')
        telephone = validated_data.get('telephone')
        mdp = validated_data.get('mdp')
        consommateur = ConsommateurEntreprise(telephone = telephone,mdp = mdp,)
        trader = Trader.objects.get(code_membre = code_trader)
        creation = CreationEntrepriseParTrader.objects.create(code_trader = code_trader,
        telephone = telephone,mdp = mdp,consommateur = consommateur,trader = trader)
        return creation

class BesoinSerializer(serializers.HyperlinkedModelSerializer):
    """ serializer de besoin prenant juste en compte le nom du besoin"""
    class Meta:
        model = ExpressionBesoin
        fields = ('id','besoin',)

class SpecificationSerializer(serializers.HyperlinkedModelSerializer):
    """ serializer des specification des besoin prenant juste en compte le nom de la specification"""
    besoin_fondamental = BesoinSerializer(read_only=True)
    class Meta:
        model = SpécificationBesoin
        fields = ('id','spécification','besoin_fondamental')

class CategorieSerializer(serializers.HyperlinkedModelSerializer):

    specification = SpecificationSerializer(read_only = True)
    class Meta:
        model = Categorie
        fields = ('id','nom_categorie','specification')

class ProduitSerializer(serializers.HyperlinkedModelSerializer):
    vendeur = EntrepriseCommercialeSerializer(read_only=True)
    categorie = CategorieSerializer(read_only=True)
    categorie_besoin = SpecificationSerializer(read_only=True)
    class Meta:
        model = Produit
        fields = ('id','nom','categorie_besoin','categorie','code_article','prix','marque','modele','description','vendeur')

class CommandeClientSerializer(serializers.HyperlinkedModelSerializer):
    vendeur = EntrepriseCommercialeSerializer(read_only=True)
    client = ConsommateurSerializer(read_only=True)
    produit = ProduitSerializer(read_only=True)

    def create(self,validated_data):
        vendeur = validated_data.pop("vendeur")
        client = validated_data.pop("client")
        produit = validated_data.pop("produit")
        commande  = CommandeClient.objects.create(vendeur=vendeur,
                                                client = client,produit=produit,
                                                **validated_data)
        return commande

    class Meta:
        model = CommandeClient
        fields = ('id','numero_client','numero_vendeur','code_produit','quantite','etat','valider','a_livrer','client','vendeur','produit',)

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','receiver','message','etat','date_notif','type_notif','sender',)

class VendeuVenteSerializer(serializers.HyperlinkedModelSerializer):
    acheteur = ConsommateurSerializer(read_only=True)
    vendeur = EntrepriseCommercialeSerializer(read_only=True)
    class Meta:
        model = VendeurVente
        fields = ('id','numero_acheteur','numero_vendeur','montant','acheteur','vendeur',)
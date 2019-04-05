from docutils.nodes import transition
from rest_framework import serializers
from archive.models import *
from emision.models import CreationParticulierParTrader
from membre.models import *
from compte.models import *
from ecommerce.models import *


from archive.models import ReactivationClient

class CompteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Compte
        fields = ('id','solde','date_expiration','actif',)

class CompteConsommateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompteConsommateur
        fields = ('id','solde','depense_epound_mensuel','date_expiration','actif',)

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
    compte_consommateur = CompteConsommateurSerializer(read_only = True)
    class Meta:
        model = ConsommateurParticulier
        fields = ('id','code_membre','mdp','nom', 
                    'prenoms','sexe','ville_residence','date_naissance','telephone','email','lieu_residence',
                    'num_carte','formation','profession',
                    'situation_matrimoniale','compte_consommateur',)

    def create(self,validated_data):
        compte_consommateur = validated_data.pop('compte_consommateur')
        if compte_consommateur:
            validated_data['compte_consommateur'] = CompteConsommateur.objects.create(**compte_consommateur)
            particulier = ConsommateurParticulier.objects.create(**validated_data)
            return particulier

    def update(self, instance, validated_data):
        print("changement en loading")
        instance =  ConsommateurParticulier.objects.get(telephone = validated_data.get('telephone'))
        if instance:
            if validated_data.get('nom'):
                instance.nom = validated_data.get('nom')
            if validated_data.get('prenoms'):
                instance.prenoms = validated_data.get('prenoms')
            if validated_data.get('mdp'):
                instance.mdp = validated_data.get('mdp')
            if validated_data.get('ville_residence'):
                instance.ville_residence = validated_data.get('ville_residence')
            if validated_data.get('sexe'):
                instance.sexe = validated_data.get('sexe')
            if validated_data.get('email'):
                instance.email = validated_data.get('email')
            if validated_data.get('lieu_residence'):
                instance.lieu_residence = validated_data.get('lieu_residence')
            if validated_data.get('num_carte'):
                instance.num_carte = validated_data.get('num_carte')
            if validated_data.get('formation'):
                instance.formation = validated_data.get('formation')
            if validated_data.get('profession'):
                instance.Profession = validated_data.get('profession')
            if validated_data.get('situation_matrimoniale'):
                instance.situation_matrimoniale = validated_data.get('situation_matrimoniale')
            if validated_data.get('actif'):
                instance.actif = validated_data.get('actif')
            instance.save()
        return instance

class ConsommateurSerializer(serializers.HyperlinkedModelSerializer):
    compte_consommateur = CompteConsommateurSerializer()
    class Meta:
        model = Membre
        fields = ('id','code_membre','mdp','nom', 
                    'telephone','actif','compte_consommateur',)

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
        if envoyeur.compte_consommateur.solde > solde:
            transaction = TransactionInterComsommateur.objects.create(envoyeur=envoyeur, receveur=receveur,
                                                                      montant_envoyer=solde,
                                                                      numero_envoyeur=numero_envoyeur,
                                                                      numero_receveur=numero_receveur, )
            return transaction
        else:
            data = {}
            data["echec"] = "Solde insuffisant pour effectuer la transaction"
            raise serializers.ValidationError(data)

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','receiver','message','etat','date_notif','type_notif','sender',)

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

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','receiver','message','etat','date_notif','type_notif','sender',)

class VilleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ville
        fields = ('id','nom',)

class QuartierSerializer(serializers.HyperlinkedModelSerializer):
    ville = VilleSerializer()

    class Meta:
        model = Quartier
        fields = ('id','nom','ville')

class EntrepriseSerializer(serializers.HyperlinkedModelSerializer):
    compte_consommateur = CompteConsommateurSerializer(read_only = True)
    emplacement = QuartierSerializer(read_only=True)
    besoin_fondamental = BesoinSerializer(read_only=True)
    class Meta:
        model = ConsommateurEntreprise
        fields = ('id','code_membre','mdp','nom','besoin_fondamental'
                'telephone','email','raison_social','emplacement','statut_juridique',
                'objet_social','capital_social','numero_rccm',
                'regime_fiscal','nif','siege_social',
                'numero_compte_bancaire','responsable','compte_consommateur',)

    def update(self, instance, validated_data):
        instance =  ConsommateurEntreprise.objects.get(telephone = validated_data.get('telephone'))
        if instance:
            if validated_data.get('nom'):
                instance.nom = validated_data.get('nom')
            if validated_data.get('prenoms'):
                instance.prenoms = validated_data.get('prenoms')
            if validated_data.get('mdp'):
                instance.mdp = validated_data.get('mdp')
            if validated_data.get('telephone'):
                instance.telephone = validated_data.get('telephone')
            if validated_data.get('email'):
                instance.email = validated_data.get('email')
            if validated_data.get('raison_social'):
                instance.raison_social = validated_data.get('raison_social')
            if validated_data.get('emplacement'):
                instance.raison_social = validated_data.get('emplacement')
            if validated_data.get('statut_juridique'):
                instance.statut_juridique = validated_data.get('statut_juridique')
            if validated_data.get('objet_social'):
                instance.objet_social = validated_data.get('objet_social')
            if validated_data.get('capital_social'):
                instance.capital_social = validated_data.get('capital_social')
            if validated_data.get('numero_rccm'):
                instance.numero_rccm = validated_data.get('numero_rccm')
            if validated_data.get('regime_fiscal'):
                instance.regime_fiscal = validated_data.get('regime_fiscal')
            if validated_data.get('nif'):
                instance.nif = validated_data.get('nif')
            if validated_data.get('siege_social'):
                instance.siege_social = validated_data.get('siege_social')
            if validated_data.get('_bancaire'):
                instance._bancaire = validated_data.get('_bancaire')
            if validated_data.get('responsable'):
                instance.responsable = validated_data.get('responsable')
            instance.save()
        return instance

class TraderSerializer(serializers.HyperlinkedModelSerializer):
    compte_trader = CompteTraderSerializer(read_only=True)
    emplacement = QuartierSerializer()
    class Meta:
        model = Trader
        fields = ('id','code_membre','mdp','nom','prenoms',
                'sexe','ville_residence','telephone','email','compte_trader','emplacement',)

    def update(self, instance, validated_data):
        instance = Trader.objects.get(telephone=validated_data.get('telephone'))
        if instance:
            if validated_data.get('nom'):
                instance.nom = validated_data.get('nom')
            if validated_data.get('prenoms'):
                instance.prenoms = validated_data.get('prenoms')
            if validated_data.get('mdp'):
                instance.mdp = validated_data.get('mdp')
            if validated_data.get('telephone'):
                instance.telephone = validated_data.get('telephone')
            if validated_data.get('email'):
                instance.email = validated_data.get('email')
            if validated_data.get('actif'):
                instance.actif = validated_data.get('actif')
            instance.save()
        return instance

class EntrepriseCommercialeSerializer(serializers.HyperlinkedModelSerializer):

    compte_entreprise_commercial = CompteEntrepriseCommercialeSerializer(read_only=True)
    emplacement = QuartierSerializer(read_only=True)
    besoin_fondamental = BesoinSerializer(read_only=True)
    class Meta:
        model = EntrepriseCommerciale
        depth = 1
        fields = ('id','code_membre','nom','mdp','telephone','emplacement','email','besoin_fondamental','actif','compte_entreprise_commercial',
                  'type_market','nature_jurique','numero_rccm','regime_fiscal','nif','siege_social','numero_cnss','responsable',)

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
        instance =  EntrepriseCommerciale.objects.get(telephone=validated_data.get('telephone'))
        if validated_data.get('nom'):
            instance.nom = validated_data.get('nom')
        if validated_data.get('mdp'):
            instance.mdp = validated_data.get('mdp')
        if validated_data.get('telephone'):
            instance.telephone = validated_data.get('telephone')
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        if validated_data.get('actif'):
            instance.actif = validated_data.get('actif')
        instance.save()
        return instance

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
                    'date_conversion','trader','consommateur','mdp')

    def create(self,validated_data):
        numero_receveur = validated_data.pop('numero_receveur')
        mdp_acheteur = validated_data.pop('mdp')
        if numero_receveur and mdp_acheteur:
            client = Consommateur.objects.get(telephone=numero_receveur)
            if client.mdp != mdp_acheteur:
                data = {}
                data["echec"]= "Le mot de passe ne correspond"
                raise serializers.ValidationError(data)
            else:
                validated_data['numero_receveur'] = numero_receveur
                validated_data['mdp'] = mdp_acheteur
                reconversion = ReconversionTrader.objects.create(**validated_data)
                return reconversion
        data = {}
        data["echec"] = "Veillez spécifier le mot de passe du consommateur"
        raise serializers.ValidationError(data)

class CreationParticulierParTraderSerializer(serializers.HyperlinkedModelSerializer):
    trader = TraderSerializer(read_only = True)
    consommateur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = CreationParticulierParTrader
        fields = ('id','numero_trader','telephone','trader','consommateur',)

    def create(self,validated_data):
        numero_trader = validated_data.get('numero_trader')
        telephone = validated_data.get('telephone')
        client = ConsommateurParticulier.objects.filter(telephone=telephone)
        if not client.exists():
            consommateur = ConsommateurParticulier(telephone=telephone, mdp="123456789", )
            trader = Trader.objects.get(telephone=numero_trader)
            creation = CreationParticulierParTrader.objects.create(numero_trader=numero_trader,
                                                                   telephone=telephone, consommateur=consommateur,
                                                                   trader=trader)
            return creation
        else:
            print(client)
            data = {}
            data["echec"] = "Ce client est deja enregistré"
            raise serializers.ValidationError(data)

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

class ReactivationClientSerializer(serializers.HyperlinkedModelSerializer):

    trader = TraderSerializer(read_only=True)
    consommateur = ConsommateurSerializer(read_only=True)

    class Meta:
        model = ReactivationClient
        fields = ('id', 'numero_trader', 'numero_receveur', 'trader', 'consommateur', 'date_reabonnement',)

class TransactionCommercialComsommateurSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = EntrepriseCommercialeSerializer(read_only = True)
    receveur = ConsommateurSerializer(read_only = True)
    class Meta:
        model = TransactionCommercialComsommateur
        fields = ('envoyeur','receveur','numero_envoyeur','numero_receveur',
                    'montant_envoyer','date_transaction',)

    def create(self,validated_data):
        numero_envoyeur = validated_data.get('numero_envoyeur')
        numero_receveur = validated_data.get('numero_receveur')
        envoyeur = EntrepriseCommerciale.objects.get(telephone = numero_envoyeur)
        receveur = Consommateur.objects.get(telephone=numero_receveur)
        solde = validated_data.get('montant_envoyer')
        transaction = TransactionCommercialComsommateur.objects.create(envoyeur = envoyeur,receveur = receveur,
                                            montant_envoyer = solde,numero_envoyeur = numero_envoyeur,
                                                                       numero_receveur = numero_receveur)
        if str(transaction) != "TransactionCommercialComsommateur object (None)":
            return transaction
        else:
            data = {}
            data['echec'] = "Montant insuffisant"
            print("Montant insuffisant")
            raise serializers.ValidationError(data)

class PayementInterCommercialSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = EntrepriseCommercialeSerializer(read_only = True)
    recepteur = EntrepriseCommercialeSerializer(read_only = True)
    class Meta:
        model = PayementInterCommercial
        fields = ('id','numero_envoyeur','numero_receveur',
                    'montant_envoyer','solde_apres_transaction',
                    'date_transaction','envoyeur','recepteur',)

    def create(self,validated_data):
        telephone_envoyeur = validated_data.pop('telephone_envoyeur')
        telephone_receveur = validated_data.pop('telephone_receveur')
        montant_envoyer = validated_data.pop('montant_envoyer')
        if telephone_envoyeur and telephone_receveur:
            client = EntrepriseCommerciale.objects.get(telephone=telephone_envoyeur)
            if client.compte_entreprise_commercial.compte_consommateur.depense_epound_mensuel + int(montant_envoyer) > CompteConsommateur.DEPENSE_MAX_MENSUEL:
                data = {}
                data["echec"]= "vous avez atteind le plafond mensuel de 100.000 epound"
                raise serializers.ValidationError(data)
        else:
            validated_data['telephone_envoyeur'] = telephone_envoyeur
            validated_data['telephone_receveur'] = telephone_receveur
            validated_data['montant_envoyer'] = montant_envoyer
            payement = PayementInterCommercial.objects.create(**validated_data)
            return payement

class PayementConsommateurSerializer(serializers.HyperlinkedModelSerializer):
    envoyeur = ConsommateurSerializer(read_only = True)
    recepteur = EntrepriseCommercialeSerializer(read_only = True)
    class Meta:
        model = PayementConsomateur
        fields = ('id','telephone_envoyeur','telephone_receveur',
                    'montant_envoyer','solde_apres_transaction',
                    'date_transaction','envoyeur','recepteur',)

    def create(self,validated_data):
        telephone_envoyeur = validated_data.pop('telephone_envoyeur')
        telephone_receveur = validated_data.pop('telephone_receveur')
        montant_envoyer = validated_data.pop('montant_envoyer')
        if telephone_envoyeur and telephone_receveur:
            client = ConsommateurParticulier.objects.get(telephone=telephone_envoyeur)
            if client.compte_consommateur.depense_epound_mensuel + int(montant_envoyer) > CompteConsommateur.DEPENSE_MAX_MENSUEL:
                data = {}
                data["echec"]= "vous avez atteind le plafond mensuel de 100.000 epound"
                raise serializers.ValidationError(data)
        else:
            validated_data['telephone_envoyeur'] = telephone_envoyeur
            validated_data['telephone_receveur'] = telephone_receveur
            validated_data['montant_envoyer'] = montant_envoyer
            payement = PayementConsomateur.objects.create(**validated_data)
            return payement

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

    class Meta:
        model = CommandeClient
        fields = ('id','numero_client','numero_vendeur',
                    'code_produit','quantite','etat','valider',
                    'a_livrer','client','vendeur','produit','date_commande')

    def update(self, instance, validated_data):
        print("updating")
        instance = CommandeClient.objects.get(pk=instance.id)
        instance.etat = validated_data['etat']
        instance.valider = validated_data['valider']
        instance.save()
        return instance

class VendeuVenteSerializer(serializers.HyperlinkedModelSerializer):
    acheteur = ConsommateurSerializer(read_only=True)
    vendeur = EntrepriseCommercialeSerializer(read_only=True)
    class Meta:
        model = VendeurVente
        fields = ('id','numero_acheteur','mdp_acheteur','numero_vendeur','montant','acheteur','vendeur',)

    def create(self,validated_data):
        numero_acheteur = validated_data.pop('numero_acheteur')
        mdp_acheteur = validated_data.pop('mdp_acheteur')
        montant = validated_data.pop('montant')
        if numero_acheteur and mdp_acheteur:
            client = Consommateur.objects.get(telephone=numero_acheteur)
            if client.mdp != mdp_acheteur:
                data = {}
                data["echec"]= "Le mot de passe ne correspond"
                raise serializers.ValidationError(data)
            elif client.compte_consommateur.solde < int(montant):
                data = {}
                data["echec"] = "Montant insuffisant"
                raise serializers.ValidationError(data)
            elif int(montant) < 100000 and client.compte_consommateur.solde < int(montant):
                data = {}
                data["echec"] = "Montant insuffisant"
                raise serializers.ValidationError(data)
            elif int(montant) < 100000 and client.compte_consommateur.solde > int(montant):
                validated_data['numero_acheteur'] = numero_acheteur
                validated_data['mdp_acheteur'] = mdp_acheteur
                validated_data['montant'] = montant
                vente = VendeurVente.objects.create(**validated_data)
                return vente
            else:
                data = {}
                data["echec"] = "Service indisponible"
                raise serializers.ValidationError(data)

class MessageClientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MessageClient
        fields = ('id','telephone','message','date_envoye')

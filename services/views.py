from rest_framework import viewsets
from membre.models import ConsommateurParticulier,Membre,Trader
from compte.models import Compte,CompteEntrepriseCommerciale
from archive.models import Notification
from services.serializers import *
from rest_framework.decorators import action

from rest_framework import status
from rest_framework.response import Response

class MembreViewSet(viewsets.ModelViewSet):

    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    lookup_field = "telephone"

    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        type_client = ""
        serializer = None
        print(telephone)
        try:
            particulier = ConsommateurParticulier.objects.filter(telephone=telephone)
            if str(particulier) != "<PolymorphicQuerySet []>":
                serializer = ParticulierSerializer(particulier[0])
                type_client = "particulier"

            entreprise = ConsommateurEntreprise.objects.filter(telephone=telephone)
            if str(entreprise) != "<PolymorphicQuerySet []>":
                serializer = EntrepriseSerializer(entreprise[0])
                type_client = "entreprise"

            vendeur = EntrepriseCommerciale.objects.filter(telephone=telephone)
            if str(vendeur) != "<PolymorphicQuerySet []>":
                serializer = EntrepriseCommercialeSerializer(vendeur[0])
                type_client = "vendeur"

        except ConsommateurParticulier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        if serializer.data != None:
            data["client"] = serializer.data
        data["type_client"] = type_client
        return Response(data)

class ParticulierViewSet(viewsets.ModelViewSet):

    queryset = ConsommateurParticulier.objects.all()
    serializer_class = ParticulierSerializer
    lookup_field = "telephone"


    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        try:
            particulier = ConsommateurParticulier.objects.get(telephone= telephone)
        except ConsommateurParticulier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ParticulierSerializer(particulier)
        return Response(serializer.data)

class EntrepriseViewSet(viewsets.ModelViewSet):

    queryset = ConsommateurEntreprise.objects.all()
    serializer_class = EntrepriseSerializer
    lookup_field = "telephone"


    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        try:
            particulier = ConsommateurEntreprise.objects.get(telephone= telephone)
        except ConsommateurEntreprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EntrepriseSerializer(particulier)
        return Response(serializer.data)

class CompteViewSet(viewsets.ModelViewSet):

    queryset = Compte.objects.all()
    serializer_class = CompteSerializer

class EntrepriseCommercialeViewSet(viewsets.ModelViewSet):
    queryset = EntrepriseCommerciale.objects.all()
    serializer_class = EntrepriseCommercialeSerializer
    lookup_field = "telephone"

class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer
    lookup_field = "telephone"

class TransactionInterComsommateurViewSet(viewsets.ModelViewSet):
    queryset = TransactionInterComsommateur.objects.all()
    serializer_class = TransactionInterComsommateurSerializer
    lookup_field = "numero_envoyeur"

class TransactionCommercialComsommateurViewSet(viewsets.ModelViewSet):
    queryset = TransactionCommercialComsommateur.objects.all()
    serializer_class = TransactionCommercialComsommateurSerializer

class ConversionTraderViewSet(viewsets.ModelViewSet):
    queryset = ConversionTrader.objects.all()
    serializer_class = ConversionTraderSerializer

class ReconversionTraderViewSet(viewsets.ModelViewSet):
    queryset = ReconversionTrader.objects.all()
    serializer_class = ReconversionTraderSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class PayementConsommateurViewSet(viewsets.ModelViewSet):
    queryset = PayementConsomateur.objects.all()
    serializer_class = PayementConsommateurSerializer

class PayementInterCommercialViewSet(viewsets.ModelViewSet):
    queryset = PayementInterCommercial.objects.all()
    serializer_class = PayementInterCommercialSerializer

class CreationParticulierParTraderViewSet(viewsets.ModelViewSet):

    queryset = CreationParticulierParTrader.objects.all()
    serializer_class = CreationParticulierParTraderSerializer

class CreationEntrepriseParTraderViewSet(viewsets.ModelViewSet):

    queryset = CreationEntrepriseParTrader.objects.all()
    serializer_class = CreationEntrepriseParTraderSerializer

class BesoinViewSet(viewsets.ModelViewSet):

    queryset = ExpressionBesoin.objects.all()
    serializer_class = BesoinSerializer

class SpecificationViewSet(viewsets.ModelViewSet):

    queryset = SpécificationBesoin.objects.all()
    serializer_class = SpecificationSerializer

class ProduitViewSet(viewsets.ModelViewSet):

    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    lookup_field = "code_article"

class CommandeClientViewSet(viewsets.ModelViewSet):

    queryset = CommandeClient.objects.all()
    serializer_class =CommandeClientSerializer
    lookup_field = "numero_client"

    @action(methods=['get'], detail=True)
    def get_commande_by_numero_vendeur(self, request, numero_client=None):
        commandes=None
        try:
            commandes = CommandeClient.objects.filter(numero_vendeur=numero_client)

        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        serializer = CommandeClientSerializer(commandes, many=True)
        data["commandes"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_commande_by_numero_client(self, request, numero_client=None):
        commandes = None
        try:
            commandes = CommandeClient.objects.filter(numero_client=numero_client)

        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        serializer = CommandeClientSerializer(commandes, many=True)
        data["commandes"] = serializer.data
        return Response(data)

    @action(methods=['post'], detail=True)
    def valider_commande(self, request, numero_client=None):
        data = {}
        try:
            commande = CommandeClient.objects.get(pk=numero_client)
            if not commande.valider:
                vendeur=EntrepriseCommerciale.objects.get(id = commande.vendeur)
                vendeur.compte_entreprise_commercial.compte_business.solde += commande.quantite*commande.produit.prix
                vendeur.compte_entreprise_commercial.compte_business.save()
                commande.etat = 2
                commande.vendeur=True
                commande.save()
            else:
                data["echec"] = "Commande déja valider"
                return Response(data)
        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        data["succes"] = "Commande valider"
        return Response(data)

    @action(methods=['post'], detail=True)
    def confirmer_disponibilite(self, request, numero_client=None):
        data = {}
        try:
            commande = CommandeClient.objects.get(pk=numero_client)
            commande.etat = 1
            commande.save()
        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data["succes"] = "Commande valider"
        return Response(data)

    @action(methods=['post'], detail=True)
    def commande_indisponible(self, request, numero_client=None):
        data = {}
        try:
            commande = CommandeClient.objects.get(pk=numero_client)
            if commande.etat != -1:
                consommateur = Consommateur.objects.get(pk=commande.client)
                consommateur.compte_consommateur.solde += commande.quantite*commande.produit.prix
                consommateur.compte_consommateur.save()
                commande.etat = -1
                commande.save()
            else:
                return Response(data)
        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data["succes"] = "Commande annulé"
        return Response(data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        notifications = None
        try:
            notifications = Notification.objects.filter(receiver= telephone)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {}
        serializer = NotificationSerializer(notifications,many = True)
        data["notifs"] = serializer.data
        return Response(data)

class VendeurVenteViewSet(viewsets.ModelViewSet):
    queryset = VendeurVente.objects.all()
    serializer_class = VendeuVenteSerializer
    look_field = "numero_vendeur"


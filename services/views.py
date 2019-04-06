from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from services.serializers import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from archive.models import ReactivationClient
from services.serializers import ReactivationClientSerializer

class MembreViewSet(viewsets.ModelViewSet):

    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    lookup_field = "telephone"

    @action(methods=['post'], detail=True)
    def set_password(self, request, password,telephone=None):
        data = {}
        resultat ="echec"
        try:
            particulier = ConsommateurParticulier.objects.filter(telephone=telephone)
            if str(particulier) != "<PolymorphicQuerySet []>":
                particulier = particulier[0]
                particulier.mdp = password
                particulier.save()
                resultat = "succes"
                data["resultat"] = resultat
                data["mdp"] = password
                return Response(data)

            entreprise = ConsommateurEntreprise.objects.filter(telephone=telephone)
            if str(entreprise) != "<PolymorphicQuerySet []>":
                entreprise = entreprise[0]
                entreprise.mdp = password
                entreprise.save()
                resultat = "succes"
                data["resultat"] = resultat
                data["mdp"] = password
                return Response(data)

            vendeur = EntrepriseCommerciale.objects.filter(telephone=telephone)
            if str(vendeur) != "<PolymorphicQuerySet []>":
                vendeur = vendeur[0]
                vendeur.mdp = password
                vendeur.save()
                resultat = "succes"
                data["resultat"] = resultat
                data["mdp"] = password
                return Response(data)

            trader = Trader.objects.filter(telephone=telephone)
            if str(trader) != "<PolymorphicQuerySet []>":
                trader = trader[0]
                trader.mdp = password
                trader.save()
                resultat = "succes"
                data["resultat"] = resultat
                data["mdp"] = password
                return Response(data)

        except Membre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data["resultat"] = resultat
        return Response(data)

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

            trader = Trader.objects.filter(telephone=telephone)
            if str(trader) != "<PolymorphicQuerySet []>":
                serializer = TraderSerializer(trader[0])
                type_client = "trader"

        except Membre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        if serializer != None:
            data["client"] = serializer.data
        data["type_client"] = type_client
        return Response(data)

class ParticulierViewSet(viewsets.ModelViewSet):

    queryset = ConsommateurParticulier.objects.all()
    serializer_class = ParticulierSerializer
    lookup_field = "telephone"

    def list(self, request):
        queryset = ConsommateurParticulier.objects.all()
        serializer = ParticulierSerializer(queryset, many=True)
        data = {}
        data["particuliers"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        try:
            particulier = ConsommateurParticulier.objects.get(telephone= telephone)
        except ConsommateurParticulier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParticulierSerializer(particulier)
        data = {}
        data["particulier"] = serializer.data
        return Response(serializer.data)

class EntrepriseViewSet(viewsets.ModelViewSet):

    queryset = ConsommateurEntreprise.objects.all()
    serializer_class = EntrepriseSerializer
    lookup_field = "telephone"

    def list(self, request):
        queryset = ConsommateurEntreprise.objects.all()
        serializer = EntrepriseSerializer(queryset, many=True)
        data = {}
        data["entreprises"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        queryset = ConsommateurEntreprise.objects.all()
        entreprise = get_object_or_404(queryset, telephone=telephone)
        serializer = EntrepriseSerializer(entreprise)
        data = {}
        data["entreprise"] = serializer.data
        return Response(data)


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

    def list(self, request):
        queryset = EntrepriseCommerciale.objects.all()
        serializer = EntrepriseCommercialeSerializer(queryset, many=True)
        data = {}
        data["vendeurs"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        queryset = EntrepriseCommerciale.objects.all()
        vendeur = get_object_or_404(queryset, telephone=telephone)
        serializer = EntrepriseCommercialeSerializer(vendeur)
        data = {}
        data["vendeur"] = serializer.data
        return Response(data)

class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer
    lookup_field = "telephone"

    def list(self, request):
        queryset = Trader.objects.all()
        serializer = TraderSerializer(queryset, many=True)
        data = {}
        data["traders"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_by_telephone(self, request, telephone=None):
        queryset = Trader.objects.all()
        trader = get_object_or_404(queryset, telephone=telephone)
        serializer = TraderSerializer(trader)
        data = {}
        data["trader"] = serializer.data
        return Response(data)

class TransactionInterComsommateurViewSet(viewsets.ModelViewSet):
    queryset = TransactionInterComsommateur.objects.all()
    serializer_class = TransactionInterComsommateurSerializer
    lookup_field = "numero_envoyeur"

    def list(self, request):
        queryset = TransactionInterComsommateur.objects.all()
        serializer = TransactionInterComsommateurSerializer(queryset, many=True)
        data = {}
        data["transactions"] = serializer.data
        return Response(data)

    def retrieve(self, request, numero_envoyeur=None):
        queryset = TransactionInterComsommateur.objects.all()
        transaction = get_object_or_404(queryset, numero_envoyeur=numero_envoyeur)
        serializer = TransactionInterComsommateurSerializer(transaction)
        data = {}
        data["transaction"] = serializer.data
        return Response(data)

class TransactionCommercialComsommateurViewSet(viewsets.ModelViewSet):
    queryset = TransactionCommercialComsommateur.objects.all()
    serializer_class = TransactionCommercialComsommateurSerializer
    lookup_field = "pk"

    def list(self, request):
        queryset = TransactionCommercialComsommateur.objects.all()
        serializer = TransactionCommercialComsommateurSerializer(queryset, many=True)
        data = {}
        data["transactions"] = serializer.data
        return Response(data)

    def retrieve(self, request, pk=None):
        queryset = TransactionCommercialComsommateur.objects.all()
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionCommercialComsommateurSerializer(transaction)
        data = {}
        data["transaction"] = serializer.data
        return Response(data)

class ConversionTraderViewSet(viewsets.ModelViewSet):
    queryset = ConversionTrader.objects.all()
    serializer_class = ConversionTraderSerializer

    def list(self, request):
        queryset = ConversionTrader.objects.all()
        serializer = ConversionTraderSerializer(queryset, many=True)
        data = {}
        data["conversions"] = serializer.data
        return Response(data)

    def retrieve(self, request, numero_trader=None):
        queryset = ConversionTrader.objects.all()
        conversion = get_object_or_404(queryset, numero_trader=numero_trader)
        serializer = ConversionTraderSerializer(conversion)
        data = {}
        data["conversion"] = serializer.data
        return Response(data)

class ReconversionTraderViewSet(viewsets.ModelViewSet):
    queryset = ReconversionTrader.objects.all()
    serializer_class = ReconversionTraderSerializer

    def list(self, request):
        queryset = ReconversionTrader.objects.all()
        serializer = ReconversionTraderSerializer(queryset, many=True)
        data = {}
        data["reconversions"] = serializer.data
        return Response(data)

    def retrieve(self, request, numero_trader=None):
        queryset = ConversionTrader.objects.all()
        reconversion = get_object_or_404(queryset, numero_trader=numero_trader)
        serializer = ReconversionTraderSerializer(reconversion)
        data = {}
        data["reconversion"] = serializer.data
        return Response(data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        data = {}
        data["notifications"] = serializer.data
        return Response(data)

class PayementConsommateurViewSet(viewsets.ModelViewSet):
    queryset = PayementConsomateur.objects.all()
    serializer_class = PayementConsommateurSerializer

    def list(self, request):
        queryset = PayementConsomateur.objects.all()
        serializer = PayementConsommateurSerializer(queryset, many=True)
        data = {}
        data["payements"] = serializer.data
        return Response(data)

class PayementInterCommercialViewSet(viewsets.ModelViewSet):
    queryset = PayementInterCommercial.objects.all()
    serializer_class = PayementInterCommercialSerializer

    def list(self, request):
        queryset = PayementInterCommercial.objects.all()
        serializer = PayementInterCommercialSerializer(queryset, many=True)
        data = {}
        data["payements"] = serializer.data
        return Response(data)

class CreationParticulierParTraderViewSet(viewsets.ModelViewSet):

    queryset = CreationParticulierParTrader.objects.all()
    serializer_class = CreationParticulierParTraderSerializer
    lookup_field = "id"

class ReactivationClientViewSet(viewsets.ModelViewSet):

    queryset = ReactivationClient.objects.all()
    serializer_class = ReactivationClientSerializer

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

    def list(self, request):
        queryset = Produit.objects.all()
        serializer = ProduitSerializer(queryset, many=True)
        data = {}
        data["produits"] = serializer.data
        return Response(data)

    def retrieve(self, request, code_article=None):
        queryset = Produit.objects.all()
        produit = get_object_or_404(queryset, code_article=code_article)
        serializer = ProduitSerializer(produit)
        data = {}
        data["produit"] = serializer.data
        return Response(data)

class CommandeClientViewSet(viewsets.ModelViewSet):

    queryset = CommandeClient.objects.all()
    serializer_class = CommandeClientSerializer
    lookup_field = "id"

    @action(methods=['get'], detail=False)
    def list_commande(self, request):
        queryset = CommandeClient.objects.all()
        serializer = CommandeClientSerializer(queryset, many=True)
        data = {}
        data["commandes"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_commande_by_numero_vendeur(self, request, id=None):

        commandes=None
        try:
            commandes = CommandeClient.objects.filter(numero_vendeur=id)

        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        serializer = CommandeClientSerializer(commandes, many=True)
        data["commandes"] = serializer.data
        return Response(data)

    @action(methods=['get'], detail=True)
    def get_commande_by_numero_client(self, request, id=None):

        commandes = None
        try:
            commandes = CommandeClient.objects.filter(numero_client=id)

        except CommandeClientSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        serializer = CommandeClientSerializer(commandes, many=True)
        data["commandes"] = serializer.data
        return Response(data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        data = {}
        data["notifications"] = serializer.data
        return Response(data)

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
    lookup_field = "id"

    def list(self, request):
        queryset = VendeurVente.objects.all()
        serializer = VendeuVenteSerializer(queryset, many=True)
        data = {}
        data["vendeurs"] = serializer.data
        return Response(data)

class MessageClientViewSet(viewsets.ModelViewSet):

    queryset = MessageClient.objects.all()
    serializer_class = MessageClientSerializer
    lookup_field = "id"

class VilleViewSet(viewsets.ModelViewSet):

    queryset = Ville.objects.all()
    serializer_class = VilleSerializer
    lookup_field = "id"

class QuartierViewSet(viewsets.ModelViewSet):

    queryset = Quartier.objects.all()
    serializer_class = QuartierSerializer
    lookup_field = "id"

    def list(self, request):
        queryset = Quartier.objects.all()
        serializer = QuartierSerializer(queryset, many=True)
        data = {}
        data["quartiers"] = serializer.data
        return Response(data)
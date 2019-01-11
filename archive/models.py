from django.db import models
from rest_framework.response import Response
from ecommerce.models import Produit
from membre.models import *
from compte.models import CompteConsommateur
from django.db import transaction
from dashboard.models import CreanceMonetaire, TauxAbsorbtionGlobal, ConsommationMensuelMoyenneConsommateurActuel, \
    ConsommationMensuelMoyenneVendeurActuel
from recette.models import Recette


class TransactionInterComsommateur(models.Model):
    """
        La classe Transaction gere les transactions 
        effectuées d'un consommateur à un autre
    """

    envoyeur = models.ForeignKey(Consommateur,
								verbose_name="Expéditeur",
								on_delete=models.CASCADE,
								related_name = "envoyeur_consommateur",
                                null = True ,blank = True,)

    numero_envoyeur = models.CharField(max_length=8,verbose_name ="Numéro de l'envoyeur",null = True)
    
    receveur = models.ForeignKey(Consommateur,
								verbose_name="receveur",
								on_delete=models.CASCADE,
								null = True, blank = True,)

    numero_receveur = models.CharField(max_length=8,verbose_name ="Numéro du bénéficiare",null = True)

    montant_envoyer = models.PositiveIntegerField(verbose_name="Montant transférer")

    date_transaction = models.DateTimeField(auto_now_add = True,verbose_name = "Date de Transaction")

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.envoyeur.compte_consommateur.solde = self.envoyeur.compte_consommateur.solde - self.montant_envoyer
                self.envoyeur.compte_consommateur.save()
                self.receveur.compte_consommateur.solde = self.receveur.compte_consommateur.solde + self.montant_envoyer
                self.receveur.compte_consommateur.save()
                super(TransactionInterComsommateur,self).save(*args, **kwargs)
        else:
            return super(TransactionInterComsommateur,self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Transfert Consommateurs vers Consommateurs'
        verbose_name_plural = 'Transfert Consommateurs vers Consommateurs'

class TransactionCommercialComsommateur(models.Model):
    """
        La classe Transaction gere les transactions 
        effectuées du compte consommateur
        d'un commerciale à un autre
    """
    numero_envoyeur = models.CharField(max_length=8,verbose_name ="Numéro de l'envoyeur",null = True)
    numero_receveur = models.CharField(max_length=8,verbose_name ="Numéro du bénéficiare",null = True)
    envoyeur = models.ForeignKey(EntrepriseCommerciale,verbose_name="Expéditeur",on_delete=models.CASCADE,
								related_name = "envoyeur_commercial",
                                null = True,)
    receveur = models.ForeignKey(Consommateur,verbose_name="Entreprise bénéficiaire",on_delete=models.CASCADE,null = True,)

    montant_envoyer = models.PositiveIntegerField(verbose_name="Montant transférer",null = True)

    solde_apres_transaction = models.PositiveIntegerField(verbose_name="Solde après transaction",null = True)

    date_transaction = models.DateTimeField(auto_now_add = True,verbose_name = "Date de Transaction")

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.envoyeur = EntrepriseCommerciale.objects.get(telephone = self.numero_envoyeur)
                self.receveur = Consommateur.objects.get(telephone = self.numero_receveur)
                if self.envoyeur.compte_entreprise_commercial.compte_business.solde > self.montant_envoyer:
                    self.envoyeur.compte_entreprise_commercial.compte_business.solde -= self.montant_envoyer
                    self.envoyeur.compte_entreprise_commercial.compte_business.save()
                    self.receveur.compte_consommateur.solde = self.receveur.compte_consommateur.solde + self.montant_envoyer
                    self.receveur.compte_consommateur.save()
                    self.solde_apres_transaction = self.envoyeur.compte_entreprise_commercial.compte_consommateur.solde
                    # mettre à jour le total des epound dispo sur compte e-c pour le taux d'absorbtion
                    absorbtion = TauxAbsorbtionGlobal.load()
                    absorbtion.epound_detenus += self.montant_envoyer
                    absorbtion.save()
                    # sauvegarder le transfert
                    return super(TransactionCommercialComsommateur, self).save(*args, **kwargs)
                elif self.envoyeur.compte_entreprise_commercial.compte_consommateur.solde > self.montant_envoyer:
                    self.envoyeur.compte_entreprise_commercial.compte_consommateur.solde -= self.montant_envoyer
                    self.envoyeur.compte_entreprise_commercial.compte_consommateur.save()
                    self.receveur.compte_consommateur.solde = self.receveur.compte_consommateur.solde + self.montant_envoyer
                    self.receveur.compte_consommateur.save()
                    self.solde_apres_transaction = self.envoyeur.compte_entreprise_commercial.compte_consommateur.solde
                    #mettre à jour le total des epound dispo sur compte e-c pour le taux d'absorbtion
                    absorbtion = TauxAbsorbtionGlobal.load()
                    absorbtion.epound_detenus += self.montant_envoyer
                    absorbtion.save()
                    #sauvegarder le transfert
                    return super(TransactionCommercialComsommateur,self).save(*args, **kwargs)
                else:
                    return TransactionCommercialComsommateur.objects.none()
        else:
            return super(TransactionCommercialComsommateur,self).save(*args, **kwargs)
			

    class Meta:
        verbose_name = 'Transfert Commercial vers Consommateur'
        verbose_name_plural = 'Transferts Commercials vers Consommateurs'

class PayementConsomateur(models.Model):
    """
        Cette classe gère les payement effectués par
        les consommateurs à l'égard des vendeurs
    """
    telephone_envoyeur = models.CharField(max_length=8,verbose_name="Téléphone de l'envoyeur",null=True)
    telephone_receveur = models.CharField(max_length=8,verbose_name="Téléphone du receveur",null=True)

    envoyeur_code = models.PositiveIntegerField(verbose_name ="Code membre de l'envoyeur",null = True)
    
    receveur_code = models.PositiveIntegerField(verbose_name ="Code membre du bénéficiare",null = True)

    envoyeur = models.ForeignKey(Consommateur,
								verbose_name="Expéditeur",
								on_delete=models.CASCADE,
								null = True,)

    receveur = models.ForeignKey(EntrepriseCommerciale,
								verbose_name="Entreprise bénéficiaire",
								on_delete=models.CASCADE,
								related_name = "receveur_commercial",
                                null = True,)

    montant_envoyer = models.PositiveIntegerField(verbose_name="Montant transférer",null = True)

    solde_apres_transaction = models.PositiveIntegerField(verbose_name="Solde après transaction",null = True)

    date_transaction = models.DateTimeField(auto_now_add = True,verbose_name = "Date de Transaction")

    class Meta:
        verbose_name = "Transaction consommateur vers vendeur"
        verbose_name_plural = "Transactions consommateurs vers vendeurs"


    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.receveur = EntrepriseCommerciale.objects.get(telephone = self.telephone_receveur)
                self.envoyeur = Consommateur.objects.get(telephone = self.telephone_envoyeur)
                self.receveur.compte_entreprise_commercial.compte_business.solde += self.montant_envoyer
                self.receveur.compte_entreprise_commercial.compte_business.save()
                self.envoyeur.compte_consommateur.solde -= self.montant_envoyer
                self.envoyeur.compte_consommateur.save()
                self.solde_apres_transaction = self.receveur.compte_entreprise_commercial.compte_business.solde
                # mettre à jour le total des epound dispo sur compte e-c pour le taux d'absorbtion
                absorbtion = TauxAbsorbtionGlobal.load()
                absorbtion.epound_detenus -= self.montant_envoyer
                absorbtion.epound_consommer += self.montant_envoyer
                absorbtion.save()
                # Creer et enregister la recette effectuer
                recette = Recette(entreprise=self.receveur, recette=self.montant_envoyer,
                                  prelevement=self.montant_envoyer * 0.05,
                                  creance=(self.montant_envoyer - (self.montant_envoyer * 0.05)) * 0.7)
                recette.save()
                # Mise à jour de la consommation mensuel moyenne des consomateurs
                conso_moy = ConsommationMensuelMoyenneConsommateurActuel.load()
                conso_moy.epound_utiliser += self.montant_envoyer
                conso_moy.save()
                # enrégistrement du payement
                super(PayementConsomateur,self).save(*args, **kwargs)

        else:
            return super(PayementConsomateur,self).save(*args, **kwargs)

class PayementInterCommercial(models.Model):
    """
        Cette classe gere les payemements effectués
        du compte consommateurs d'un vendeur
        vers le compte vendeur d'un autre
    """

    numero_envoyeur = models.CharField(max_length=8, verbose_name="Numéro de l'envoyeur", null=True)
    numero_receveur = models.CharField(max_length=8, verbose_name="Numéro du bénéficiare", null=True)

    envoyeur = models.ForeignKey(EntrepriseCommerciale,
								verbose_name="Entreprise Expéditeur",
								on_delete=models.CASCADE,
								related_name = "entreprise_envoyeur",
                                null = True,)

    receveur = models.ForeignKey(EntrepriseCommerciale,
								verbose_name="Entreprise bénéficiaire",
								on_delete=models.CASCADE,
								related_name = "entreprise_beneficiaire",
                                null = True,)

    montant_envoyer = models.PositiveIntegerField(verbose_name="Montant transférer",null = True)

    solde_apres_transaction = models.PositiveIntegerField(verbose_name="Solde après transaction",null = True)

    date_transaction = models.DateTimeField(auto_now_add = True,verbose_name = "Date de Transaction")

    class Meta:
        verbose_name = "Transaction vendeur vers vendeur"
        verbose_name_plural = "Transactions vendeurs vers vendeurs"

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.receveur = EntrepriseCommerciale.objects.get(telephone = self.numero_envoyeur)
                self.envoyeur = EntrepriseCommerciale.objects.get(telephone = self.numero_receveur)
                self.receveur.compte_entreprise_commercial.compte_business.solde += self.montant_envoyer
                self.receveur.compte_entreprise_commercial.compte_business.save()
                self.envoyeur.compte_entreprise_commercial.compte_consommateur.solde -= self.montant_envoyer
                self.envoyeur.compte_entreprise_commercial.compte_consommateur.save()
                self.solde_apres_transaction = self.receveur.compte_entreprise_commercial.compte_business.solde
                # mettre à jour le total des epound dispo sur compte e-c pour le taux d'absorbtion
                absorbtion = TauxAbsorbtionGlobal.load()
                absorbtion.epound_detenus -= self.montant_envoyer
                absorbtion.epound_consommer += self.montant_envoyer
                absorbtion.save()
                # Creer et enregister la recette effectuer
                recette = Recette(entreprise = self.receveur,recette = self.montant_envoyer,
                                  prelevement = self.montant_envoyer*0.05,
                                  creance = (self.montant_envoyer - (self.montant_envoyer*0.05))*0.7)
                recette.save()
                # Mise a jour de la consommation mensuel moyenne vendeur actuel
                conso_moy = ConsommationMensuelMoyenneVendeurActuel.load()
                conso_moy.epound_utiliser += self.montant_envoyer
                conso_moy.save()
                # save the objects
                super(PayementInterCommercial,self).save(*args, **kwargs)

        else:
            return super(PayementInterCommercial,self).save(*args, **kwargs)

class ConversionTrader(models.Model):
    """
        la Classe ConversionTrader gère les 
        conversions d'argent des consommateurs
        en unités epounds
    """
    numero_trader = models.CharField(max_length=8,verbose_name ="Numéro du trader",null = True)
    
    numero_receveur = models.CharField(max_length=8,verbose_name ="Numéro du Consommateur",null = True)

    trader = models.ForeignKey(Trader,verbose_name="Trader",
								on_delete=models.CASCADE,
                                null = True,)

    consommateur = models.ForeignKey(Consommateur,verbose_name="Consommateur",
                                on_delete=models.CASCADE,
                                null = True,)

    montant_converti = models.PositiveIntegerField(verbose_name="Somme Converti",
                                null = True)

    epounds_transferer = models.PositiveIntegerField(verbose_name="epounds transférer au client",
                                null = True)

    solde_apres_conversion = models.PositiveIntegerField(verbose_name="Solde après Conversion",
                                null = True)

    date_conversion = models.DateTimeField(verbose_name ="Date de conversion",
                                auto_now_add = True,)

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                # Opération sur le trader
                self.trader = Trader.objects.get(telephone = self.numero_trader)
                self.consommateur = Consommateur.objects.get(telephone = self.numero_receveur)
                self.trader.compte_trader.solde = self.trader.compte_trader.solde - self.montant_converti
                self.trader.compte_trader.save()
                # Mise a jour de la création monétaire
                creance_monetaire = CreanceMonetaire.load()
                creance_monetaire.cumul_bonification += self.montant_converti*CompteConsommateur.TAUX_GAIN/100
                creance_monetaire.save()
                # Opération sur le consommateur
                self.epounds_transferer = self.montant_converti+self.montant_converti*CompteConsommateur.TAUX_GAIN/100
                self.consommateur.compte_consommateur.solde += self.epounds_transferer
                self.solde_apres_conversion = self.consommateur.compte_consommateur.solde
                self.consommateur.compte_consommateur.save()
                # mettre à jour le total des epound dispo sur compte e-c pour le taux d'absorbtion
                absorbtion = TauxAbsorbtionGlobal.load()
                absorbtion.epound_detenus += self.epounds_transferer
                absorbtion.save()
                super(ConversionTrader,self).save(*args, **kwargs)
        else:
            return super(ConversionTrader,self).save(*args, **kwargs)

    class Meta:
        verbose_name ='Conversion Trader'
        verbose_name_plural = 'Conversions Traders'

class ReconversionTrader(models.Model):
    """
        Cette classe permet au Trader de gérer les
        reconversions des unités epounds des consommateurs
        en monnaies Local
    """
    numero_trader = models.CharField(max_length=8, verbose_name="Numéro du trader", null=True)

    numero_receveur = models.CharField(max_length=8, verbose_name="Numéro du Consommateur", null=True)

    trader = models.ForeignKey(Trader,verbose_name="Trader",
								on_delete=models.CASCADE,
                                null = True,)

    consommateur = models.ForeignKey(Consommateur,verbose_name="Consommateur",
                                on_delete=models.CASCADE,
                                null = True,)

    epound_reconverti = models.PositiveIntegerField(verbose_name="Unités epouns Reconverties",)

    montant_retourner = models.PositiveIntegerField(verbose_name=" Montant Retourner"
                                                    ,null = True)

    solde_consommateur_apres_reconversion = models.PositiveIntegerField(
        verbose_name ='Solde après Reconversion',null =True)

    date_conversion = models.DateTimeField(verbose_name ="Date de conversion",
                                auto_now_add = True,)

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.consommateur = Consommateur.objects.get(telephone = self.numero_receveur)
                self.trader = Trader.objects.get(telephone=self.numero_trader)
                self.montant_retourner = self.epound_reconverti-self.epound_reconverti*CompteConsommateur.TAUX_PERTE/100
                self.consommateur.compte_consommateur.solde -= self.epound_reconverti
                self.consommateur.compte_consommateur.save()
                self.solde_consommateur_apres_reconversion = self.trader.compte_trader.solde

                # mettre à jour le total des epound dispo sur compte e-c pour le taux d'absorbtion
                absorbtion = TauxAbsorbtionGlobal.load()
                absorbtion.epound_detenus -= self.epound_reconverti
                absorbtion.save()
                super(ReconversionTrader,self).save(*args, **kwargs)
        else:
            return super(ConversionTrader,self).save(*args, **kwargs)

class Notification(models.Model):
    receiver = models.CharField(max_length = 150,null = True)
    message = models.TextField(null = True)
    etat = models.PositiveIntegerField(null = True)
    date_notif = models.DateTimeField(auto_now_add = True,null = True)
    type_notif = models.PositiveIntegerField(null = True)
    sender = models.CharField(max_length = 150,null = True)

class CreationEntrepriseParTrader(models.Model):
    """
        Cette classe gère la création des clients par
        les tradeurs. les informations à passées sont:
        -le numero de télephone
        -le mot de passe du client
    """
    code_trader = models.PositiveIntegerField(verbose_name = "Code du Trader",null = True)
    trader = models.ForeignKey(Trader, on_delete = models.CASCADE,null = True)
    consommateur = models.ForeignKey(ConsommateurEntreprise, on_delete = models.CASCADE,null = True)
    telephone = models.CharField(max_length =8,verbose_name ="Téléphone du client",null = True)
    mdp = models.CharField(max_length = 50,verbose_name = "Mot de passe",null = True)

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.trader = Trader.objects.get(code_membre = self.code_trader)
                self.trader.compte_trader.solde -= 10000
                self.trader.compte_trader.save()
                self.consommateur = ConsommateurEntreprise.objects.create(telephone = self.telephone, mdp =self.mdp)
                super(CreationEntrepriseParTrader,self).save(*args, **kwargs)

class CommandeClient(models.Model):
    """Cette classe gère les commandes effectuées par les clients"""
    numero_client = models.CharField(verbose_name="Numéro du client",max_length=8,null=True)
    client = models.ForeignKey(Consommateur,on_delete=models.CASCADE,null=True)
    numero_vendeur = models.CharField(verbose_name="Numéro du vendeur",max_length=8,null=True)
    vendeur = models.ForeignKey(EntrepriseCommerciale,on_delete=models.CASCADE,null=True)
    code_produit = models.CharField(max_length=100,verbose_name="Code de l'article",blank=True)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE,null=True)
    quantite = models.PositiveIntegerField(verbose_name="Quantité",null=True)
    a_livrer = models.BooleanField(verbose_name="Article à liver")
    etat = models.PositiveIntegerField(default=0)
    valider = models.BooleanField(verbose_name="Valider",default=False)
    date_commande = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.client = Consommateur.objects.get(telephone = self.numero_client)
                self.vendeur = EntrepriseCommerciale.objects.get(telephone = self.numero_vendeur)
                self.produit = Produit.objects.get(code_article = self.code_produit)
                if self.client.compte_consommateur.solde < self.produit.prix:
                    msg  = "Montant insuffusant pour effectuer cette commande"
                    print(msg)
                    data = {}
                    data['msg'] = msg
                    return Response(data['msg'])
                else:
                    self.client.compte_consommateur.solde -= self.quantite*self.produit.prix
                    self.client.compte_consommateur.save()
                if self.a_livrer:
                    self.vendeur = EntrepriseCommerciale.objects.get(telephone = "22222222")
                super(CommandeClient,self).save(*args, **kwargs)
        else:
            return super(CommandeClient,self).save(*args, **kwargs)

class VendeurVente(models.Model):

    """Cette classe gère les ventes réaliser par les vendeur
    """
    numero_acheteur = models.CharField(max_length=8,verbose_name="Numéro de l'acheteur",null=True)
    mdp_acheteur = models.CharField(max_length = 50,verbose_name = "Mot de passe client",null = True)
    numero_vendeur = models.CharField(max_length=8,verbose_name="Numéro du vendeur",null=True)
    acheteur = models.ForeignKey(Consommateur,on_delete=models.CASCADE,null=True)
    vendeur = models.ForeignKey(EntrepriseCommerciale,on_delete=models.CASCADE,null=True)
    montant = models.PositiveIntegerField(verbose_name="Montant",null=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.client = Consommateur.objects.get(telephone = self.numero_acheteur)
                self.vendeur = EntrepriseCommerciale.objects.get(telephone = self.numero_vendeur)
                if self.client.compte_consommateur.solde > self.montant:
                    self.client.compte_consommateur.solde -= self.montant
                    self.client.compte_consommateur.save()
                    self.vendeur.compte_entreprise_commercial.compte_consommateur.solde += self.montant
                    self.vendeur.compte_entreprise_commercial.compte_consommateur.save()
                    super(VendeurVente,self).save(*args, **kwargs)
                else:
                    return None

class ReactivationClient(models.Model):

    numero_trader = models.CharField(max_length=8, verbose_name="Numéro du trader", null=True)

    numero_receveur = models.CharField(max_length=8, verbose_name="Numéro du Consommateur", null=True)

    trader = models.ForeignKey(Trader, verbose_name="Trader",
                               on_delete=models.CASCADE,
                               null=True, )

    consommateur = models.ForeignKey(Consommateur, verbose_name="Consommateur",
                                     on_delete=models.CASCADE,
                                     null=True, )

    date_reabonnement = models.DateTimeField(verbose_name="Date de réabonnement",
                                           auto_now_add=True, )

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                # Opération sur le trader
                self.trader = Trader.objects.get(telephone=self.numero_trader)
                self.consommateur = Consommateur.objects.get(telephone=self.numero_receveur)
                self.trader.compte_trader.solde = self.trader.compte_trader.solde - 5
                self.trader.compte_trader.save()
                # Opération sur le consommateur
                self.consommateur.actif = True
                self.consommateur.save()
                super(ReactivationClient, self).save(*args, **kwargs)
        else:
            return super(ReactivationClient, self).save(*args, **kwargs)

class MessageClient(models.Model):
    """
        Cette classe permet aux utilisateur de nous envoyer des méssage ou des suggestions
    """
    telephone = models.CharField(max_length=8, verbose_name="Téléphone du client", null=True)
    message = models.TextField(verbose_name="Contenu du méssage", null=True)
    date_envoye = models.DateTimeField(auto_now_add=True,null=True)

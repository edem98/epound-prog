from django.db import models

from dashboard.models import CreanceMonetaire
from membre.models import Membre,Trader,Consommateur, ConsommateurParticulier
from django.contrib.auth.models import User
from compte.models import CompteAlpha
from django.db import transaction
from django.contrib.auth.hashers import check_password


class EmissionUnites(models.Model):
    """cette classe permet de vendre des unités e-pounds aux traders et aux gros consommateurs"""

    operateur = models.ForeignKey(User, verbose_name='Opérateur',
                                  on_delete=models.CASCADE,
                                  related_name='emeteur',
                                  null=True,
                                  blank=False)

    beneficiaire = models.ForeignKey(Membre, verbose_name="Bénéficiaire",
                                     on_delete=models.DO_NOTHING, )
    montant_debouse = models.PositiveIntegerField(verbose_name="Montant déboursé")
    unite_epound_correspondant = models.PositiveIntegerField(verbose_name="e-pounds correspondant")
    mdp = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")

    def save(self, *args, **kwargs):
        egaux = check_password(self.mdp, self.operateur.password)
        if egaux == True:
            compte_alpha = CompteAlpha.load()
            if 'compte_trader_id' in self.beneficiaire.__dict__:
                compte_alpha.solde -= self.montant_debouse
                compte_alpha.save()
                compte_trader = self.beneficiaire.compte_trader
                compte_trader.solde += self.unite_epound_correspondant
                compte_trader.save()
            elif 'compte_consommateur_id' in self.beneficiaire.__dict__:
                compte_alpha.solde -= self.montant_debouse
                print(str(compte_alpha.solde))
                compte_alpha.save()
                compte_consommateur = self.beneficiaire.compte_consommateur
                compte_consommateur.solde += self.unite_epound_correspondant
                compte_consommateur.save()
        super(EmissionUnites, self).save(*args, **kwargs)  # On enregistre la nouvelle instance.

    class Meta():
        verbose_name = "Emission d'unité"
        verbose_name_plural = "Emission d'unités"

class EmissionSurCompteAlpha(models.Model):

    utilisateur = models.ForeignKey(User, verbose_name='Utilisateur',on_delete=models.CASCADE,null=True,blank=False)
    montant = models.PositiveIntegerField(verbose_name="Montant Emit")
    password = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")
    date_emission = models.DateTimeField(auto_now_add=True,)

    def save(self, *args, **kwargs):
        compte_alpha = CompteAlpha.load()
        print(compte_alpha.solde)
        print(self.montant)
        compte_alpha.solde += self.montant
        compte_alpha.save()
        print(compte_alpha.solde)
        super(EmissionSurCompteAlpha, self).save(*args, **kwargs)

class EmissionSurCompteTrader(models.Model):

    utilisateur = models.ForeignKey(User, verbose_name='Utilisateur',on_delete=models.CASCADE,null=True,blank=False)
    trader = models.ForeignKey(Trader, verbose_name="Bénéficiaire",on_delete=models.CASCADE,null=True,blank=False)
    montant = models.PositiveIntegerField(verbose_name="Montant Emit")
    bonification = models.PositiveIntegerField(verbose_name="Bonnification",editable=False,)
    password = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")
    date_emission = models.DateTimeField(auto_now_add=True,)

    def save(self, *args, **kwargs):
        compte_alpha = CompteAlpha.load()
        self.bonification = self.montant*0.1
        compte_alpha.solde -= self.montant+self.bonification
        compte_alpha.save()
        self.trader.compte_trader.solde += self.montant + self.bonification
        self.trader.compte_trader.save()
        super(EmissionSurCompteTrader, self).save(*args, **kwargs)

class EmissionSurCompteConsommateur(models.Model):
    """
            La class EmissionSurCompteConsommateur permet aux Trader Interne
            d'effectués des Conversions.
        """

    trader = models.ForeignKey(Trader, verbose_name="Trader",on_delete=models.CASCADE,null=True,blank=False)
    consommateur = models.ForeignKey(Consommateur, verbose_name='Consommateur',on_delete=models.CASCADE,null=True,blank=False)
    montant = models.PositiveIntegerField(verbose_name="Montant Emit")
    bonification = models.PositiveIntegerField(verbose_name="Bonnification",editable=False,)
    password = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")
    date_emission = models.DateTimeField(auto_now_add=True,)

    def save(self, *args, **kwargs):
        self.bonification = self.montant*0.5
        #retrait de l'argent au trader
        self.trader.compte_trader.solde -= self.montant
        self.trader.compte_trader.save()
        # Mise a jours de la créance moétaire
        creance = CreanceMonetaire.load()
        creance.cumul_bonification += self.bonification
        creance.save()
        # ajout des unités epounds et de la bonnification au consommateur
        self.consommateur.compte_consommateur.solde += self.montant+self.bonification
        self.consommateur.compte_consommateur.save()
        super(EmissionSurCompteConsommateur, self).save(*args, **kwargs)

class CreationParticulierParTrader(models.Model):
    """
        Cette classe gère la création des clients par
        les tradeurs. les informations à passées sont:
        -le numero de télephone
        -le mot de passe du client
    """
    numero_trader = models.CharField(max_length=8,verbose_name = "Numero du Trader",null = True)
    solde_initial = models.PositiveIntegerField(verbose_name = "Solde initial du Trader",null = True,editable=False)
    trader = models.ForeignKey(Trader, on_delete = models.CASCADE,null = True)
    consommateur = models.ForeignKey(ConsommateurParticulier, on_delete = models.CASCADE,null = True)
    telephone = models.CharField(max_length =8,verbose_name ="Téléphone du client",null = True)
    date_emission = models.DateTimeField(auto_now_add=True,)



    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.trader = Trader.objects.get(telephone = self.numero_trader)
                self.solde_initial = self.trader.compte_trader.solde
                self.trader.compte_trader.solde -= 3000
                self.trader.compte_trader.save()
                self.consommateur = ConsommateurParticulier.objects.create(telephone = self.telephone, mdp ="123456789")
                super(CreationParticulierParTrader,self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Adhésion"
        verbose_name_plural = "Adhésions"
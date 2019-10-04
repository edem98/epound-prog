from django.db import models
from dashboard.models import CreanceMonetaire
from membre.models import Membre, Trader, Consommateur, ConsommateurParticulier
from django.contrib.auth.models import User
from compte.models import CompteAlpha
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.contrib.auth.base_user import BaseUserManager
from utils import envoyer_sms


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
    utilisateur = models.ForeignKey(User, verbose_name='Utilisateur', on_delete=models.CASCADE, null=True, blank=False)
    montant = models.PositiveIntegerField(verbose_name="Montant Emit")
    password = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")
    date_emission = models.DateTimeField(auto_now_add=True, )

    def save(self, *args, **kwargs):
        compte_alpha = CompteAlpha.load()
        print(compte_alpha.solde)
        print(self.montant)
        compte_alpha.solde += self.montant
        compte_alpha.save()
        print(compte_alpha.solde)
        super(EmissionSurCompteAlpha, self).save(*args, **kwargs)


class EmissionSurCompteTrader(models.Model):
    utilisateur = models.ForeignKey(User, verbose_name='Utilisateur', on_delete=models.CASCADE, null=True, blank=False)
    trader = models.ForeignKey(Trader, verbose_name="Bénéficiaire", on_delete=models.CASCADE, null=True, blank=False)
    montant = models.PositiveIntegerField(verbose_name="Montant Emit")
    bonification = models.PositiveIntegerField(verbose_name="Bonnification", editable=False, )
    password = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")
    date_emission = models.DateTimeField(auto_now_add=True, )

    def save(self, *args, **kwargs):
        compte_alpha = CompteAlpha.load()
        self.bonification = self.montant * 0.1
        compte_alpha.solde -= self.montant + self.bonification
        compte_alpha.save()
        self.trader.compte_trader.solde += self.montant + self.bonification
        self.trader.compte_trader.save()
        super(EmissionSurCompteTrader, self).save(*args, **kwargs)


class EmissionSurCompteConsommateur(models.Model):
    """
            La class EmissionSurCompteConsommateur permet aux Trader Interne
            d'effectués des Conversions.
        """

    trader = models.ForeignKey(Trader, verbose_name="Trader", on_delete=models.CASCADE, null=True, blank=False)
    consommateur = models.ForeignKey(Consommateur, verbose_name='Consommateur', on_delete=models.CASCADE, null=True,
                                     blank=False)
    montant = models.PositiveIntegerField(verbose_name="Montant Emit")
    bonification = models.PositiveIntegerField(verbose_name="Bonnification", editable=False, )
    password = models.CharField(max_length=100, verbose_name="Confirmez votre mot de passe")
    date_emission = models.DateTimeField(auto_now_add=True, )

    def save(self, *args, **kwargs):
        self.bonification = self.montant * 0.5
        # retrait de l'argent au trader
        self.trader.compte_trader.solde -= self.montant
        self.trader.compte_trader.save()
        # Mise a jours de la créance moétaire
        creance = CreanceMonetaire.load()
        creance.cumul_bonification += self.bonification
        creance.save()
        # ajout des unités epounds et de la bonnification au consommateur
        self.consommateur.compte_consommateur.solde += self.montant + self.bonification
        self.consommateur.compte_consommateur.save()
        super(EmissionSurCompteConsommateur, self).save(*args, **kwargs)


class CreationParticulierParTrader(models.Model):
    """
        Cette classe gère la création des clients par
        les tradeurs. les informations à passées sont:
        -le numero de télephone
        -le mot de passe du client
    """
    numero_trader = models.CharField(max_length=8, verbose_name="Numero du Trader", null=True)
    solde_initial = models.PositiveIntegerField(verbose_name="Solde initial du Trader", null=True, editable=False)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, null=True)
    consommateur = models.ForeignKey(ConsommateurParticulier, on_delete=models.CASCADE, null=True, blank=True)
    telephone = models.CharField(max_length=8, verbose_name="Téléphone du client", null=True)
    date_emission = models.DateTimeField(auto_now_add=True, )

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                self.solde_initial = self.trader.compte_trader.solde
                self.trader.compte_trader.solde -= 1000
                self.trader.compte_trader.save()
                # Génération du code membre et du password du nouveau client
                code_membre = Membre.objects.all().order_by("-id")[0]
                code_membre = code_membre.id + 1
                password = BaseUserManager().make_random_password(5)
                # Création de particuler
                self.consommateur = ConsommateurParticulier(telephone=self.telephone, mdp=password,
                                                            code_membre=code_membre)
                self.consommateur.save()
                # Création du méssage et envoie du méssage
                message = "Bienvenue sur epound\n" + "code membre: " + str(
                    self.consommateur.code_membre) + "\nmot de passe: " + password
                to = "228" + self.telephone
                envoyer_sms(message, to)
                # Retourner l'élément creer
                super(CreationParticulierParTrader, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Adhésion"
        verbose_name_plural = "Adhésions"


class CreationParticulierParTraderEtIntegrateur(models.Model):
    """
        Cette classe gère la création de clients ayant ete integrer
        par un membre du reseau. l' operation est effectuer par
        les tradeurs et le membre integrateur beneficie de 500 epounds de bonus
        . les informations à passées sont:
        -le numero de télephone de l'integrateur
        - le numero de telephone du nouveau client
        -le mot de passe du trader
    """
    numero_trader = models.CharField(max_length=8, verbose_name="Numero du Trader", null=True)
    numero_integrateur = models.CharField(max_length=8, verbose_name="Numero de l'integrateur", null=True)
    telephone = models.CharField(max_length=8, verbose_name="Téléphone du client", null=True)
    solde_initial = models.PositiveIntegerField(verbose_name="Solde initial du Trader", null=True, editable=False)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, null=True)
    integrateur = models.ForeignKey(ConsommateurParticulier, on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='ancient')
    consommateur = models.ForeignKey(ConsommateurParticulier, on_delete=models.CASCADE, null=True,
                                     blank=True, related_name='new')
    date_emission = models.DateTimeField(auto_now_add=True, )

    def save(self, *args, **kwargs):
        if self.id == None:
            with transaction.atomic():
                if ConsommateurParticulier.objects.filter(pk=self.integrateur.pk).exists():
                    # prelevement sur compte trader
                    self.solde_initial = self.trader.compte_trader.solde
                    self.trader.compte_trader.solde -= 1000
                    self.trader.compte_trader.save()
                    # Retrait de 500 epounds du tradeur integrateur
                    tradeur_integrateur = Trader.objects.get(code_membre=367)
                    tradeur_integrateur.compte_trader.solde -= 500
                    tradeur_integrateur.compte_trader.save()
                    # bonus de 500 epounds pour l'integrateur
                    self.integrateur.compte_consommateur.solde += 500
                    self.integrateur.compte_consommateur.save()
                    # Génération du code membre et du password du nouveau client
                    code_membre = Membre.objects.all().order_by("-id")[0]
                    code_membre = code_membre.id + 1
                    password = BaseUserManager().make_random_password(5)
                    # Création de particuler
                    self.consommateur = ConsommateurParticulier(telephone=self.telephone, mdp=password,
                                                                code_membre=code_membre)
                    self.consommateur.save()
                    # Création du méssage et envoie du méssage
                    message = "Bienvenue sur epound\n" + "code membre: " + str(
                        self.consommateur.code_membre) + "\nmot de passe: " + password
                    to = "228" + self.telephone
                    envoyer_sms(message, to)
                    # Retourner l'élément creer
                    super(CreationParticulierParTraderEtIntegrateur, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Adhésion par membre"
        verbose_name_plural = "Adhésions par membres"

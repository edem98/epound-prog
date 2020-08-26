from django.db import models
from polymorphic.models import PolymorphicModel
from membre.models import *
from utils import TimeStamp
from utils import SingletonModel
import datetime


class CompteAlpha(SingletonModel):
    proprietaire = models.CharField(max_length=100, verbose_name="Propriétaire du compte",
                                    default='e-pounds Corporation')
    solde = models.PositiveIntegerField(verbose_name="Solde e-pounds", default=10000000)

    def __str__(self):
        return "Compte Alpha"

    class Meta():
        verbose_name = "Compte Alpha"
        verbose_name_plural = "Compte Alpha"


class CompteBeta(SingletonModel):
    proprietaire = models.CharField(max_length=100, verbose_name="Propriétaire du compte",
                                    default='e-pounds Corporation')
    solde = models.PositiveIntegerField(verbose_name="Solde e-pounds", default=10000000)

    def __str__(self):
        return "Compte Bêta"

    class Meta():
        verbose_name = "Compte Bêta"
        verbose_name_plural = "Compte Bêta"


class CompteGrenier(SingletonModel):
    fonte = models.PositiveIntegerField(verbose_name="Fonte", null=True)
    prelevement_reconversion = models.PositiveIntegerField(verbose_name="Prélevement sur Reconversion", null=True)
    prelevement_vendeur = models.PositiveIntegerField(verbose_name="Prélevement sur Vendeur", null=True)
    montant_reconverti_local = models.PositiveIntegerField(verbose_name="cumul des 70% des reconversions vendeurs",
                                                           null=True)
    recette = models.PositiveIntegerField(verbose_name="Destruction Monaitaire", default=0)

    def __str__(self):
        return "Compte Grenier"

    class Meta():
        verbose_name = "Compte Grenier"
        verbose_name_plural = "Compte Grenier"


class Compte(PolymorphicModel, TimeStamp):
    solde = models.PositiveIntegerField(default=0)
    date_expiration = models.DateField(verbose_name="Date d'expiration", null=True, blank=True)
    actif = models.BooleanField(verbose_name='En activité', default=True, )

    def __str__(self):
        return "Compte :" + str(self.id)

    class Meta():
        verbose_name = "Compte"

    def save(self, *args, **kwargs):
        # recuperation de l'entreprise associér a ce compte
        if self.id == None:
            super(Compte, self).save(*args, **kwargs)
            self.date_expiration = self.date_add.date() + datetime.timedelta(720)
            self.save()
        else:
            self.save()
            return super(Compte, self).save(*args, **kwargs)


class CompteTrader(Compte):
    taux_gain = models.FloatField(verbose_name="Taux d'intérêt",
                                  editable=False, default=1.1)
    class Meta():
        verbose_name = "Compte Trader"


class CompteConsommateur(Compte):
    TAUX_GAIN = 25
    TAUX_PERTE = 28
    TAUX_FONTE_MENSUEL = 2
    DEPENSE_MAX_MENSUEL = 100000
    depense_epound_mensuel = models.PositiveIntegerField(verbose_name="Depense mensuel", default=0, )

    class Meta():
        verbose_name = "Compte Consommateur"


class CompteBusiness(Compte):
    TAUX_CONTRIBUTION = 5
    TAUX_RECONVERSION = 70

    class Meta():
        verbose_name = 'Compte Vente'

# def titulaire(self):
# 	print(self.id)
# 	from membre.models import EntrepriseCommerciale
# 	compte_entreprise = CompteEntrepriseCommerciale.objects.get(compte_business__id=self.id)
# 	entreprise = EntrepriseCommerciale.objects.get(compte_entreprise_commercial=compte_entreprise)
# 	return entreprise.nom
#
# def __str__(self):
# 	s = self.titulaire()
# 	return s


class CompteEntrepriseCommerciale(Compte):
    compte_consommateur = models.OneToOneField(CompteConsommateur,
                                               verbose_name="Compte Achat",
                                               on_delete=models.CASCADE,
                                               related_name="conso_vers_entreprise")
    compte_business = models.OneToOneField(CompteBusiness,
                                           verbose_name="Compte Vente",
                                           on_delete=models.CASCADE,
                                           related_name="vente_vers_entreprise")
    credit = models.PositiveIntegerField(verbose_name="Credit", default=0)
    TAUX_REMBOURSEMENT = 0

    def delete(self, *args, **kwargs):
        # suppression du compte associér a ce vendeur
        self.compte_consommateur.delete()
        self.compte_business.delete()
        super(CompteEntrepriseCommerciale, self).delete(*args, **kwargs)

    class Meta():
        verbose_name = "Compte Entreprise Commerciale"

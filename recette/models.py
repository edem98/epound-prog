from django.db import models
from membre.models import EntrepriseCommerciale

class Recette(models.Model):
    """
    Cette classe enrégistres les données relatives aux recettes effectuées par
    les vendeurs mensuellemnt
    """

    entreprise = models.ForeignKey(EntrepriseCommerciale,verbose_name="Entreprise",on_delete=models.CASCADE,null=True)
    recette = models.PositiveIntegerField(verbose_name="Recette",null=True)
    prelevement = models.PositiveIntegerField(verbose_name="Prélevement",null=True)
    creance = models.PositiveIntegerField(verbose_name="Créance dûe")
    date_recette = models.DateTimeField(verbose_name="Date de la recette",auto_now_add=True,)

    class Meta:
        verbose_name = "Recette Journalière"
        verbose_name_plural = "Recettes Journalières"
        ordering = ['entreprise', '-date_recette',]


class RecetteMensuel(models.Model):
    """
    Cette classe enrégistres les données relatives aux recettes effectuées par
    les vendeurs
    """
    Janvier = 'Janvier'
    Février = 'Reserver'
    Mars = 'Mars'
    Avril = 'Avril'
    Mai = 'Mai'
    Juin = 'Juin'
    Juillet = 'Juillet'
    Aout = 'Août'
    Septembre = 'Septembre'
    Octobre = 'Octobre'
    Novembre = 'Novembre'
    Decembre = 'Décembre'

    MOIS = [
        (Janvier, 'Janvier'),
        (Février, 'Février'),
        (Mars, 'Mars'),
        (Avril, 'Avril'),
        (Mai, 'Mai'),
        (Juin, 'Juin'),
        (Juillet, 'Juillet'),
        (Aout, 'Août'),
        (Septembre, 'Septembre'),
        (Octobre, 'Octobre'),
        (Novembre, 'Novembre'),
        (Decembre, 'Décembre'),
    ]

    entreprise = models.ForeignKey(EntrepriseCommerciale,verbose_name="Entreprise",on_delete=models.CASCADE,null=True)
    recette = models.PositiveIntegerField(verbose_name="Recette",null=True)
    prelevement = models.PositiveIntegerField(verbose_name="Prélevement",null=True)
    creance = models.PositiveIntegerField(verbose_name="Créance dûe")
    mois = models.CharField(max_length=50,verbose_name="Mois", choices=MOIS,null=True)
    date_recette = models.DateTimeField(verbose_name="Date ",auto_now_add=True,)

    class Meta:
        verbose_name = "Recette Mensuel"
        verbose_name_plural = "Recettes Mensuels"
        ordering = ['entreprise', '-date_recette',]

class RecetteAnnuel(models.Model):
    """
    Cette classe enrégistres les données relatives aux recettes effectuées par
    les vendeurs annuellement
    """

    entreprise = models.ForeignKey(EntrepriseCommerciale,verbose_name="Entreprise",on_delete=models.CASCADE,null=True)
    recette = models.PositiveIntegerField(verbose_name="Recette",null=True)
    prelevement = models.PositiveIntegerField(verbose_name="Prélevement",null=True)
    creance = models.PositiveIntegerField(verbose_name="Créance dûe")
    date_recette = models.DateTimeField(verbose_name="Date ",auto_now_add=True,)

    class Meta:
        verbose_name = "Recette Annuelle"
        verbose_name_plural = "Recettes Annuelles"
        ordering = ['entreprise', '-date_recette',]
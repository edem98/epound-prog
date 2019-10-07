from celery.decorators import task
from django.utils import timezone
from utils import CorrespondanceMois
from .models import *

@task
def reinitialiserTauxAbsorbtionGlobal():
    """
        Cette fonction réinitialise le taux d'absotion global
        en remettant a 0 le total epound consommer au cous du mois
    :return: str(done)
    """
    correspondance = CorrespondanceMois()
    absortion_actuel = TauxAbsorbtionGlobal.load()
    absortion_actuel.epound_consommer = 1
    absortion_actuel.mois = correspondance.correspondre(timezone.now().month)
    absortion_actuel.save()
    return print("...done")

@task
def updateMoisConsommationMoyenneMensuelGlobal():
    """
        Cette fonction met a jour le mois de l'Objet
        singleton permetant de garder la valeur  de la
        consommation moyenne mensuel actuel
    :return: str(...done)
    """
    correspondance = CorrespondanceMois()
    conso_global = ConsommationMensuelMoyenneConsommateurActuel.load()
    conso_global.mois = correspondance.correspondre(timezone.now().month)
    conso_global.save()
    return print("...done")

@task
def updateMoisVendeurMoyenneMensuelGlobal():
    """
        Cette fonction met a jour le mois de l'Objet
        singleton permetant de garder la valeur  de la
        consommation moyenne mensuel actuel
    :return: str(...done)
    """
    correspondance = CorrespondanceMois()
    conso_global = ConsommationMensuelMoyenneVendeurActuel.load()
    conso_global.mois = correspondance.correspondre(timezone.now().month)
    conso_global.save()
    return print("...done")

@task
def sauvegarderTauxAbsorbtionMensuel():
    """
        Cette fonction est une tâche période qui
        permet de faire des sauvegarde mensuels du taux d'absorbtion
    :return: fonction (reinitialiserTauxAbsorbtionGlobal)
    """

    absortion_actuel = TauxAbsorbtionGlobal.load()
    absortion_mensuel = TauxAbsorbtionGlobalMensuel(epound_detenus = absortion_actuel.epound_detenus,
                                                    epound_consommer = absortion_actuel.epound_consommer,
                                                    mois = absortion_actuel.mois)
    absortion_mensuel.save()
    return  reinitialiserTauxAbsorbtionGlobal()

@task
def sauvegarderConsommationMensuelMoyenneConsommateur():

    conso_global = ConsommationMensuelMoyenneConsommateurActuel.load()
    date = timezone.now().date() - conso_global.date_debut_consommation
    conso_mois = ConsommationMensuelMoyenneConsommateur(mois = conso_global.mois,epound_utiliser = conso_global.epound_utiliser,
                                                        nombre_mois=int(date.days / 30))
    return  updateMoisConsommationMoyenneMensuelGlobal()

@task
def sauvegarderVendeurMensuelMoyenneConsommateur():

    conso_global = ConsommationMensuelMoyenneVendeurActuel.load()
    date = timezone.now().date() - conso_global.date_debut_consommation
    conso_mois = ConsommationMensuelMoyenneVendeur(mois = conso_global.mois,epound_utiliser=conso_global.epound_utiliser,
                                                   nombre_mois = int(date.days / 30))
    return  updateMoisVendeurMoyenneMensuelGlobal()
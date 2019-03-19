from celery.decorators import task
from django.utils import timezone

from compte.models import CompteConsommateur
from membre.models import Consommateur

@task
def deductionensuelCompteConsommatesur():
    """
        Cette fonction deduit de facon automatique et mensuelement
        2 % du solde du compte de tout les consommateurs
    """
    consommateurs = Consommateur.objects.all()
    for consommateur in consommateurs:
        if consommateur.compte_consommateur.solde > 0:
            consommateur.compte_consommateur.solde *= 0.98
    return print("...done")

@task
def reinitialiser_depense_annuel():
    """
        Cette fonction met a zero la depenses mensuels des comptes consomateurs des membres
    """
    comptes = CompteConsommateur.objects.filter(actif = True)
    for compte in comptes:
        compte.depense_epound_mensuel = 0
        compte.save()
    return print("...done")


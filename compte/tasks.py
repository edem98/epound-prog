from celery.decorators import task
from django.utils import timezone
from membre.models import Consommateur

@task
def deductionensuelCompteConsommateur():
    """
        Cette fonction deduit de facon automatique et mensuelement
        2 % du solde du compte de tout les consommateurs
    """
    consommateurs = Consommateur.objects.all()
    for consommateur in consommateurs:
        if consommateur.compte_consommateur.solde > 0:
            consommateur.compte_consommateur.solde *= 0.98
    return print("...done")


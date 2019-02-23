from celery.decorators import task
from django.utils import timezone
from .models import Membre

@task
def desactiver_membre():
    """
        Cette fonction desactive les membre n'ayant pas renouveler leur abonement
    """
    cible = Membre.objects.filter(date_desactivation = timezone.now().date())
    for membre in cible:
        membre.actif = False
    return print("...done")

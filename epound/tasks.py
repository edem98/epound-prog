
from celery.decorators import task
from celery import shared_task
# We can have either registered task
@shared_task
def hello():
     return "premier setup d'une tache asynchrone"


@shared_task
def add(x, y):
    print(x + y)
    return x + y



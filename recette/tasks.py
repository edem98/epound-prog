
from celery.decorators import task
# We can have either registered task
@task
def hello():
     return "premier setup d'une tache asynchrone"
from django.db import models
import requests

""" from compte import CompteBusiness
from dashboard.models import Creance

COMPTEBUSINESS = CompteBusiness
CREANCE = Creance """


def envoyer_sms(message, destinataire, expediteur="Epound Corporation"):
    """
        Cet controlleur envoie le mot de passe et code membre auc nouveaux utilisateurs
    :type message: string
    :param message: message to send
    :param destinataire: le destinataire du message
    :param expediteur: l4expediteur (Epound corp)
    """
    url = "https://nexmo-nexmo-messaging-v1.p.rapidapi.com/send-sms"

    querystring = {"text": message, "from": expediteur, "to": destinataire}

    payload = ""
    headers = {
        'x-rapidapi-host': "nexmo-nexmo-messaging-v1.p.rapidapi.com",
        'x-rapidapi-key': "48fb167c5dmsh0e4eec0a01639efp1352e8jsn154c9a663649",
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    print(response.text)


class TimeStamp(models.Model):
	date_add = models.DateTimeField(auto_now_add = True,verbose_name = "Date d'ajout")
	date_update = models.DateTimeField(auto_now = True,verbose_name = "Dernière mise à jour")

	class Meta():
		abstract = True


class SingletonModel(models.Model):
	class Meta:
		"""docstring for Meta"""
		abstract = True

	def save(self,*args,**kwargs):
		self.pk = 1
		super(SingletonModel,self).save(*args,**kwargs)

	@classmethod
	def load(cls):
		obj, created = cls.objects.get_or_create(pk = 1)
		if not created:
			return obj
		return created


class CorrespondanceMois():
	"""
		Cette class permet de faire correspondre des chiffres à
		des mois de l'année
	"""
	def __init__(self):
		self.janvier = 1
		self.fevrier = 2
		self.mars = 3
		self.avril = 4
		self.mai = 5
		self.juin = 6
		self.juillet = 7
		self.aout = 8
		self.septembre = 9
		self.octobre = 10
		self.novembre = 11
		self.decembre = 12

	def correspondre(self,mois):
		"""
		methode permettant de faire correspondre un mois
		à un chiffre
		:param mois:
		:return a month in string type
		"""

		if mois == self.janvier:
			return "Janvier"
		elif mois == self.fevrier:
			return  "Février"
		elif mois == self.mars:
			return "Mars"
		elif mois == self.avril:
			return "Avril"
		elif mois == self.mai:
			return "Mai"
		elif mois == self.juin:
			return "Juin"
		elif mois == self.juillet:
			return "Juillet"
		elif mois == self.aout:
			return "Août"
		elif mois == self.septembre:
			return  "Septembre"
		elif mois == self.octobre:
			return "Octobre"
		elif mois == self.novembre:
			return "Novembre"
		elif mois == self.decembre:
			return "Novembre"


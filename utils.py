from django.db import models
from django.core.cache import cache
""" from compte import CompteBusiness
from dashboard.models import Creance

COMPTEBUSINESS = CompteBusiness
CREANCE = Creance """

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

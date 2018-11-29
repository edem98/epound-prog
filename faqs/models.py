from django.db import models

class Sujet(models.Model):
    """
        Cette class définit les sujets qui intéressent
        les utilisateurs recherchant de l'aide
    """
    sujet = models.CharField(max_length =250,verbose_name ="Sujet",null = True)
    slug = models.SlugField(verbose_name="Etiquette",null=True,max_length=80)

    def __str__(self):
        return self.sujet


class ProblemeSolution(models.Model):
    """
        Cette classe expose les préocupations relatives à
        un sujet en particuliers et donne la salution la mieux adapté
    """
    sujet = models.ForeignKey(Sujet, on_delete = models.CASCADE,null = True)
    probleme = models.CharField(max_length =250,verbose_name="Question",null= True)
    solution = models.TextField(verbose_name="Réponse",null= True)
    manuel = models.FileField(upload_to='manuels_utilisations/%Y/%m/%d/',null= True,blank= True)

    def __str__(self):
        return self.probleme
from django.db import models
from membre.models import EntrepriseCommerciale



class ExpressionBesoin(models.Model):
    besoin = models.CharField(max_length=80,verbose_name = "Besoin",)
    image_illustratif = models.ImageField(upload_to = 'besoins/',verbose_name="image associé",null = True)

    class Meta:
        verbose_name = "Besoins Humains"

    def __str__(self):
        return self.besoin

class SpécificationBesoin(models.Model):
    besoin_fondamental = models.ForeignKey(ExpressionBesoin, on_delete = models.CASCADE, null = True)
    spécification = models.CharField(max_length=80,verbose_name = "Spécification",)
    image_illustratif = models.ImageField(upload_to = 'specifications_besoins/',
    verbose_name="image associé",null = True, blank = True,)

    class Meta:
        verbose_name = "Spécifiaction des Besoins"

    def __str__(self):
        return self.spécification

class Categorie(models.Model):
    """
        Catégories pouvant etre trouver dans les spécifications de besoins
    """
    specification = models.ForeignKey(SpécificationBesoin, on_delete = models.CASCADE, null = True)
    nom_categorie = models.CharField(max_length=100,verbose_name="Nom de la Catégorie",null=True)
    image_categorie = models.ImageField(upload_to='categorie/',
                                          verbose_name="Image de la Catégorie", null=True, blank=True, )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom_categorie

class Produit(models.Model):
    nom = models.CharField(max_length=100,verbose_name="Nom de l'article")
    vendeur = models.ForeignKey(EntrepriseCommerciale,on_delete=models.CASCADE,null = True)
    categorie_besoin = models.ForeignKey(SpécificationBesoin, on_delete=models.CASCADE, null=True,verbose_name="Spécification")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True,)
    code_article = models.CharField(max_length=100,verbose_name="Code de l'article",unique=True,blank=True)
    prix = models.PositiveIntegerField(verbose_name="Prix de l'article",null=True)
    marque = models.CharField(max_length = 50, null = True,blank=True)
    modele = models.CharField(max_length = 50, null = True,blank=True)
    description = models.TextField(null = True,blank=True)
    image_produit = models.ImageField(upload_to = 'produits/',verbose_name = "Image",null = True,)
    date_ajout = models.DateTimeField(auto_now_add = True,)

    def save(self, *args, **kwargs):
        # recuperation de l'entreprise associér a ce compte
        if self.id == None:
            super(Produit, self).save(*args, **kwargs)
            self.code_article = str(self.id)+""+str(self.vendeur.code_membre)
            self.save(update_fields=['code_article',])
        else:
            return super(Produit, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom

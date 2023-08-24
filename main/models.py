from django.db import models
from django.contrib.auth.models import User



class Coupon(models.Model):
    value = models.CharField(max_length=200)
    reduction = models.DecimalField(max_digits=5, decimal_places=2)

class Total(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #reduction = models.DecimalField(max_digits=10)

class Panier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    produits = models.ManyToManyField('Produit', through='ItemPanier')
   


class ItemPanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantite * self.produit.prix


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/images/produits')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    reduction = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    categorie = models.CharField(max_length=100)
    etat = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Adresse(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/images/')
    
from django.contrib import admin
from .models import Produit, Coupon, Adresse

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'categorie', 'etat', 'image', 'reduction')  # Champs à afficher dans la liste des produits

admin.site.register(Produit, ProduitAdmin)


class couponAdmin(admin.ModelAdmin):
    list_display = ('value', 'reduction')  # Champs à afficher dans la liste des produits

admin.site.register(Coupon, couponAdmin)

admin.site.register(Adresse)





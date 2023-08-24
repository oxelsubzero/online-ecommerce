from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Produit, Panier, ItemPanier, Coupon, Total, Adresse
import json #to jsonify some data
from django.http import JsonResponse 
import decimal


# Create your views here.



class Index(View):
    def get(self,request):
        produits_chaud = Produit.objects.all()[:5]  # Récupérer les 20 premiers produits
        produits_vente = Produit.objects.all()[5:8]
        produits_meilleurs = Produit.objects.all()[8:11]
        produits_recher = Produit.objects.all()[11:14]
        context = {
            'produits_chaud': produits_chaud,
            'produits_vente': produits_vente,
            'produits_meilleurs': produits_meilleurs,
            'produits_recher': produits_recher
            
        }
        if request.user.is_authenticated:
            panier, created = Panier.objects.get_or_create(user=request.user)
            items = ItemPanier.objects.filter(panier=panier)
            total = sum(item.total_cost for item in items)
            totalitem = sum(item.quantite for item in items)
            context = {
                "items":items,
                'produits_chaud': produits_chaud,
                'produits_vente': produits_vente,
                'produits_meilleurs': produits_meilleurs,
                "total": total,
                "totalitem": totalitem,
                'produits_recher': produits_recher
            }
            return render(request,"index.html",context)

        return render(request,"index.html",context)
    

class Shop(View):
    def get(self,request):
        produits = Produit.objects.all()
        context = {
            "produits" : produits,
           
        }
        if request.user.is_authenticated:
            panier, created = Panier.objects.get_or_create(user=request.user)
            items = ItemPanier.objects.filter(panier=panier)
            total = sum(item.total_cost for item in items)
            totalitem = sum(item.quantite for item in items)
            context = {
            "produits" : produits,
            "items":items,
            "total": total,
            "totalitem": totalitem,
            }
            return render(request,"shop-grid.html",context)
        return render(request,"shop-grid.html",context)
    def post(self, request):
            category_name = request.POST['categorie']
            if category_name=="all":
                products = Produit.objects.all()
            else :
                products = Produit.objects.filter(categorie=category_name)
            
            if request.user.is_authenticated:
                panier, created = Panier.objects.get_or_create(user=request.user)
                items = ItemPanier.objects.filter(panier=panier)
                total = sum(item.total_cost for item in items)
                totalitem = sum(item.quantite for item in items)
                context = {
                "produits" : products,
                "items":items,
                "total": total,
                "totalitem": totalitem,
                }
                return render(request,"shop-grid.html",context)
            context = {'produits': products}
            return render(request, "shop-grid.html", context)
    

class Contact(View):
    def get(self, request):
        return render(request,"contact.html")
    

class Detail(View):
    def post(self,request,produit_id):
        return render(request,"product-details.html")


class Cart(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, "authentication/login.html")
        panier, created = Panier.objects.get_or_create(user=request.user)
        items = ItemPanier.objects.filter(panier=panier)
        total = sum(item.total_cost for item in items)
        totalitem = sum(item.quantite for item in items)
        context = {
            "items":items,
            "total": total,
            "totalitem": totalitem,
        }
        return render(request,"cart.html",context)



class Add2cart(View):
    def post(self, request, produit_id):
        if not request.user.is_authenticated:
            return render(request, "authentication/login.html")
        produit = get_object_or_404(Produit, id=produit_id)
        panier, created = Panier.objects.get_or_create(user=request.user)
        item, item_created = ItemPanier.objects.get_or_create(panier=panier, produit=produit)
        if not item_created:
            item.quantite += 1
            item.save()
        return redirect('cart')  # Redirige vers la vue du panier

    
class Checkout(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, "authentication/login.html")
        total,created = Total.objects.get_or_create(user=request.user)

        total_user = total.total_amount
        context = {
            "total":total_user
        }
        return render(request,"checkout.html",context)
    
class Profil(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, "authentication/login.html")
        return render(request,"index.html")
    
"""class Validate_coupon(View):
    def post(self,request):
        data=json.loads(request.body)
        
        try :
            value = data['coupon']
            if not str(value).isalnum():
                return JsonResponse({'coupon_error':"le coupon ne peux pas contenir de caractères spéciaux"},status=400)
                
            elif not Coupon.objects.filter(value=str(value)).exists():
                return JsonResponse({"coupon_error":"Désolé, le coupon est invalide"},status=400)
                
            else:
                couponobj = get_object_or_404(Coupon,value=str(value))
                return JsonResponse({"reduc":couponobj.reduction},status=400)
        except :
            user = request.user  
            new_value = data['total']  # Supposons que le champ value soit passé dans la requête POST
            
            total = Total.objects.filter(user=user).first()
            
            
            if not total:
                total = Total(user=user)
            
            # Mettez à jour la valeur et enregistrez le modèle
            total.value = new_value
            total.save()
            
            return JsonResponse({'message': 'Total updated successfully.'})"""

class Validate_coupon(View):
    def post(self, request):
        data = json.loads(request.body)

        value = data['coupon']
        if not str(value).isalnum():
            return JsonResponse({'coupon_error': "le coupon ne peut pas contenir de caractères spéciaux"}, status=400)
                
        elif not Coupon.objects.filter(value=str(value)).exists():
            return JsonResponse({"coupon_error": "Désolé, le coupon est invalide"}, status=400)
                
        else:
            couponobj = get_object_or_404(Coupon, value=str(value))
            return JsonResponse({"reduc": couponobj.reduction})
        
            
class Update_total(View):
   def post(self, request):
        data = json.loads(request.body)
        user = request.user
        new_value = data.get('total')
        
        try:
            new_value_int = int(new_value)  # Convertir en nombre entier
            
            # Vérifier si l'utilisateur a déjà une instance de Total
            total, created = Total.objects.get_or_create(user=user)
            
            # Mettre à jour la valeur et enregistrer le modèle
            total.total_amount = new_value_int
            total.save()
            
            return JsonResponse({'message': 'Total updated successfully.'})
            
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': 'Invalid value provided.'}, status=400)


        
class SupprimerDuPanier(View):
    def get(self, request, item_id):
        item = ItemPanier.objects.get(id=item_id)
        item.delete()
        return redirect('cart')      


class Checkout2 (View):
    def get(self, request):
        if request.user.is_authenticated:
            addresse = Adresse.objects.all()[0]
            total,created = Total.objects.get_or_create(user=request.user)
            total_user = total.total_amount
            context = {
                "addresse":addresse,
                "total":total_user
            }
            return render(request,"checkout2.html",context)
        addresse = Adresse.objects.all()[0]
        context = {
                "addresse":addresse,
            }
        
        return render(request,"checkout2.html",context)
        
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User #User is a class that handle user 
import json #to jsonify some data
from django.http import JsonResponse 
from validate_email import validate_email #a python module to verify email format
from django.contrib import messages #send message on the page

from .utils import  account_activation_token
from django.core.mail import EmailMessage 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.contrib import auth

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email) #create a new user
                user.set_password(password)
                user.is_active = False #deactivate the account 
                user.save()

                """now we want to send en email verification to the 
                    user. the email will contain a link so for that we 
                    need the domain of the site, an uid encode in base64, 
                    and an token
                """
                current_site = get_current_site(request) 

                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activez votre compte'
                activate_url = 'http://'+email_body['domain']+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Suivez le lien suivant pour activer votre compte \n'+activate_url,
                    'oxelmiguel@outlook.fr',
                    [email],
                )
                email.send(fail_silently=False)

                messages.success(request, "Votre compte a été créer avec succes; verifiez vos emails pour le lien d'activation")
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')





class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':"le nom d'utilisateur ne peux pas contenir de caractères spéciaux"},status=400)
        if User.objects.filter(username=str(username)).exists():
            return JsonResponse({"username_error":"Désolé, le nom d'utilisateur est deja utilisé"},status=400)
        
        return JsonResponse({'username_valid':True})
    
class emailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':"l'email est invalide"},status=400)
        if User.objects.filter(email=str(email)).exists():
            return JsonResponse({"email_error":"Désolé, l'email est deja utilisé"},status=400)
        
        return JsonResponse({'email_valid':True})
    


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'Utilisateur deja activé')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Compte activé avec succes')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    """messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')"""
                    return redirect('shop')
                messages.error(
                    request, "Le compte n'est pas activé,Veuillez verifier vos cmail")
                return render(request, 'authentication/login.html')
            messages.error(request, 'Informations de connexion invalides')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Veuillez remplir tout les champs')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'Vous avez été deconnecté')
        return redirect('login')
from django.urls import path
from .views import RegistrationView, UsernameValidationView, emailValidationView, VerificationView, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register',RegistrationView.as_view(),name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name="username_validation"),
    path('validate-email',csrf_exempt(emailValidationView.as_view()),name="email_validation"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')
   
]



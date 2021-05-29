from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='customer/login.html'), name='login_view'),
    path('registration/', RegistrationCustomer.as_view(), name='registration_customer'),
    path('logout/', logout_view, name='logout_view')
]

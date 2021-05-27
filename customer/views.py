from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings

# Create your views here.
from .forms import RegistrationCustomerForm
from cart.cart import Cart
from cart.models import CartAuthCustomer
import json


class RegistrationCustomer(CreateView):
    template_name = 'customer/registration.html'
    model = User
    form_class = RegistrationCustomerForm
    success_url = reverse_lazy('main_page')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            session_cart = Cart(self.request)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            self.create_auth_cart(session_cart)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def create_auth_cart(self, session_cart):
        customer_cart = session_cart.cart
        CartAuthCustomer.objects.create(customer=self.request.user, cart_customer=json.dumps(customer_cart))

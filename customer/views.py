from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.
from .forms import RegistrationCustomerForm


class RegistrationCustomer(CreateView):
    template_name = 'customer/registration.html'
    model = User
    form_class = RegistrationCustomerForm
    success_url = reverse_lazy('main_page')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})
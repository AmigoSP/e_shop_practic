from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationCustomerForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Password_Confirm')

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            check = User.objects.filter(username=username).exists()
            if check:
                raise ValidationError(f'Name: {username} already exists')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Password and password_confirm not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# reemplazar el UserCreationForm que viene predeterminado
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo electronico',
        max_length=50,
        help_text="Coloca tu email",
        error_messages={'invalid':"Ingresa tu correo nuevamente"})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = User.objects.filter(email = email)
        if u.count():
            raise ValidationError("Email está utilizado")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

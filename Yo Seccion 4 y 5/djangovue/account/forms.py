from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import UserProfile

# importamos el gettext internamente de django, el as sirve para darle otro nombre
from django.utils.translation import gettext as _

# en forms.py utilizaremos el ejemplo de la traduccion

# reemplazar el UserCreationForm que viene predeterminado
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo electronico',
        max_length=50,
        help_text=_('Put your favorite email'),
        error_messages={'invalid':"Ingresa tu correo nuevamente"})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = User.objects.filter(email = email)
        if u.count():
            raise ValidationError(_("Email taking"))
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        # enviamos los campos desde el modelo: user y avatar
        model = UserProfile
        fields = ('avatar','user')

    # para modificar los campos, en este caso ocultar el usuario y añadir una clase a la seleccion de imagen
    def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
            self.fields['user'].widget = forms.HiddenInput()
            self.fields['user'].required = False
            self.fields['avatar'].widget.attrs['class'] = "custom-file-input"
            self.fields['avatar'].widget.attrs['id'] = "customFile"

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        w, h = get_image_dimensions(avatar)

        # validacion por tamaño de la img
        max_width = max_height = 1980
        if w > max_width or h > max_height:
            raise forms.ValidationError("Imagen muy grande, no puede superar las %spx, %spx" % (max_width, max_height))

        # extension archivo
        m,t = avatar.content_type.split('/')
        if not (m == 'image' and t in ['jpeg', 'jpg', 'gif', 'png']):
            raise forms.ValidationError("Tipo de archivo no soportado, intente con: jpeg, png, jpg, gif")

        # validar tamaño imagene
        if len(avatar) > (150 * 1024):
            raise forms.ValidationError("La imagen no puede superar los 150 KB")

        return avatar


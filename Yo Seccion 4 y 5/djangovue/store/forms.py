# creamos el forms.py para el sistema de comentarios
# importar forms
from django import forms
# cargar modelo
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'lastname', 'email', 'body')

    # para modificar los campos en el html
    # para este caso queremos ocultar los datos del formulario para los usuarios loggeados
    def __init__(self, user, *args, **kwargs):
            super(MessageForm, self).__init__(*args, **kwargs)
            if user.is_authenticated:
                self.fields['name'].widget = forms.HiddenInput()
                self.fields['name'].required = False
                self.fields['lastname'].widget = forms.HiddenInput()
                self.fields['lastname'].required = False
                self.fields['email'].widget = forms.HiddenInput()
                self.fields['email'].required = False
            
            #self.fields['avatar'].widget.attrs['class'] = "custom-file-input"
            #self.fields['avatar'].widget.attrs['id'] = "customFile"


# Formulario generico para los campos coupon, no está asociado a un modelo
class CouponForm(forms.Form):
    code = forms.CharField()
    element_id = forms.CharField(widget=forms.HiddenInput())


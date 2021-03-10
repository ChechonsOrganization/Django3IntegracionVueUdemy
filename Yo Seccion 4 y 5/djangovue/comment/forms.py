from django.forms import ModelForm, Textarea, TextInput

from .models import Comment, TypeContact

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] # o si es tupla ('text',)
        widgets = {
            'text' : Textarea(attrs={'class':'form-input'})
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['text'].widget.attrs.update({'class':'form-input'})

    # obtener una referencia del elemento con el cual estamos trabajando
    # le pasamos el modelo (clase) y el self
    # y asi podemos obtener una instancia del elemento que queremos guardar (del form)
    # def save(self, commit=True, text=""):
    def save(self, commit=True, text=""):
        instance = super(CommentForm, self).save(commit=commit)

        # Si queremos condicionar antes de actualizar
        # if(instance.text == ""):
        #     instance.text = "No podrás modificarme"

        if(text != ""):
            instance.text = text

        if(commit):
            instance.save()
        
        return instance

from django import forms
from django.core.validators import MinLengthValidator, EmailValidator

class ContactForm(forms.Form):

    #Tupla para los Choice
    CHOICE_SEX = (
        ('M', "Masculino"),
        ('F', "Femenino"),
        ('N', "Prefiero no especificar")
    )

    # initial es opcional, que sea requerired=True o False
    # name = forms.CharField(label="Nombre", initial='Pepe', required=False, disabled=True)
    #name = forms.CharField(label="Nombre", initial='Pepe', required=True, disabled=False, help_text="Aquí va tu nombre",max_length=10, min_length=2)
    #name = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}),label="Nombre", max_length=10, validators=[MinLengthValidator(3, message='El nombre debe contener más %(limit_value)d carácteres')])
    name = forms.CharField(label="Nombre", max_length=10)
    #email = forms.CharField(label="Correo", validators=[EmailValidator(message="Correo inválido", whitelist=['gmail'])])
    surname = forms.CharField(label="Apellido", required=False, max_length=10, min_length=3)
    email = forms.EmailField(label="Correo")
    # para diferenciar los numeros (569) 9091 1154 
    phone = forms.RegexField(label="Telefono", regex='\(\w{3}\)\w{4}\w{4}', max_length=13, min_length=13)
    date_birth = forms.DateField(label="Fecha de nacimiento")
    sex = forms.ChoiceField(label="Sexo",choices=CHOICE_SEX)
    #type_contact = forms.ChoiceField(label="Tipo de contacto",choices=CHOICE, initial=3)
    type_contact = forms.ModelChoiceField(label="Tipo de contacto", queryset=TypeContact.objects.all(), initial=1)
    # subida de archivos
    documento =forms.FileField(label="Documento", required=False)
    #document =forms.ImageField(label="Documento")
    terms = forms.BooleanField(label="Condiciones de servicio")
    
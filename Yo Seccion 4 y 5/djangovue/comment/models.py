from django.db import models
# importamos listelement
from listelement.models import Element

# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    # copiado desde models listelement, este ahora tendrá elementos opcionales, debemos capturarlos con related_name
    element = models.ForeignKey(Element, related_name='comments', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Comentario #{}'.format(self.id)

class TypeContact(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Contact(models.Model):

    CHOICE_SEX = (
        ('M', "Masculino"),
        ('F', "Femenino"),
        ('N', "Prefiero no especificar")
    )

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=13)
    date_birth = models.DateField()
    documento = models.FileField(upload_to='uploads/contact',default='', null=True)
    sex = models.CharField(max_length=1, choices=CHOICE_SEX, default='M')
    type_contact = models.ForeignKey(TypeContact, on_delete=models.CASCADE, default=1)


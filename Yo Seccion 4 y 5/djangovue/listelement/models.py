# importar decimal para la operacion del descuento
from decimal import Decimal
from django.db import models
# importar taggit para el uso de tags valga la redundancia
from taggit.managers import TaggableManager
# importar django stdimage
from stdimage import StdImageField, JPEGField
# importar signals para eliminar las imagenes
from django.dispatch import receiver
# importar los settings
from django.conf import settings
# importar reverse para el sitemap
from django.urls import reverse
# importar slugify para convertir el texto de las url limpias en slug de manera automatica
from django.utils.text import slugify
# importar os para eliminar imagenes
import os

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    #DEFINIR MODELO __str__
    def __str__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    #DEFINIR MODELO __str__
    def __str__(self):
        return self.title

class Element(models.Model):
    # agregamos el tag para que el modelo sea etiquetable
    tags = TaggableManager()
    title = models.CharField(max_length=255)
    # se actualiza el url_clean: url_clean = models.CharField(max_length=255), no es necesario la migracion para actualizar
    url_clean = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2, default=6.10) # 12345678.90
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type, on_delete= models.CASCADE)

    # funcion save para setear el url_clean de manera automatica
    def save(self, *args, **kwargs):
        self.url_clean = slugify(self.title)
        super(Element, self).save(*args, **kwargs)

    # obtener get absolute url para el sitemap
    def get_absolute_url(self):
        return reverse("store:detail", args=[self.url_clean])

    class Meta:
        # Remove parent's ordering effect
        ordering = ['id']

    # obtener calculos de descuentos 
    def get_discount(self, coupon):
        return (coupon.discount / Decimal(100)) * self.price 

    # obtener el precio final del producto despues del descuento
    def get_price_after_discount(self, coupon):
        return self.price - self.get_discount(coupon)

    #DEFINIR MODELO __str__
    def __str__(self):
        return self.title

# modelo creado para subir las imagenes del producto (element)
class ElementImages(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    # cover sin stdimage
    # cover = models.ImageField(upload_to='images/')

    # cover con stdimage
    # cover = StdImageField(upload_to='images/',variations={'thumbnail': {'width': 300, 'height': 300, "crop": True}})

    # cover con JPEGField
    cover = JPEGField(upload_to='images/',variations={'custom': {'width': 360, 'height': 487, "crop": True}})

    # para obtener el nombre de la imagen original
    base_cover_name = models.CharField(max_length=100, default='')
    # para obtener la extension
    base_cover_ext = models.CharField(max_length=5, default='')

    def __str__(self):
        return self.title

    # guardar campos de manera personalizada
    def save(self, *args, **kwargs):
        """
            Obtener la referencia del nombre original de la imagen como de su extensión
        """
        (root, ext) = os.path.splitext(self.cover.path)
        """
            Quitar path absoluto del archivo, para solo dejar la carpeta donde este
            se guardará (images), el nombre de la imagen y su extension.

            Importamos y llamamos a settings para quitar path absoluto 
            que yace en la variable root y solo dejar la carpeta donde se subirá(images).
            Esto es para almacenar el nombre y carpeta de nuestras imagenes en la base de datos
            elementimages -> base_cover_name que es lo mismo que -> cover, solo que esté sera llamado y el cover no

            Condiciones:
                1. Si el base_cover_name está vacío porque no hay imagen subida,
                   la variable root elimina el path absoluto y agrega la carpeta donde esta se sube (images)
                2. Si el base_cover_name no está vacío, quiere decir que se está actualizando
                   ya sea la imagen o solo su titulo, en este caso hay dos posibilidades, asi que
                   necesitaremos primero comprobar si la variable root contiene la carpeta de subida (images), luego:
                   2.1. Si hayamos que la variable "palabra" se encuentra en la variable "root" quiere decir que
                        estamos actualizando solo el titulo de la imagen, por lo cual tendremos que quitar
                        todo el path absoluto y agregar "images/" nuevamente, de otro modo se nos duplicará en la BBDD,
                        asi que reemplazamos la palabra "images\" y luego eliminamos el path absoluto para que no se duplique
                   2.2 Sino encuentran la palabra en el root significa que estamos actualizando por otra imagen, entonces solo
                        procedemos a eliminar el path absoluto y agregar el nombre de la carpeta de subida "images/" y asignarla
                        nuevamente a base_cover_name
        """    
        if (self.base_cover_name == ""):
            root = root.replace(settings.MEDIA_ROOT+"\\","images/")
            self.base_cover_name = root
        elif (self.base_cover_name != ""):
            # probar si root contene la palabra images\ para actualizar solo el titulo
            palabra = "images\\"
            if palabra in root.lower():
                root = root.replace('images\\','')
                root = root.replace(settings.MEDIA_ROOT+"\\","images/")
                self.base_cover_name = root
            else:
                root = root.replace(settings.MEDIA_ROOT+"\\","images/")
                self.base_cover_name = root

        # guardar extensión de la imagen
        self.base_cover_ext = ext

        # llamamos a la super clase para salvar datos
        super(ElementImages, self).save(*args, **kwargs)


# Funcion para eliminar Imagenes Y sus CUSTOM al eliminar una imagen del registro en BBDD
# @receiver para estar atento cuando se borre para ser accionado
@receiver(models.signals.post_delete, sender=ElementImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # preguntar si la instancia (imagen original) existe
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)

    # obtener el nombre original de la imagen como de su extensión (custom)
    (root, ext) = os.path.splitext(instance.cover.path)

    # sumamos el nombre de la imagen original mas su extensión
    extra_file = root+".custom.jpeg"

    # preguntar si la imagen custom existe para eliminarla
    if os.path.isfile(extra_file):
        os.remove(extra_file)


# Funcion para eliminar Imagenes al ser actualizarlas del registro en BBDD
# @receiver para estar atento cuando se borre para ser accionado
@receiver(models.signals.pre_save, sender=ElementImages)
def auto_delete_file_on_update(sender, instance, **kwargs):

    # preguntar si tenemos pk
    if not instance.pk:
        return False

    # para buscar al elemento por su pk y por cover
    try:
        old_file = ElementImages.objects.get(pk=instance.pk).cover
    except ElementImages.DoesNotExist:
        return False

    # comparamos si tenemos una imagen antigua para eliminarla del registro
    new_file = instance.cover
    if not old_file == new_file:
        # preguntar si la instancia antigua existe
        if instance.cover:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

        # obtener el nombre original de la imagen como de su extensión (imagen custom)
        (root, ext) = os.path.splitext(old_file.path)

        # sumamos el nombre de la imagen original mas su extensión
        extra_old_file = root+".custom.jpeg"

        # preguntar si la imagen custom existe para eliminarla
        if os.path.isfile(extra_old_file):
            os.remove(extra_old_file)

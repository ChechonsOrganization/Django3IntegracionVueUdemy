from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# http para el csv
from django.http import HttpResponse
# importamos el gettext internamente de django, el as sirve para darle otro nombre
from django.utils.translation import gettext as _

# para los mails y enviar html por mensaje
from django.core.mail import send_mail
from django.template import loader

# importar paginación
from django.core.paginator import Paginator

from .models import Comment, Contact
from .forms import CommentForm, ContactForm

# CSV
import csv

# importamos el logging
import logging
# obtener una instancia del logger
logger = logging.getLogger(__name__)

# Create your views here.

def export(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="datostest.csv"'

    # obtener los datos de los comentarios para exportarlos en el csv
    comments = Comment.objects.all()
    # crear writer
    writer = csv.writer(response)
    # construir cabecera
    writer.writerow(["Id","Comentario"])
    # recorrer los comentarios
    for c in comments:
        writer.writerow([c.id,c.text])

    #writer = csv.writer(response)
    #writer.writerow(['Primera fila','Django','Flask','Python'])
    #writer.writerow(['Segunda fila','A','B','C','Mas Datos','Otro'])

    return response


def testview(request):
    return render(request,'test/testview.html')

import os
from djangovue import settings

def index(request):
    # comentar, es solo ejemplo
    print(_("Welcome to my application"))
    
    #logger.debug("ESTO ES UN DEBUG")
    #logger.info("ESTO ES UN INFO")
    #logger.error("ESTO ES UN ERROR")

    # ejecutamos el ejemplo de session
    if 'comment_id' in request.session:
        print("Ultimo comentario "+str(request.session['comment_id']))
        # destruir el dato
        del request.session['comment_id']

    comments = Comment.objects.all().order_by('id')

    # paginación
    paginator = Paginator(comments,5)
    # obtener pagina actual, de paginación
    page_number = request.GET.get('page')
    # objeto paginación
    comments_page = paginator.get_page(page_number)

    #return render(request,'index.html',{'comments':comments})
    return render(request,'index_page.html',{'comments_page':comments_page})


def add(request):

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            
            html_message = loader.render_to_string('email/comment.html',{'comment':comment})
            
            #ejemplo session
            request.session['comment_id'] = comment.id

            send_mail(
                "Comentario #"+str(comment.id), #"Titulo",
                comment.text,#"Contenido del mail",
                "sergio.04.ramirez@gmail.com",
                ["sergio.04.ramirez@gmail.com"],
                fail_silently=False,
                html_message=html_message
                #html_message="<h1>Hola Mundo</h1>"
            )

            return redirect('comment:index')
    else:
        form = CommentForm()

    return render(request, 'add.html',{'form':form})


def update(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        print(form.errors.as_json())
        print(form.errors.as_text())

        #form.save(commit=True,text="hola mundo" )
        if form.is_valid():
            form.save(commit=True)
            return redirect('comment:update',pk=comment.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'update.html',{'form':form, 'comment': comment})

# en caso de necesitar desactivar el csrf, utilizar este codigo
#from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

#@csrf_exempt
def contact(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():

            contact = Contact()
            contact.name = form.cleaned_data['name']
            contact.surname = form.cleaned_data['surname']
            contact.phone = form.cleaned_data['phone']
            contact.email = form.cleaned_data['email']
            contact.date_birth = form.cleaned_data['date_birth']
            contact.sex = form.cleaned_data['sex']
            contact.type_contact = form.cleaned_data['type_contact']
            if 'documento' in request.FILES:
                contact.documento = request.FILES['documento']
            contact.save()
            #print('Valido: ' + str(form.cleaned_data['type_contact'].id))
            #print('Valido: ' + form.cleaned_data['sex'])
            messages.add_message(request, messages.INFO, 'Contacto recibido')
            return redirect('comment:contact')
        else:
            print('Invalido')
    else: 
        form = ContactForm()

    # if (form.errors):
    #     raise ValidationError(form.errors)

    return render(request, 'contact.html',{'form':form})

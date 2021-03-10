from django.contrib import admin

# Register your models here.

# importar modelo Question y Choice para generar un crud desde el admin
from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    #para escoger lo que uno quiere que vaya en el listado, por defecto no trae el id en la lista
    list_display = ('id', 'question_text', 'pub_date')
    #agregar panel de filtros, en este caso, la fecha de publicacion de las preguntas
    list_filter = ['pub_date','question_text']
    #para agregar un cuadro de busqueda para nuestras tablas
    search_fields = ['question_text']
    fieldsets = [
        ('Datos básicos', {'fields' : ['question_text']}),
        ('Información fecha', {'fields' : ['pub_date']})
    ]
    inlines = [ChoiceInline]
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
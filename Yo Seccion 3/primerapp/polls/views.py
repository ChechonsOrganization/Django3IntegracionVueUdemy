from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.views import generic

from .models import Question, Choice



class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5] 
    

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


# Create your views here.

""" ABRE def index(request):
    #return HttpResponse("Hola Mundo Django")
    # output = ', '.join([q.question_text for q in questions])
    # return HttpResponse(output)
    questions = Question.objects.order_by('-pub_date')[:5] #indicando los ultimos 5

    #template = loader.get_template('index.html')
    context = {
        'questions' : questions
    }

    #return HttpResponse(template.render(context, request))
    return render(request,'index.html',context)

def detail(request, question_id):

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Pregunta no existe')

    question = get_object_or_404(Question, pk=question_id)

    # return HttpResponse("Detail %s" % question_id)
    #le pasamos el context (que es un diccionario, o directamente)
    return render(request,'detail.html',{'question':question,})

def results(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    #response = "results %s"
    #return HttpResponse(response % question_id)
    return render(request,'results.html',{'question':question,}) CIERRE COMENTARIO"""
    

def vote(request, question_id):

    print(str(request.POST['choice']))

    question = get_object_or_404(Question, pk=question_id)

    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse("Error en el choice")
    else:
        select_choice.votes +=1
        select_choice.save()
        #return HttpResponse("vote %s" % question_id)
        return HttpResponseRedirect(reverse('polls:results', args=[question.id]))

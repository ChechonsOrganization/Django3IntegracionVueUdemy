from . import views
from django.urls import path


app_name='polls'
urlpatterns = [
    #/polls/
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    #path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:question_id>/results', views.results, name='results'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    # vote permanece igual
    path('<int:question_id>/vote', views.vote, name='vote') 
]
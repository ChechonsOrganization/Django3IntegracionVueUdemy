from django.urls import path
# para importar las vistas desde el modulo actual
from . import views

app_name='account'

urlpatterns = [
    path('user_data/', views.user_data),
    path('profile/', views.profile, name='profile'),
    path('register/',views.register, name='register')
]

import os
from django.conf import settings

from django.shortcuts import render, redirect, reverse
# importamos el decorador para la autenticación de usuario @login_required como en ASP.NET
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
# reemplazado por:
from django.contrib.auth import login as make_login
from django.core.exceptions import ObjectDoesNotExist

from .forms import CustomUserCreationForm, UserProfileForm
from .forms import UserProfile
# Create your views here.


def user_data(request):
    # asi podemos obtener los datos del usuario desde el controlador
    #print(request.user.username)
    #print(request.user.is_authenticated)
    return render(request, 'user_data.html')

@login_required
def profile(request):
    #print(request.user.id)
    form = UserProfileForm()
    if request.method == 'POST':
        pathOldAvatar = None
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

            print(settings.MEDIA_ROOT)
            print(userprofile.avatar.name)
            
            pathOldAvatar = os.path.join(settings.MEDIA_ROOT,userprofile.avatar.name)
            print(os.path.join(settings.MEDIA_ROOT,userprofile.avatar.name))
        except ObjectDoesNotExist:
            form = UserProfileForm(data=request.POST, files=request.FILES)

        if form.is_valid():

            #verificar si tiene el avatar anterior
            if pathOldAvatar is not None and os.path.isfile(pathOldAvatar):
                os.remove(pathOldAvatar)

            userprofile = form.save(commit=False)
            userprofile.user = request.user
            userprofile.save()


    return render(request, 'profile.html', {'form':form})

def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                make_login(request, user)
                return redirect(reverse('account:profile'))
                
            #return redirect(reverse('login'))

    return render(request, 'register.html',{'form':form})
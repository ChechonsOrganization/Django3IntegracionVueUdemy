"""djangovue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# importar settings y static para que funcione el añadir static
from django.conf import settings
from django.conf.urls.static import static
#añadir include
from django.urls import path, include
from django.contrib.auth import views as auth_views
# añadir vistas de restmanual 
from restmanual import views as restmanual


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    #incluir listelement
    path('api/', include('listelement.urls')),
    #incluir comment
    path('comment/', include('comment.urls')),
    # incluir account
    path('accounts/', include('account.urls')),
    # incluir/activar usuarios
    path('accounts/', include('django.contrib.auth.urls')),
    # path de aplicacion store, arrancará desde la raiz del proyecto
    path('', include('store.urls')),
    # cambiar url de cambiar contraseña
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html')
    ),
    # colocar la URI de restmanual sin necesidad de integrar las url, pero en este caso se puede emplear de esta manera
    path('restmanual/demo',restmanual.manualJson),
    # incluir el path de product list de restmanual urls
    path('restmanual/', include('restmanual.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
]

# ignorar aviso del VS
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

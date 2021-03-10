from django.urls import path
from . import views

# importar sitemap
from django.contrib.sitemaps.views import sitemap
# importart sitemap.py
from .sitemap import ElementSitemap


# crear site
sitemaps = {
    'sitemap': ElementSitemap
}


app_name='store'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/pay/paypal/<int:pk>', views.make_pay_paypal, name='make_pay_paypal'),
    # este path es para recibir el cupon en el pago de paypal
    path('product/pay/paypal/<int:pk>/<str:code>', views.make_pay_paypal, name='make_pay_paypal'),
    path('product/paypal/success/<int:pk>', views.paypal_success, name='paypal_success'),
    # definir paypal success para el url con descuento
    path('product/paypal/success/<int:pk>/<str:code>', views.paypal_success, name='paypal_success'),
    path('product/paypal/cancel', views.paypal_cancel, name='paypal_cancel'),
    path('bought/', views.bought, name='bought'),
    path('product/payed/detail/<int:pk>', views.detail_pay, name='detail_pay'),
    path('product/<int:pk>',views.DetailView.as_view(), name='detail'),
    #path('product/<slug:url_clean>',views.DetailView.as_view(), name='detail'),
    # al encontrar coincidencias django va a dejar de seguir buscando, entonces hay que dejar coupon_apply antes de detail
    path('product/coupon_apply',views.coupon_apply, name='coupon_apply'),
    path('product/<slug:url_clean>',views.detail, name='detail'),
    # url para aplicar el cupon en detalle
    path('product/<slug:url_clean>/<str:code>',views.detail, name='detail'),
    #path('product/<int:pk>/<slug:url_clean>',views.DetailView.as_view(), name='detail'),
    path('sitemap.xml', sitemap,{'sitemaps':sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

from django.shortcuts import render, redirect,reverse, get_object_or_404
# importamos el modelo Element, Category de la app listelement
from listelement.models import Element, Category
# importar paginator
from django.core.paginator import Paginator
# importar vistas genericas
from django.views import generic
# importar decorator para asegurar que el usuario esté loggeado para las compras
from django.contrib.auth.decorators import login_required
# importar decorador para que los cupones sean verificados solo por post
from django.views.decorators.http import require_POST
# importar settings general para llamar las configuraciones de paypal
from django.conf import settings
# importar timezone para la validacion de fechas
from django.utils import timezone
# importar 404
from django.http import HttpResponseNotFound
# cargar el modelo tag
from taggit.models import Tag
# importar paypal
import paypalrestsdk
import logging
# importar modelo Payment y Coupon de Store
from .models import Payment, Coupon
# cargar forms.py 
from .forms import MessageForm, CouponForm

# Create your views here.

def index(request):

    elements = Element.objects.all()

    # habilitar busqueda de elementos en index.html
    search = request.GET.get('search') if request.GET.get('search') else ''
    category_id = request.GET.get('category_id')
    # verificar si category_id está definido
    category_id = int(category_id) if category_id else ''
    # tag para la busqueda
    tag_id = request.GET.get('tag_id')
    # verificar si tag_id está definido
    tag_id = int(tag_id) if tag_id else ''


    if search:
        # indicar relacion con prefetch_related para que no haga mas consultas de las necesarias, y el uso del _set
        elements = Element.objects.prefetch_related('elementimages_set').filter(title__contains=search)
        # en caso de querer buscar sin case-sensitive elements = Element.objects.filter(title__icontains=search)
    else:
        elements = Element.objects.prefetch_related('elementimages_set')

    if category_id:
        elements = elements.filter(category_id=category_id)

    # tags
    if tag_id:
        tag = get_object_or_404(Tag,id=tag_id)
        # relacion de muchos a muchos para consultar la misma necesitamos __in
        elements = elements.filter(tags__in=[tag])

    # si buscamos obtener todos los elementos usamos:
    # elements = elements.all()

    # listar elementos los cuales su tipo sean productos y no post
    elements = elements.filter(type = 2)

    paginator = Paginator(elements, 6)

    categories = Category.objects.all()

    # obtener el listado de los tags
    tags = Tag.objects.all()

    page_number = request.GET.get('page')

    elements_page = paginator.get_page(page_number)

    # enviar datos a la vista para la busqueda
    return render(request, 'store/index.html', {'elements' : elements_page, 'categories':categories, 'search':search, 'category_id':category_id, 'tags':tags, 'tag_id':tag_id})

# crear def detalle para los comentarios en detail, el codigo es opcional, code = None
def detail(request, url_clean, code=None):

    #coupon = None
    #if code:
    #    coupon = get_valid_coupon(code)
    coupon = get_valid_coupon(code) if code else None

    # comprobar si el code es nulo
    msj_coupon = ''
    if (code == 'None' or coupon is None) and code is not None:
        msj_coupon = 'El cupón es inválido'
        code = ''
        

    element = get_object_or_404(Element, url_clean=url_clean)
    # establecer nueva variable que sea igual que element
    messages = element.element_comments.filter(activate=True)
    # crear variable message_form
    message_form = MessageForm(user=request.user)
    # crear instancia de coupon
    coupon_form = CouponForm(initial={'element_id':element.id, 'code':code})
    # message new, podemos aprovechar la variable desde la vista para 
    # mostrar un mensaje de exito en caso de que esté definido
    message_new = None
    
    # si estamos recibiendo el formulario
    if request.method == 'POST':
        # definir formulario inicial messageForm
        # al message_form le pasamos el user que trae en forms.py de __init__
        message_form = MessageForm(user=request.user, data=request.POST)
        if message_form.is_valid():
            message_new = message_form.save(commit=False)
            message_new.element = element
            if request.user.is_authenticated:
                message_new.name = request.user.first_name
                message_new.lastname = request.user.last_name
                message_new.email = request.user.email
                message_new.user = request.user
            message_new.save()
            # para limpiar los datos al enviar
            message_form = MessageForm(user=request.user)

    return render(request, 'store/detail.html',{'element':element, 
                                                'message_form':message_form,
                                                'message_new':message_new,
                                                'messages':messages,
                                                'coupon_form':coupon_form,
                                                'coupon':coupon,
                                                'msj_coupon':msj_coupon
                                                })

# funcion para validar los cupones de pago
@require_POST
def coupon_apply(request):

    form = CouponForm(request.POST)
    coupon = None

    if form.is_valid():
        code = form.cleaned_data['code']
        elementId = form.cleaned_data['element_id']
    
    try:
        couponModel = get_valid_coupon(code) # le pasamos la funcion get_valid_coupon
        if couponModel:
            coupon = couponModel
        
    except Coupon.DoesNotExist:
        pass

    try:
        element = Element.objects.get(id=elementId)
    except Element.DoesNotExist:
        coupon=None

    return redirect('store:detail',url_clean=element.url_clean, code=coupon)

class DetailView(generic.DeleteView):
    model = Element
    template_name = 'store/detail.html'
    slug_field = 'url_clean'
    slug_url_kwarg = 'url_clean'


#Compra Paypal, incluido el codigo de descuento como opcional, code = None
@login_required
def make_pay_paypal(request, pk, code=None):

    # condicion para el descuento de paypal
    coupon = get_valid_coupon(code) if code else None

    # para cupon invalido
    if coupon is None and code is not None:
        return HttpResponseNotFound()
        
    element = get_object_or_404(Element, pk = pk)

    # si tenemos un cupon, usaremos unas variables para ingresar en los parametros del payment
    if coupon:
        return_url = "http://127.0.0.1:8000/product/paypal/success/%s/%s"%(element.id,coupon.code)
        price = round(element.get_price_after_discount(coupon),2)
    else:
        return_url = "http://127.0.0.1:8000/product/paypal/success/%s"%element.id
        price = element.price

    paypalrestsdk.configure({
    "mode": settings.PAYPAL_CLIENT_MODO,
    "client_id": settings.PAYPAL_CLIENT_ID ,
    "client_secret": settings.PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": "http://127.0.0.1:8000/product/paypal/cancel"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": str(price),
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": str(price),
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    # autorizar pago
    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))

    return render(request,'store/paypal/buy.html',{'element': element, 'approval_url': approval_url,'coupon':coupon})

# si la operacion de paypal es exitosa, se le añade code=None
@login_required
def paypal_success(request, pk, code=None):

    # crear variable cupon
    coupon = get_valid_coupon(code) if code else None

    # necesita el client_id y el client_secret
    paypalrestsdk.configure({
    "mode": settings.PAYPAL_CLIENT_MODO,
    "client_id": settings.PAYPAL_CLIENT_ID ,
    "client_secret": settings.PAYPAL_CLIENT_SECRET })

    # ejecución pago

    #recibir pk del elemento que queremos comprar
    element = get_object_or_404(Element, pk = pk)

    # recibir payment y payer
    paymentId = request.GET.get('paymentId')
    payerId = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(paymentId)

    # definir una excepcion
    try:
        if payment.execute({"payer_id": payerId}):

            # creamos pago
            paymentModel = Payment(
                payment_id=paymentId,
                payer_id=payerId,
                price=element.price,
                element_id=element.id,
                user_id=request.user.id
            )

            if coupon:
                paymentModel.coupon = coupon
                paymentModel.discount = element.get_price_after_discount(coupon)
                paymentModel.price_discount = element.get_discount(coupon)
                coupon.active = 0
                coupon.save()

            # guardar pago
            paymentModel.save()

            print("Payment execute successfully")

            # redireccionar al usuario
            return redirect(reverse('store:detail_pay',args=[paymentModel.id]))

        else:
            print(payment.error) # Error Hash

    except paypalrestsdk.exceptions.ResourceNotFound as identifier:
        print("Ha ocurrido un error de paypal %s"%type(identifier).__name__)

    return render(request,'store/paypal/success.html')

# redirección de la compra exitosa para mostrar lo que se ha comprado
@login_required
def detail_pay(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'store/payment/detail.html',{'payment':payment})

# controlador para ver las compras realizadas por el usuario
@login_required
def bought(request):
    # si quisieramos retornar todas las compras
    # return render(request, 'store/payment/bought.html',{'payments':Payment.objects.select_related('element').all()})

    # para retornar las compras del usuario logueado
    return render(request, 'store/payment/bought.html',{'payments':Payment.objects.select_related('element').filter(user = request.user)})

# si la operacion de paypal es cancelada
@login_required
def paypal_cancel(request):
    return render(request,'store/paypal/cancel.html')


# otras funciones
# funcion 
def get_valid_coupon(code):
    now = timezone.now()
    coupon = None
    try:
        couponModel = Coupon.objects.get(
            code__iexact=code,
            valid_from__lte=now, #less than or equal to
            valid_to__gte=now, # great than or equal to
            active=True
        )
        coupon = couponModel
    except Coupon.DoesNotExist:
        pass

    return coupon

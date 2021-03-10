# este archivo se usará para los filtros personalizados en django, importante crear en templatetags el __init__.py
from django import template

register = template.Library()

# funcion para descontar
# añadimos decorador @register.filter(name='discount')
@register.filter('discount')
def discount(element, coupon):
    return element.get_discount(coupon)

# funcion para restar el descuento al precio
# añadimos decorador @register.filter(name='discount')
@register.filter('discount_final')
def discount_final(element, coupon):
    return element.get_price_after_discount(coupon)

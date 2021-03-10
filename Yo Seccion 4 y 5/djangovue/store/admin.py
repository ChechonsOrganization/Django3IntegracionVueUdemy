from django.contrib import admin
# importamos modelo Message, Coupon
from .models import Message, Coupon


# Register your models here.

#colocamos decorador para registrar en el admin

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name','email','element','created','activate')
    list_filter = ('activate', 'created','updated')
    search_fields = ('name','email','body')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)


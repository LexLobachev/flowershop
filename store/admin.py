from django.contrib import admin

from store.models import Posy, Florist, Courier, Client


@admin.register(Posy)
class PosyAdmin(admin.ModelAdmin):
    list_display = ('title', 'cause', 'price', 'description', 'picture', 'composition')
    list_filter = ('title', 'cause', 'price')


@admin.register(Florist)
class FloristAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client_key')


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client_key')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'full_name', 'phone_number', 'address', 'florist_key', 'courier_key', 'delivery_datetime')
    list_filter = ('client_id', 'phone_number')

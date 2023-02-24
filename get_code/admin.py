from django.contrib import admin

from .models import SteamCode, Key, Shop, PurchaseType


@admin.register(SteamCode)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'value', 'status', 'key'
    )
    search_fields = ['code', 'value', 'status', 'key']


@admin.register(PurchaseType)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'amount', 'codes_list',
    )


@admin.register(Key)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'key',
    )
    search_fields = ['key']


@admin.register(Shop)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'guid', 'seller_id',
    )
    search_fields = ['name', 'guid', 'seller_id']

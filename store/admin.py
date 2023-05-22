from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

# Register your models here.
admin.site.register(Category)
admin.site.register(Top)
admin.site.register(Spacial)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    list_display_links = ['user', 'product']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_display_links = ['order', 'product', 'quantity']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'image']
    list_display_links = ['name', 'price', 'category', 'image']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_cart_items', 'get_cart_total', 'get_items']
    list_display_links = ['user', 'get_cart_items', 'get_cart_total']

    def get_items(self, obj):
        count = obj.orderitem_set.count()
        url = (
            reverse("admin:store_orderitem_changelist")
            + "?"
            + urlencode({"order__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} محصول</a>', url, count)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'family', 'pay', 'postcode']
    list_display_links = ['name', 'family', 'pay', 'postcode']

admin.site.site_header = 'مدیریت سایت'
admin.site.site_title = 'سایت فروشگاهی'
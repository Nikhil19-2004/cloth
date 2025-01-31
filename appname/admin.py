from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Contact)
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image')  # Show the image in the list display
    search_fields = ('name', 'category__name')
    filter = ('category')

admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('user__username',)

admin.site.register(CartItem)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('product__name', 'cart__user__username',)
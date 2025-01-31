from django.shortcuts import render
from .views import *
def cart(request):
	cart = Cart(request)
	context = {
		"cart": cart
	}
	return context
def cart_context_processor(request):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.products.all()
        cart_length = len(cart_items)
    except TypeError:
        cart_length = 0
    return {
        'cart_length': cart_length
    }
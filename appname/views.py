from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import stripe
from .forms import *

# Create your views here.

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request,"home.html")


def contact(request): 
    # if not request.user.is_authenticated:
    #     return redirect('login')
    if request.method== 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        sub= request.POST.get('sub')
        message= request.POST.get('message')
        print(name,email,sub,message)
        user= Contact(name=name, email=email, sub=sub, message=message)
        user.save()
    return render(request,"contact.html")

def aboutus(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request,"aboutus.html")

def account(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request,"account.html")

def cart(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request,"cart.html")

def privacy_policy(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request, 'terms_of_service.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Signup successful! Welcome!')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return redirect('logins')
    else:
         return render(request,'login.html')
    
def Account(request):
    frm= UserCreationForm()
    if request.method=='POST': 
        frm = UserCreationForm(request.POST) 
        if frm.is_valid(): 
            frm.save() 

    return render(request, 'account.html', {'fm':frm})
        
def logoutuser(request):
    logout(request)
    return redirect('login')

def product(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    categories = Category.objects.all()
    product = Product.objects.get(id=1)
    return render(request, 'product.html', {'categories': categories,'product':product})

def product_query(request):
    query = request.GET.get('q', '')
    if query:
        categories = Category.objects.filter(products__name__icontains=query).distinct()
    else:
        categories = Category.objects.all()
    return render(request, 'product.html', {'categories': categories, 'query': query})

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.products.all()  # Get CartItems related to the current Cart
    total_price = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart': cart})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} Added in your cart.")
    return redirect('cart')
    
def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from your cart.")
    return redirect('cart')

def pay_now(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        pass
    return render(request, 'checkout.html')

import logging
stripe.api_key = "sk_test_51PiV2tSHhsNN23Z1uaemlRWp0JTkiuLQk42Jib5ZT858F2UEPKGdoSnSi69XiBTL0TzTuZb3j44vCrQc647smSn000I8nEflJn"


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)  
    total_price = 0

    for cart_item in cart_items:
        unit_price_in_paise = int(cart_item.product.price * 100)
        item_total_amount = unit_price_in_paise * cart_item.quantity
        total_price += item_total_amount
    print(f"Total price of the cart: {total_price} paise")
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': total_price, 
                        'product_data': {
                            'name': "Cart Total",  
                        },
                    },
                    'quantity': 1, 
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            return HttpResponseBadRequest(f"Error creating checkout session: {str(e)}")
    else:
        return HttpResponseBadRequest("Invalid request method.")
def success(request):
    return render(request, 'success.html', {"payment_status": "success_url"})

def cancel(request):
    return render(request, 'cancel.html', {"payment_status": "cancel_url"})



def example_function(**kwargs):
  try:
    stripe.PaymentIntent.create(**kwargs)
  except stripe.error.CardError as e:
    logging.error("A payment error occurred: {}".format(e.user_message))
  except stripe.error.InvalidRequestError:
    logging.error("An invalid request occurred.")
  except Exception:
    logging.error("Another problem occurred, maybe unrelated to Stripe.")
  else:
    logging.info("No error.")
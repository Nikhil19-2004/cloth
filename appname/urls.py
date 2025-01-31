from django.urls import path
from .views import*

urlpatterns = [
    path('',home,name="home"),
    path('product/',product,name="product"),
    path('contact/',contact,name="contact"),
    path('aboutus/',aboutus,name="aboutus"),
    path('signup/',signup,name="signup"),
    path('account/',account,name="account"),
    path('login/',login,name="login"),
    path('logout/', logoutuser, name="logout"),
    path('cart/',cart,name="cart"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name="remove_from_cart"),
    path('privacy-policy/',privacy_policy, name='privacy_policy'),
    path('terms-of-service/',terms_of_service, name='terms_of_service'),
    path('pay_now/',pay_now,name='pay_now'),
    path('search/', product_query, name='product_query'),
    path('create-checkout-session/', create_checkout_session, name = "create-checkout-session"),
    path('success/', success, name = "success"),
    path('cancel/', cancel, name = "cancel"),
]









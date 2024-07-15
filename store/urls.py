from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('store/',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register"),
    path('logout/',views.logoutUser,name="logout"),
    path('chat/',views.websocket,name="chatting"),
    #path('personal/<str:pk>',views.personal,name="personal"),
    path('personal/',views.personal,name="personal"),
    path('product/<str:pk>',views.product,name="product"),
    path("wschat", views.chatPage, name="chat-page"),
    path('colour/',views.colourCoding,name="colourCoding"),
    path("outfit/", views.outfitlist, name="outfit"),
    path("outfit-chat/<str:pk>", views.fun_outfit, name="outfit-chat"),
    path("colcoding/<str:pk>", views.Colour, name="colcoding"),


]

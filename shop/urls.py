from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='ShopHome'),
    path('about/',views.about, name = "AboutUs"),
    path('contact/', views.contact, name = "ContactUs"),
    path('tracker/', views.tracker, name = 'tracker'),
    path('product/<int:myid>', views.productView, name = 'product'),
    path('search/',views.search, name = 'Search'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('signup',views.handleSignup, name = 'handleSignup'),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
]
    
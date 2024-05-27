# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name="index"),
#     path('cars', views.cars_page),
#     path('loginpage', views.login_page),
#     path('login', views.login),
#     path('registerpage', views.register_page),
#     path('register', views.register),
#     path('cars', views.cars_page), 
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('aboutus', views.aboutUs, name='AboutUs'),
    path('contactus', views.contactUs, name='ContactUs'),
    path('shoppingcart', views.shoppingCart, name='ShoppingCart'),
    path('faqs', views.fAQS, name='FAQS'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('order-success/', views.order_success, name='order_success'),
    
    path('create', views.create ,name='create'),  
    path('login', views.login,name='Login'), 
    path('cars', views.cars_page,name='cars_page'), 
    path('registerpage', views.register),	
    path('loginpage', views.login_page),	
    path('logout', views.logout),	
]
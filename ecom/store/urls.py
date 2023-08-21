from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index,name='index'),
    path('view_product/<int:id>/', views.view_product,name='view_product'),
    path('register/', views.register,name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'),name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'),name="logout"),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('addtowishlist/',views.add_to_wishlist,name='add_to_wishlist'),
    path('removefromwishlist/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('cart/',views.cart,name='cart'),
    path('addtocart/',views.add_to_cart,name='add_to_cart'),
    path('removefromcart/',views.remove_from_cart,name='remove_from_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('product_decrement/<int:id>/',views.product_decrement,name='product_decrement'),
    path('product_increment/<int:id>/',views.product_increment,name='product_increment'),
]
    


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from .models import Product,Wishlist,Cart,Order
# Register your models here.


admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)




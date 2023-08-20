from django.shortcuts import render,redirect
from .models import Product,Wishlist,Cart,carti
from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponse

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request,'store/index.html',{'products':products})


def view_product(request,id):
    product_obj = Product.objects.get(id=id)
    return render(request,'store/view_product.html',{'product_obj':product_obj})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')
    user_form = UserRegistrationForm()
    return render(request,'store/register.html',{'user_form':user_form})


def wishlist(request):
    wish_items = Wishlist.objects.filter(user=request.user)
    return render(request,'store/wishlist.html',{'wish_items':wish_items})


def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_obj-id')
        product_item = Product.objects.get(id=product_id)
        try:
            wish_item = Wishlist.objects.get(user=request.user,product=product_item)
            if wish_item:
                pass
        except:
             Wishlist.objects.create(user=request.user,product=product_item)
    
        finally:
               return redirect('wishlist')
          

def remove_from_wishlist(request):
    if request.method == 'POST':
       item_id = request.POST.get('item-id')
       Wishlist.objects.filter(id=item_id).delete()
       return redirect('wishlist')
    

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request,'store/cart.html',{'cart_items':cart_items})
   
    
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product-id')
        product_item = Product.objects.get(id=product_id)

        try:
            cart_item = Cart.objects.get(user=request.user,product=product_item)
            if cart_item:
                pass
        except:
             Cart.objects.create(user=request.user,product=product_item)
    
        finally:
               return redirect('cart')
        

def remove_from_cart(request):
    if request.method == 'POST':
       item_id = request.POST.get('item-id')
       Cart.objects.filter(id=item_id).delete()
       return redirect('cart')
    

def checkout(request):
    cartitems = Cart.objects.filter(user=request.user)
    product_qty = request.GET.get('quantity')
    # product_qty = int(product_qty)
    print(product_qty)
    total_price = 0

    for item in cartitems:
        total_price = total_price + item.product.price * product_qty

    context = {'cartitems':cartitems, 'total_price': total_price}
    return render(request,'store/checkout.html',context)
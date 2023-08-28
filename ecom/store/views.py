from django.shortcuts import render,redirect
from .models import Product,Wishlist,Cart,Order,User,Contact
from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    products = Product.objects.all()
    return render(request,'store/index.html',{'products':products})

@login_required(login_url='login')
def view_product(request,id):
    product_obj = Product.objects.get(id=id)
    return render(request,'store/view_product.html',{'product_obj':product_obj})

@login_required(login_url='login')
def product_decrement(request,id):
    cart_data=Cart.objects.all()
    data=[]
    for i in cart_data:
        if (i.user == request.user) and (id == i.product.id):
            data = i
    if data.product_quantity == 0:
        return HttpResponse("Not Allowed...")        
    else:
        data.product_quantity = data.product_quantity - 1
        data.save()
        return redirect('/cart/')

@login_required(login_url='login')
def product_increment(request,id):
    cart_data=Cart.objects.all()
    data=[]
    for i in cart_data:
        if (i.user == request.user) and (id == i.product.id):
            data = i
    data.product_quantity = data.product_quantity + 1
    data.save()
    return redirect('/cart/')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')
    user_form = UserRegistrationForm()
    return render(request,'store/register.html',{'user_form':user_form})

@login_required(login_url='login')
def wishlist(request):
    wish_items = Wishlist.objects.filter(user=request.user)
    return render(request,'store/wishlist.html',{'wish_items':wish_items})

@login_required(login_url='login')
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
          
@login_required(login_url='login')
def remove_from_wishlist(request):
    if request.method == 'POST':
       item_id = request.POST.get('item-id')
       Wishlist.objects.filter(id=item_id).delete()
       return redirect('wishlist')
    
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request,'store/cart.html',{'cart_items':cart_items})
   
@login_required(login_url='login')
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
               return redirect('wishlist')
        
@login_required(login_url='login')
def remove_from_cart(request):
    if request.method == 'POST':
       item_id = request.POST.get('item-id')
       Cart.objects.filter(id=item_id).delete()
       return redirect('cart')
    
@login_required(login_url='login')
def checkout(request):
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0

    for item in cartitems:
        total_price = total_price + item.product.price * item.product_quantity

    context = {'cartitems':cartitems, 'total_price': total_price}
    return render(request,'store/checkout.html',context)

@login_required(login_url='login')
def order(request):
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0

    for item in cartitems:
        total_price = total_price + item.product.price * item.product_quantity

    if total_price == 0:
        return HttpResponse("<h2>Please help yourself and add a product atleast to your cart</h2>")

    context = {'cartitems':cartitems, 'total_price': total_price}
    return render(request,'store/order.html',{'cartitems':cartitems,'total_price':total_price})

@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        cartitems = Cart.objects.filter(user=request.user)
        for i in cartitems:
            total_price = 0
            total_price = total_price + i.product.price * i.product_quantity
            Order.objects.create(user=request.user,Product=Product.objects.get(name=i.product.name),product_quantity=i.product_quantity,total_rupess=total_price)
    Cart.objects.all().delete()
    data=Order.objects.filter(user=request.user)
    return render(request,'store/success.html',{'data':data})


@login_required(login_url='login')
def Myorder(request):
    products=Order.objects.filter(user=request.user)
    total_ordered_amount = 0
    for items in products:
        total_ordered_amount += items.total_rupess
    return render(request,'store/Myorder.html',{'products':products,'total_ordered_amount':total_ordered_amount})

@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name,email,message)
        Contact.objects.create(name=name,email=email,message=message)
        return HttpResponse('<h2>Successfully Sent The Message!</h2>')
    return render(request,'store/contact.html')
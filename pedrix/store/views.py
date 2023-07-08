from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Product, Cart, CartItem, Order, OrderItem
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    customer = request.user.customer
    cart = Cart.objects.get(customer=customer)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def checkout(request):
    customer = request.user.customer
    cart = Cart.objects.get(customer=customer)
    total = 0
    for cart_item in cart.cartitem_set.all():
        total += cart_item.product.price * cart_item.quantity
    order = Order.objects.create(customer=customer, total=total)
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        # Reduzir o estoque do produto com base na quantidade comprada
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
    cart.delete()
    return redirect('order_confirmation')

@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

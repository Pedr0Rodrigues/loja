from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Cart, CartItem

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def product_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items})

def add_to_cart_view(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

def remove_from_cart_view(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    cart_item = CartItem.objects.get(id=cart_item_id, cart__user=user)
    cart_item.delete()
    
    return redirect('cart')

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Processar o pedido e finalizar a compra
        
        # Limpar o carrinho
        cart.cartitem_set.all().delete()
        
        # Redirecionar para a página de confirmação de pedido
        return redirect('order_confirmation')
    
    cart_items = cart.cartitem_set.all()
    return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items})

def order_confirmation_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()
    
    return render(request, 'order_confirmation.html', {'cart': cart, 'cart_items': cart_items})

def logout_view(request):
    logout(request)
    return redirect('login')


def create_products():
    products = [
        {
            'name': 'Poke Ball',
            'description': 'Descrição do Produto 1',
            'price': 200.00,
            'image': 'https://www.pokemongobrasil.com/wp-content/uploads/2016/08/pokebola-go.png',
        },
        {
            'name': 'Great Ball',
            'description': 'Descrição do Produto 2',
            'price': 600.00,
            'image': 'https://static.wikia.nocookie.net/pokemon/images/a/ac/Great_Ball_Artwork.png',
        },
        {
            'name': 'Ultra Ball',
            'description': 'Descrição do Produto 3',
            'price': 1200.00,
            'image': 'https://i.pinimg.com/originals/67/ea/dd/67eadd55b0734f51a603d07d9eabcddf.jpg',
        },
    ]
    
    for product_data in products:
        product = Product(**product_data)
        product.save()

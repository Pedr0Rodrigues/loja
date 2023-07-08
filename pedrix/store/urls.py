from django.urls import path
from store.views import (
    register_view,
    login_view,
    product_list_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
    checkout_view,
    order_confirmation_view,
    logout_view
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('product-list/', product_list_view, name='product_list'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order-confirmation/', order_confirmation_view, name='order_confirmation'),
    path('logout/', logout_view, name='logout'),
]

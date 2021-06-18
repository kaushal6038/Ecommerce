from django.urls import path, include
from .views import products_view, search_view, add_to_cart, charge, single_product, cart_view, payment_view, remove_product,update_product

urlpatterns = [
    path('', products_view, name='nm_marketplace_product_list'),
    path('single_product/<int:pk>', single_product, name='nm_marketplace_single_product'),
    path('search/', search_view, name='nm_marketplace_search'),
    path('add_to_cart/', add_to_cart, name='nm_marketplace_add_to_cart'),
    path('charge/', charge, name='nm_marketplace_charge'),
    path('cart/', cart_view, name='nm_marketplace_cart'),
    path('cart/payment/', payment_view, name='nm_marketplace_payment'),
    path('cart/remove_product/<int:pk>', remove_product, name='nm_marketplace_remove_product'),
    path('cart/update_product/', update_product, name='nm_marketplace_update_product')
]

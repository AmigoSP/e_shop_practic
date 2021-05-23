from django.shortcuts import render, redirect
from django.conf import settings
from django.core import serializers

# Create your views here.
from cart.cart import Cart
from products.products_settings import PRODUCTS_MODELS
from .forms import CartUpdateProduct


def cart_detail(request):
    form_qty = CartUpdateProduct()
    cart = request.session.get(settings.CART_USER_SESSION, Cart(request).cart)
    if any((not cart, cart.get('total_qty') in (0, '0'))):
        return render(request, 'cart/cart_empty.html', {'cart': 'Корзина пуста'})
    pre_products = {next(serializers.deserialize('json', product[0])).object: product[1] for product in
                    cart['products'].items()}
    cart['products'] = pre_products
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'form': form_qty})


def add_to_cart(request, subcategory_slug, product_pk):
    slug = subcategory_slug
    model = PRODUCTS_MODELS.get(slug)
    product = model.objects.get(pk=product_pk)
    user_cart = Cart(request)
    user_cart.add_product(product)
    return redirect('product_detail', slug_category=slug, product_slug=product.slug_url)

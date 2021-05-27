from django.core import serializers

from .cart import Cart


def cart(request):
    cart_customer = Cart(request).cart
    if any((not cart_customer, cart_customer.get('total_qty') in (0, '0'))):
        return {'cart': 'Корзина пуста'}
    if cart_customer.get('products'):
        pre_products = {next(serializers.deserialize('json', product[0])).object: product[1] for product in
                        cart_customer['products'].items()}
        cart_customer['products'] = pre_products
    return {'cart': cart_customer}

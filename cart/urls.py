from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<slug:subcategory_slug>/<int:product_pk>/', add_to_cart, name='add_to_cart'),
    path('update/', update_cart, name='update_cart')

]

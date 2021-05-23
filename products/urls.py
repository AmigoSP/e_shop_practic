from django.urls import path
from .views import main_page, ProductsView, ProductDetailView

urlpatterns = [
    path('product/category/<slug:slug_category>/<slug:product_slug>/', ProductDetailView.as_view(),
         name='product_detail'),
    path('product/category/<slug:slug_category>/', ProductsView.as_view(), name='category_list'),
    path('', main_page, name='main_page'),

]

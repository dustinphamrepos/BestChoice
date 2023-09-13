from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart_one_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_one_item, name='remove_cart_one_item'),
    path('remove_cart_all_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_all_item, name='remove_cart_all_item'),
    path('checkout/', views.checkout, name='checkout'),
]
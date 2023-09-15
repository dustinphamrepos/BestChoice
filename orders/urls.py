from django.urls import path
from . import views

urlpatterns = [
    path('place_order/<int:id_address>/', views.place_order, name='place_order'),
    path('order_complete/<int:order_number>/', views.order_complete, name='order_complete'),
    path('order_received/<int:order_number>/', views.order_received, name='order_received'),
]
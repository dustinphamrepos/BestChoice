from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('account_info/', views.account_info, name='account_info'),
  path('all_orders/', views.all_orders, name='all_orders'),
  path('wait_for_confirm_orders/', views.wait_for_confirm_orders, name='wait_for_confirm_orders'),
  path('waiting_orders/', views.waiting_orders, name='waiting_orders'),
  path('delivering_orders/', views.delivering_orders, name='delivering_orders'),
  path('delivered_orders/', views.delivered_orders, name='delivered_orders'),
  path('canceled_orders/', views.canceled_orders, name='canceled_orders'),
  path('account_address/', views.account_address, name='account_address'),
  path('account_delete_address/<int:address_id>/', views.account_delete_address, name='account_delete_address'),
  path('change_password/', views.change_password, name='change_password'),
  path('change_information/', views.change_information, name='change_information'),
]
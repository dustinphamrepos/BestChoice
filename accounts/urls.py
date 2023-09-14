from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('account_info/', views.account_info, name='account_info'),
  path('account_address/', views.account_address, name='account_address'),
  path('account_delete_address/<int:id>/', views.account_delete_address, name='account_delete_address'),
  path('change_password/', views.change_password, name='change_password'),
  path('change_information/', views.change_information, name='change_information'),
]
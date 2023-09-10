from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('account/', views.account, name='account'),
  path('change_password/', views.change_password, name='change_password'),
  path('change_information/', views.change_information, name='change_information'),
]
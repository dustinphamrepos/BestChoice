
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from orders.forms import AddressForm
from orders.models import Address, Order, OrderProduct
from carts.models import Cart, CartItem
from carts.views import _cart_id
from .models import Account
from .forms import RegistrationForm

# Create your views here.
def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      username = email.split('@')[0]

      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
      user.phone_number = phone_number
      user.save()
      messages.success(request=request, message="Register succeed!")
      return redirect('login')
    else:
      messages.error(request=request, message="Register failed!")
  else:
    form = RegistrationForm()
  context = {
    'form': form,
  }
  return render(request, 'accounts/register.html', context=context)

def login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = auth.authenticate(email=email, password=password)
    if user is not None:
      try:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        cart_items = CartItem.objects.filter(cart=cart)
        if cart_items.exists():
          product_variation = []
          for cart_item in cart_items:
            variations = cart_item.variations.all()
            product_variation.append(list(variations))

          existing_cart_items = CartItem.objects.filter(user=user)
          existing_variation_list = [list(item.variations.all()) for item in existing_cart_items]
          id = [item.id for item in existing_cart_items]

          for product in product_variation:
            if product in existing_variation_list:
              index = existing_variation_list.index(product)
              item_id = id[index]
              item = CartItem.objects.get(id=item_id)
              item.quantity += 1
              item.user = user
              item.save()
            else:
              cart_items = CartItem.objects.filter(cart=cart)
              for item in cart_items:
                item.user = user
                item.save()

      except Exception:
        pass
      auth.login(request=request, user=user)
      messages.success(request=request, message='Login succeed!')
      return redirect('home')
    else:
      messages.error(request=request, message="Login failed!")
  
  context = {
    'email': email if 'email' in locals() else '',
    'password': password if 'password' in locals() else ''
  }

  return render(request, 'accounts/login.html', context=context)

@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  messages.success(request=request, message='You are logged out.')
  return redirect('home')

@login_required(login_url='login')
def account_info(request):
  user = request.user
  active = 'info'
  context = {
    'user': user,
    'active': active
  }
  return render(request, 'accounts/account_info.html', context=context)

@login_required(login_url='login')
def change_password(request):
  if request.method == 'POST':
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if password == confirm_password:
      user = request.user
      user.set_password(password)
      user.save()
      messages.success(request, message='Password changed successfully.')
      return redirect('account_info')
    else:
      messages.error(request, message='Password do not match.')
  return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def change_information(request):
  user = request.user
  old_first_name = user.first_name
  old_last_name = user.last_name
  old_username = user.username
  old_email = user.email
  if user.phone_number:
    old_phone_number = user.phone_number
  else:
    old_phone_number = ''
  if request.method == 'POST':
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone_number = request.POST.get('phone_number')

    user.first_name = first_name
    user.last_name = last_name
    user.phone_number = phone_number
    user.save()
    messages.success(request, message='Information changed successfully.')
    return redirect('account_info')
  
  context = {
    'old_first_name': old_first_name,
    'old_last_name': old_last_name,
    'old_username': old_username,
    'old_email': old_email,
    'old_phone_number': old_phone_number,
  }
  return render(request, 'accounts/change_information.html', context=context)
  
def account_address(request):
  current_user = request.user
  active = 'address'
  list_address = Address.objects.filter(user=current_user)

  if list_address:
    list_address = list_address
  else:
    pass

  if request.method == 'POST':
    form = AddressForm(request.POST)
    if form.is_valid():
      address = Address()
      address.user = current_user
      address.first_name = form.cleaned_data['first_name']
      address.last_name = form.cleaned_data['last_name']
      address.phone_number = form.cleaned_data['phone_number']
      address.email = form.cleaned_data['email']
      address.city = form.cleaned_data['city']
      address.district = form.cleaned_data['district']
      address.precinct = form.cleaned_data['precinct']
      address.address_detail = form.cleaned_data['address_detail']
      
      address.save()

      messages.success(request=request, message='Saved!')

      return redirect('account_address')
    else:
      messages.error(request=request, message="Save failed!")

  else:
    form = AddressForm()

  context = {
    'form': form,
    'list_address': list_address,
    'active': active
  }

  return render(request, 'accounts/account_address.html', context=context)

def account_delete_address(request, address_id):
  address = Address.objects.get(id=address_id)
  address.delete()
  return redirect('account_address')

def all_orders(request):
  current_user = request.user
  active = 'all_orders'

  try:
    all_orders = Order.objects.filter(user=current_user)
  except Exception:
    pass

  context = {
    'user': current_user,
    'all_orders': all_orders if 'all_orders' in locals() else "",
    'active': active
  }

  return render(request, 'accounts/all_orders.html', context=context)

def wait_for_confirm_orders(request):
  active = 'wait_for_confirm_orders'
  try:
    wait_for_confirm_orders =  Order.objects.filter(status='Wait for confirmation')
  except Exception:
    pass
  
  context = {
    'wait_for_confirm_orders': wait_for_confirm_orders,
    'active': active
  }

  return render(request, 'accounts/wait_confirm_orders.html', context=context)

def waiting_orders(request):
  active = 'waiting_orders'
  try:
    waiting_orders =  Order.objects.filter(status='Waiting for delivery')
  except Exception:
    pass
  
  context = {
    'waiting_orders': waiting_orders,
    'active': active
  }

  return render(request, 'accounts/waiting_orders.html', context=context)

def delivering_orders(request):
  active = 'delivering_orders'
  try:
    delivering_orders =  Order.objects.exclude(status='Delivered')
  except Exception:
    pass
  
  context = {
    'delivering_orders': delivering_orders,
    'active': active
  }

  return render(request, 'accounts/delivering_orders.html', context=context)

def delivered_orders(request):
  active = 'delivered_orders'
  try:
    delivered_orders =  Order.objects.filter(status='Delivered')
  except Exception:
    pass
  
  context = {
    'delivered_orders': delivered_orders,
    'active': active
  }

  return render(request, 'accounts/delivered_orders.html', context=context)

def canceled_orders(request):
  active = 'canceled'
  try:
    canceled_orders =  Order.objects.filter(status='Canceled')
  except Exception:
    pass
  
  context = {
    'canceled_orders': canceled_orders,
    'active': active
  }

  return render(request, 'accounts/canceled_orders.html', context=context)
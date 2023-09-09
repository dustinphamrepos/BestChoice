
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
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
      return redirect('register')
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
def account(request):
  user = request.user
  context = {'user': user}
  return render(request, 'accounts/account.html', context=context)


from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from orders.models import Address

from carts.models import Cart, CartItem
from store.models import Product, Variation


def _cart_id(request):
  cart_id  = request.session.session_key
  if not cart_id:
    cart_id  = request.session.create()
  return cart_id

def cart(request, total=0, quantity=0, cart_items=None):
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request=request))
      cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
      total += cart_item.product.price * cart_item.quantity
      quantity += cart_item.quantity
    tax = total * 2 / 100
    grand_total = total + tax
  except ObjectDoesNotExist:
    pass

  context = {
    'total': total,
    'quantity': quantity,
    'cart_items': cart_items,
    'tax': tax if 'tax' in locals() else "",
    'grand_total': grand_total if 'tax' in locals() else 0
  }

  return render(request, 'store/cart.html', context=context)

def add_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  product_variations = list()
  if request.method == 'POST':
    for item in request.POST:
      key = item
      value = request.POST.get(key)
      try:
        variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
        product_variations.append(variation)
      except ObjectDoesNotExist:
        pass
  
  current_user = request.user
  if current_user.is_authenticated:
    is_exists_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
    if is_exists_cart_item:
      cart_items = CartItem.objects.filter(product=product, user=current_user)
      existing_variation_list = [list(item.variations.all()) for item in cart_items]
      id = [item.id for item in cart_items]
      if product_variations in existing_variation_list:
        index = existing_variation_list.index(product_variations)
        cart_item = CartItem.objects.get(id=id[index])
        cart_item.quantity += 1
      else:
        cart_item = CartItem.objects.create(product=product, user=current_user, quantity=1)
    else:
      cart_item = CartItem.objects.create(product=product, user=current_user, quantity=1)

  else:
    try:
      cart = Cart.objects.get(cart_id=_cart_id(request=request))
    except Cart.DoesNotExist:
      cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_exists_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_exists_cart_item:
      cart_items = CartItem.objects.filter(product=product, cart=cart)
      existing_variation_list = [list(item.variations.all()) for item in cart_items]
      id = [item.id for item in cart_items]
      if product_variations in existing_variation_list:
        index = existing_variation_list.index(product_variations)
        cart_item = CartItem.objects.get(id=id[index])
        cart_item.quantity += 1
      else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)

  if len(product_variations) > 0:
    cart_item.variations.clear()
    for item in product_variations:
      cart_item.variations.add(item)
  cart_item.save()
  return redirect('cart')

def remove_cart_one_item(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(id=cart_item_id, product=product, user=request.user)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
    
    if cart_item.quantity > 1:
      cart_item.quantity -= 1
      cart_item.save()
    else:
      cart_item.delete()
  except Exception:
    pass
  return redirect('cart')

def remove_cart_all_item(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(id=cart_item_id, product=product, user=request.user)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request=request))
      cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
    cart_item.delete()
  except Exception:
    pass
  return redirect('cart')

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
  current_user = request.user

  if current_user.phone_number:
    phone_number = current_user.phone_number
  else:
    phone_number = ''

  try:
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    for cart_item in cart_items:
      total += cart_item.product.price * cart_item.quantity
      quantity += cart_item.quantity
    tax = total * 2 / 100
    grand_total = total + tax
  except ObjectDoesNotExist:
    pass

  list_address = Address.objects.filter(user=current_user)

  context = {
    'current_user': current_user,
    'phone_number': phone_number,
    'total': total,
    'quantity': quantity,
    'cart_items': cart_items,
    'tax': tax if 'tax' in locals() else '',
    'grand_total': grand_total,
    'list_address': list_address if 'list_address' in locals() else ""
  }

  return render(request, 'store/checkout.html', context=context)
    



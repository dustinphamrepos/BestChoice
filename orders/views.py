import datetime
from django.shortcuts import redirect, render
from store.models import Product

from carts.models import CartItem
from orders.models import Order, OrderProduct, Address
from .forms import OrderForm

# Create your views here.
def place_order(request, total=0, quantity=0, id_address=None):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_count = cart_items.count()

  if cart_count <= 0:
    return redirect('store')
  
  grand_total = 0
  tax = 0
  for cart_item in cart_items:
    total += cart_item.product.price * cart_item.quantity
    quantity += cart_item.quantity
  tax = (2*total)/100
  grand_total = total + tax

  selected_address = Address.objects.get(user=current_user, id=id_address)

  if request.method == 'POST':
    data = Order()
    data.user = current_user
    data.first_name = selected_address.first_name
    data.last_name = selected_address.last_name
    data.phone_number = selected_address.phone_number
    data.email = selected_address.email
    data.city = selected_address.city
    data.district = selected_address.district
    data.precinct = selected_address.precinct
    data.address_detail = selected_address.address_detail
    data.order_note = request.POST.get('order_note')
    data.order_total = grand_total
    data.tax = tax
    data.ip = request.META.get('REMOTE_ADDR')
    data.is_ordered = False
    data.save()

    year = int(datetime.date.today().strftime('%Y'))
    day = int(datetime.date.today().strftime('%d'))
    month = int(datetime.date.today().strftime('%m'))
    date = datetime.date(year, month, day)
    current_date = date.strftime("%Y%m%d")
    order_number = current_date + str(data.id)
    data.order_number = order_number
    data.save()

    order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
    context = {
      'order': order,
      'cart_items': cart_items,
      'total': total,
      'tax': tax,
      'grand_total': grand_total,
    }
    return render(request, 'orders/order.html', context=context)
  else:
    return redirect('checkout')


def order_complete(request, order_number):
  current_user = request.user

  try:
    cart_items = CartItem.objects.filter(user=current_user)
    order = Order.objects.get(user=current_user, order_number=order_number)
    order.is_ordered = True
    order.save()
    ordered_products = OrderProduct.objects.filter(order__id=order.id)

    for item in cart_items:
      order_product = OrderProduct()
      order_product.order_id = order.id
      order_product.user_id = request.user.id
      order_product.product_id = item.product.id
      order_product.quantity = item.quantity
      order_product.product_price = item.product.price
      order_product.ordered = True
      order_product.save()

      cart_item = CartItem.objects.get(id=item.id)
      product_variation = cart_item.variations.all()
      order_product = OrderProduct.objects.get(id=order_product.id)
      order_product.variations.set(product_variation)
      order_product.save()

      product = Product.objects.get(id=item.product_id)
      product.stock -= item.quantity
      product.save()

    CartItem.objects.filter(user=request.user).delete()

    subtotal = 0
    for i in ordered_products:
      subtotal += i.product_price * i.quantity

    context = {
      'order': order,
      'ordered_products': ordered_products,
      'order_number': order.order_number, 
      'subtotal': subtotal,
    }
    return render(request, 'orders/order_complete.html', context=context)
  except Exception:
    return redirect('order_complete')

def order_received(request, order_number):
  current_user = request.user
  try:
    order_received = Order.objects.get(user=current_user, order_number=order_number)
    order_received.status = 'Delivered'
    order_received.save()
    order_products_received = OrderProduct.objects.filter(order__id=order_received.id)

    context = {
      'order_received': order_received,
      'order_products_received': order_products_received,
      'order_number': order_received.order_number, 
    }
    return render(request, 'orders/order_received.html', context=context)
  except Exception:
    return redirect('home')

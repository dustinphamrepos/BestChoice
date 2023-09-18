from django.db import models

from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
class Order(models.Model):
  STATUS = (
    ('Wait for confirmation', 'Wait for confirmation'),
    ('Waiting for delivery', 'Waiting for delivery'),
    ('Delivering', 'Delivering'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
  )

  user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
  order_number = models.CharField(max_length=20)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone_number = models.CharField(max_length=15)
  email = models.EmailField(max_length=50)
  city = models.CharField(max_length=50)
  district = models.CharField(max_length=50)
  precinct = models.CharField(max_length=60)
  address_detail = models.CharField(max_length=100)
  order_note = models.CharField(max_length=100, blank=True)
  order_total = models.FloatField()
  tax = models.FloatField()
  status = models.CharField(max_length=30, choices=STATUS, default='Delivering')
  ip = models.CharField(blank=True, max_length=20)
  is_ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def full_name(self):
    return "{} {}".format(self.first_name, self.last_name)

  def full_address(self):
    return "N. {}, {} district, {} precinct, {} city.".format(self.address_detail, self.precinct, self.district, self.city)

  def __str__(self):
    return self.first_name


class OrderProduct(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variations = models.ManyToManyField(Variation, blank=True)
  quantity = models.IntegerField()
  product_price = models.FloatField()
  ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.product.product_name
  
class Address(models.Model):
  user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
  order_number = models.CharField(max_length=20)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone_number = models.CharField(max_length=15)
  email = models.EmailField(max_length=50)
  city = models.CharField(max_length=50)
  district = models.CharField(max_length=50)
  precinct = models.CharField(max_length=60)
  address_detail = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def full_name(self):
    return "{} {}".format(self.first_name, self.last_name)
  
  def full_address(self):
    return "N. {}, {} district, {} precinct, {} city.".format(self.address_detail, self.precinct, self.district, self.city)

  def __str__(self):
    return "{} {} - {} {} {} {}".format(self.first_name, self.last_name, self.address_detail, self.precinct, self.district, self.city)



from django.shortcuts import get_object_or_404, render

from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    context = {
        'products': products
    }
    return render(request, 'store/store.html', context=context)

def product_detail(request, category_slug, product_slug=None):
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    context = {
        'single_product': single_product,
    }

    return render(request, 'store/product_detail.html', context=context)


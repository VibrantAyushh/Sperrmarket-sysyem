from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})



def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = Decimal(request.POST['price'])   # ✅ convert
        quantity = int(request.POST['quantity']) # ✅ convert

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )
        messages.success(request, "Product added successfully!")
        return redirect('product_list')

    return render(request, 'store/add_product.html')



def update_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.save()   # total_amount recalculates here
        return redirect('product_list')

    return render(request, 'store/update_product.html', {'product': product})



def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product_list')

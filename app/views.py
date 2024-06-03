from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from difflib import SequenceMatcher
from .models import Product, CartItem, Order
from django.contrib.auth.models import User


def header(request):
    return render(request, 'header.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('user_index')
    else:
        return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                return render(request, 'admin_login.html', {'error': 'You do not have permission to access this page.'})
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'admin_login.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def logout_view(request):
    logout(request)
    return redirect('admin_login')


def user_index(request):
    products = Product.objects.all()
    return render(request, 'user_index.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        specification = request.POST.get('specification')
        quantity = request.POST.get('quantity')  # Retrieve quantity from the form
        new_product = Product(name=name, specification=specification, quantity=quantity)
        new_product.save()  # Save the new product to the database
        return redirect('product_list')  # Redirect to product list page after adding product
    return render(request, 'add_product.html')


def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.quantity == 0:
        messages.error(request, 'Out of stock. Cannot remove product with zero quantity.')
        return redirect('admin_home')
    product.delete()
    messages.success(request, 'Product removed successfully.')
    return redirect('admin_home')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



def search_product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        try:
            product = Product.objects.get(pk=int(search_query))
        except (ValueError, Product.DoesNotExist):
            product = Product.objects.filter(name__icontains=search_query).first()
        if not product:
            messages.error(request, 'No product with this name or ID.')
            return render(request, 'admin_home.html')
        if product.quantity == 0:
            messages.warning(request, f'Product "{product.name}" is out of stock.')
        return render(request, 'product_search_results.html', {'product': product, 'products': products})
    return render(request, 'admin_home.html', {'products': products})

def generate_report(request):
    products = Product.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_report.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    y = 750
    p.drawString(100, y, "Product Report")
    y -= 20
    for product in products:
        p.drawString(100, y, f"Name: {product.name}, Quantity: {product.quantity}")
        y -= 20
    p.showPage()
    p.save()
    return response


def check_similarity(specification):
    products = Product.objects.all()
    max_similarity = 0
    similar_product = None
    
    for product in products:
        similarity = SequenceMatcher(None, specification, product.specification).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            similar_product = product
            
    return similar_product


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop.html', context)


def order_now(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        order = Order.objects.create(user=request.user, product=product)
        messages.success(request, 'Ordered successfully.')
        return redirect('shop')
    return render(request, 'shop.html')


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        CartItem.objects.create(user=request.user, product=product, quantity=1)
        messages.success(request, 'Added to cart successfully.')
        return redirect('shop')
    return redirect('shop')


def user_search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        try:
            if query:
                search_results = Product.objects.filter(name__icontains=query)
                return render(request, 'user_search_result.html', {'products': search_results})
            else:
                return render(request, 'user_search_result.html', {'products': []})
        except Exception as e:
            return render(request, 'user_search_result.html', {'products': []})
    else:
        return render(request, 'user_search_result.html', {'products': []})


def view_order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'view_order_list.html', {'orders': orders})

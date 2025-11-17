import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from main.forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import requests
import json

# Create your views here.
@login_required(login_url='/login')
def show_main_page(request):
    context = {
        'name' : 'Fitto Fadhelli Voltanie Ariyana',
        'npm' : '2406423401',
        'class' : 'PBP F',
        'categories': Product.SPORTS_PRODUCT_CATEGORY,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, 'main.html', context)

def not_found_error_page(request, exception):
    return render(request, 'notfound.html', status=404)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main_page')

    context = {'form': form}
    return render(request, "product_form.html", context)

@login_required(login_url='/login')
def show_detail(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product':product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize('xml', product_list)
    return HttpResponse(xml_data, content_type='application/xml')

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id' : str(product.id),
            'name' : product.name,
            'price' : product.price,
            'description' : product.description,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'is_featured' : product.is_featured,
            'stock' : product.stock,
            'quantity_purchased' : product.quantity_purchased,
            'user_id': product.user_id
        }
        for product in product_list
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    try:
        product = Product.objects.filter(pk=id)
        xml_data = serializers.serialize('xml', product)
        return HttpResponse(xml_data, content_type='application/xml')
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, id):
    try:
        product = Product.objects.select_related('user').get(pk=id)
        data = {
            'id' : str(product.id),
            'name' : product.name,
            'price' : product.price,
            'description' : product.description,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'is_featured' : product.is_featured,
            'stock' : product.stock,
            'quantity_purchased' : product.quantity_purchased,
            'user_id' : product.user.id,
            'user_username' : product.user.username if product.user_id else None,
        }

        return JsonResponse(data)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

@login_required(login_url='/login')
def get_product_json(request):
    category_filter = request.GET.get("category")
    user_filter = request.GET.get("filter")

    product_list = Product.objects.all()

    if category_filter:
        product_list = product_list.filter(category=category_filter)
    if user_filter == 'my':
        product_list = product_list.filter(user=request.user)

    data = [
        {
            'id' : str(product.id),
            'name' : product.name,
            'price' : product.price,
            'description' : product.description,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'category_display' : product.get_category_display(),
            'is_featured' : product.is_featured,
            'stock' : product.stock,
            'quantity_purchased' : product.quantity_purchased,
            'user_username' : product.user.username if product.user else None,
        }
        for product in product_list
    ]
    return JsonResponse(data, safe=False)


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        
    context = {'form':form}
    return render(request, 'register.html', context)


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main_page"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_POST
def login_ajax(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            response = JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'user': {
                    'username': user.username,
                    'last_login': str(datetime.datetime.now())
                }
            })
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Account is disabled'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid username or password'
        }, status=400)

@csrf_exempt
@require_POST
def register_ajax(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 != password2:
        return JsonResponse({
            'status': 'error',
            'message': 'Passwords do not match'
        }, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Username already exists'
        }, status=400)

    user = User.objects.create_user(username=username, password=password1)
    user.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Account created successfully'
    })

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main_page')

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('main:show_main_page')


@csrf_exempt
@require_POST
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    category = request.POST.get("category", "uncategorized")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    stock = request.POST.get("stock", 0)

    # konversi harga & stok ke integer jika ada
    try:
        price = int(price)
    except (TypeError, ValueError):
        price = 0
    try:
        stock = int(stock)
    except (TypeError, ValueError):
        stock = 0

    user = request.user if request.user.is_authenticated else None

    new_product = Product(
        name=name,
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        stock=stock,
        user=user
    )
    new_product.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Product created successfully',
        'product': {
            'id': str(new_product.id),
            'name': new_product.name,
            'price': new_product.price,
            'description': new_product.description,
            'thumbnail': new_product.thumbnail,
            'category': new_product.category,
            'is_featured': new_product.is_featured,
            'stock': new_product.stock,
            'quantity_purchased': new_product.quantity_purchased,
            'user_username': new_product.user.username if new_product.user else None,
        }
    }, status=201)

@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    category = request.POST.get("category", "uncategorized")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'
    stock = request.POST.get("stock", 0)

    try:
        price = int(price)
    except (TypeError, ValueError):
        price = 0
    try:
        stock = int(stock)
    except (TypeError, ValueError):
        stock = 0

    product.name = name
    product.price = price
    product.description = description
    product.category = category
    product.thumbnail = thumbnail
    product.is_featured = is_featured
    product.stock = stock
    product.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Product updated successfully',
        'product': {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'stock': product.stock,
            'quantity_purchased': product.quantity_purchased,
            'user_username': product.user.username if product.user else None,
        }
    })

@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return JsonResponse({'status': 'success', 'message': 'Product deleted successfully'})


def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))
        price = data.get("price")
        description = strip_tags(data.get("description", ""))
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        stock = data.get("stock", 0)
        user = request.user
        
        product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            stock=stock,
            user=user
        )

        product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def my_products_json_flutter(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)
    
    products = Product.objects.filter(user=request.user)
    data = [
        {
            'id' : str(product.id),
            'name' : product.name,
            'price' : product.price,
            'description' : product.description,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'is_featured' : product.is_featured,
            'stock' : product.stock,
            'quantity_purchased' : product.quantity_purchased,
            'user_id': product.user_id
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)

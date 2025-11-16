from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import datetime
import json
import requests

from main.forms import ProductForm
from main.models import Product

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        # Fetch image from external source
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        if response.status_code == 200:
            # Return the image with proper content type
            return HttpResponse(
                response.content,
                content_type=response.headers.get('Content-Type', 'image/jpeg')
            )
        else:
            # If the external site returned an error (404, 403, etc.), 
            # we return a 404 Not Found to the Flutter app.
            return HttpResponse('Image not found or access denied', status=404)
    except requests.RequestException as e:
        print("\n--- PROXY IMAGE CRASH ---")
        print(f"Failed to fetch: {image_url}")
        print(f"The error was: {e}")
        print("-------------------------\n")
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)


@csrf_exempt
def add_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        price = data.get("price", 0)
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        thumbnail = data.get("thumbnail", "")
        category = data.get("category", "")
        is_featured = data.get("is_featured", False)
        
        new_product = Product(
            user=request.user,  
            name=name,
            price=price,
            description=description,
            thumbnail=thumbnail,
            category=category,
            is_featured=is_featured,
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    form = ProductForm()
    context = {
        'project' : 'majulah shop',
        'name': request.user.username,
        'npm' : 2406396584,
        'class': 'PBP D',
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'form': form,
    }
    return render(request, "main.html", context)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_product_ajax(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        
        return JsonResponse({"status": "success", "message": "Product added successfully!"}, status=201)
    else:
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_POST
@login_required(login_url='/login')
def delete_product_ajax(request):
    try:
        data = json.loads(request.body)
        product = get_object_or_404(Product, pk=data["id"])

        if product.user != request.user:
            return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

        product.delete()
        return JsonResponse({"status": "success", "message": "Product deleted"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

def add_product(request):
    form = ProductForm()
    context = {'form': form}
    return render(request, "add_product.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user == request.user:
        product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product': product}
    return render(request, "product_detail.html", context)

def show_json(request):
    products = Product.objects.select_related('user').all()
    data = []
    for product in products:
        data.append({
                'id': str(product.id),
                "user": product.user.id if product.user else None,
                "username": product.user.username if product.user else None,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "category": product.category,
                "thumbnail": product.thumbnail,
                "is_featured": product.is_featured,
            }
        )
    return JsonResponse(data, safe=False)

def show_json_by_id(request, id):
    try:
        product = Product.objects.get(pk=id)
        data = [{
                "id": str(product.id),
                "user": product.user.id if product.user else None,
                "username": product.user.username if product.user else None,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "category": product.category,
                "thumbnail": product.thumbnail,
                "is_featured": product.is_featured,
            }
        ]
        return JsonResponse(data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)


def show_xml(request):
    product_list = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", product_list), content_type="application/xml")

def show_xml_by_id(request, id):
    try:
        product = Product.objects.get(pk=id)
        return HttpResponse(serializers.serialize("xml", [product]), content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
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
def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully! You can now log in.'}, status=201)
        else:
            # Return form errors as JSON
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = JsonResponse({'status': 'success', 'message': 'Login successful! Redirecting...'})
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
        # Provide a more specific error message
        return JsonResponse({'status': 'error', 'message': 'Invalid username or password. Please try again.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

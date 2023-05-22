import json
from django.shortcuts import render
from .models import *
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as logins
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *

# Create your views here.
def main(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    tops = Top.objects.all()
    spacials = Spacial.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
        else:
            order_items = []
        favorites = Favorite.objects.filter(user=request.user)
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET.get('name')
        cat = request.GET.get('category')
        if cat == '0':
            products = Product.objects.filter(name__contains=name)
        else:
            products = Product.objects.filter(category=cat, name__contains=name)
        page = request.GET.get('page')
        paginator = Paginator(products, 6)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages) 
    else:
        page = request.GET.get('page')
        paginator = Paginator(products, 6)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages) 
    return render(request, 'main.html', {'categories':categories, 'products': products, 'order': order, 'order_items': order_items, 'tops': tops, 'spacials': spacials, 'favorites': favorites})

def category(request, category_name):
    categories = Category.objects.all()
    products = Product.objects.filter(category__name=category_name)
    tops = Top.objects.all()
    spacials = Spacial.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
        else:
            order_items = []
        favorites = Favorite.objects.filter(user=request.user)
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}
    page = request.GET.get('page')
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'main.html', {'categories':categories, 'products': products, 'order': order, 'order_items': order_items, 'tops': tops, 'spacials': spacials, 'favorites': favorites})

def product(request, product_name):
    categories = Category.objects.all()
    if Product.objects.filter(name=product_name.replace('-', ' ')).exists():
        product = Product.objects.get(name=product_name.replace('-', ' '))
    else:
        product = None
    favorite = False
    already = False
    qt = 1
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
            if order_items.filter(product=product).exists():
                already = True
                qt = order_items.get(product=product).quantity
        else:
            order_items = []
        favorites = Favorite.objects.filter(user=request.user)
        if favorites.filter(product=product).exists():
            favorite = True
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}
    return render(request, 'product.html', {'categories':categories, 'product': product, 'order': order, 'order_items': order_items, 'already': already, 'qt': qt, 'favorites': favorites, 'favorite': favorite})

def checkout(request):
    categories = Category.objects.all()
    form = PayForm()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
        else:
            order_items = []
        favorites = Favorite.objects.filter(user=request.user)
        if request.method == 'POST':
            form = PayForm(data=request.POST)
            form.instance.order = order
            form.instance.pay = order.get_cart_total
            if form.is_valid() and order.get_cart_items > 0:
                form.save()
                for orderitem in order_items:
                    orderitem.delete()
                messages.success(request, 'خرید با موفقیت انجام شد')
                return HttpResponseRedirect(reverse('checkout'))
            else:
                for error in form.errors:
                    messages.error(request, form.errors[error][0])
                if order.get_cart_items <= 0:
                    messages.error(request, 'سبد خرید شما خالی است')
                return HttpResponseRedirect(reverse('checkout'))
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}

    return render(request, 'checkout.html', {'categories':categories, 'order': order, 'order_items': order_items, 'favorites': favorites, 'form': form})

@login_required
def cart(request):
    categories = Category.objects.all()
    order, created = Order.objects.get_or_create(user=request.user)
    if order.get_cart_items > 0:
        order_items = OrderItem.objects.filter(order=order)
    else:
        order_items = []
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'cart.html', {'categories': categories, 'order': order, 'order_items': order_items, 'favorites': favorites})

@login_required
def favorite(request):
    categories = Category.objects.all()
    order, created = Order.objects.get_or_create(user=request.user)
    if order.get_cart_items > 0:
        order_items = OrderItem.objects.filter(order=order)
    else:
        order_items = []
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite.html', {'categories': categories, 'order': order, 'order_items': order_items, 'favorites': favorites})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main'))
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            logins(request, user)
            return HttpResponseRedirect(reverse('main'))
        else:
            for error in form.errors:
                messages.error(request, form.errors[error][0])
            return HttpResponseRedirect(reverse('login'))
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
        else:
            order_items = []
            favorites = {'count': 0}
        favorites = Favorite.objects.filter(user=request.user)
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}
    return render(request, 'login.html', {'categories':categories, 'order': order, 'order_items': order_items, 'form': form, 'favorites': favorites})

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            for error in form.errors:
                messages.error(request, form.errors[error][0])
            return HttpResponseRedirect(reverse('signup'))
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
        else:
            order_items = []
        favorites = Favorite.objects.filter(user=request.user)
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}
    return render(request, 'signup.html', {'categories':categories, 'order': order, 'order_items': order_items, 'form': form, 'favorites': favorites})

@login_required
def addcart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    quantity = data['quantity']
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderitem.quantity = quantity
    orderitem.save()
    return JsonResponse({'message': product_id + ' added to cart'})

@login_required
def delcart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderitem.delete()

    return JsonResponse({'message': product_id + ' deleted from cart'})

@login_required
def edit(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'del':
        if orderitem.quantity > 1:
            orderitem.quantity -= 1
    orderitem.save()
    return JsonResponse({'product_id': product_id, 'action': action})

@login_required
def favor(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    if Favorite.objects.filter(user=request.user, product=product).exists():
        favor = Favorite.objects.get(user=request.user, product=product)
        favor.delete()
    else:
        favor = Favorite.objects.create(user=request.user, product=product)
        favor.save()
    return JsonResponse({'product_id': product_id, 'user': request.user.username})

def page404(request, exception=None):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
        if order.get_cart_items > 0:
            order_items = OrderItem.objects.filter(order=order)
        else:
            order_items = []
        favorites = Favorite.objects.filter(user=request.user)
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0} 
        order_items = []
        favorites = {'count': 0}
    return render(request, '404.html', {'categories': categories, 'order': order, 'order_items': order_items, 'favorites': favorites})

def api_login(request):
    if request.user.is_authenticated:
        return JsonResponse(json.dumps({'message': 'already logged'}), safe=False)
    form = LoginForm()
    if request.method == 'GET':
        form = LoginForm(data=request.GET)
        if form.is_valid():
            user = form.get_user()
            logins(request, user)
            return JsonResponse(json.dumps({'message': 'login successfully'}), safe=False)
        else:
            errors = []
            for error in form.errors:
                errors.append(form.errors[error][0])
            return JsonResponse(json.dumps({'message': 'error', 'errors': errors}), safe=False)
    
def api_main(request):
    categories = Category.objects.all()
    tops = Top.objects.all()
    spacials = Spacial.objects.all()
    data = {'categories': [c.name for c in categories], 'tops': [t.serialize() for t in tops], 'specials': [s.serialize() for s in spacials]}
    return JsonResponse(json.dumps(data), safe=False)

def api_products(request, page):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages) 
    data = {'products': [p.serialize() for p in products], 'next': products.has_next(), 'previous': products.has_previous()}

    return JsonResponse(json.dumps(data), safe=False)

def api_product(request, product_name):
    if Product.objects.filter(name=product_name).exists():
        product = Product.objects.get(name=product_name)
        data = {'product': product.serialize()}
    else:
        data = {'product': ''}
        
    return JsonResponse(json.dumps(data), safe=False)
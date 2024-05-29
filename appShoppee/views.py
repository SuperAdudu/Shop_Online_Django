from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.parsers import FormParser, MultiPartParser
# Create your views here.



def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}

    return render(request,'appShop/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is not correct!')

    context = {}
    return render(request,'appShop/login.html',context)

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        keys = Product.objects.filter(name__icontains=searched) 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItem = order['get_cart_items']

    products = Product.objects.all()
    return render(request,'appShop/search.html',{'searched':searched,'keys':keys,'products':products,'cartItem':cartItem})

def category(request):
    categories = Categories.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug=active_category) 

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItem = order['get_cart_items']

    context = {'categories':categories,'products':products,'active_category':active_category,'cartItem':cartItem}
    return render(request,'appShop/category.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItem = order['get_cart_items']

    products = Product.objects.all()
    categories = Categories.objects.filter(is_sub=False)
    context = {'products':products,'cartItem':cartItem,'categories':categories}
    return render(request, 'appShop/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items

    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItem = order['get_cart_items']

    categories = Categories.objects.filter(is_sub=False)
    context = {'items':items,'order':order,'cartItem':cartItem,'categories':categories}
    return render(request, 'appShop/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items

    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItem = order['get_cart_items']

    categories = Categories.objects.filter(is_sub=False)
    context = {'items':items,'order':order,'cartItem':cartItem,'categories':categories}
    return render(request, 'appShop/checkout.html',context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items

    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItem = order['get_cart_items']

    id = request.GET.get('id','')    
    products = Product.objects.filter(id=id)
    categories = Categories.objects.filter(is_sub=False)
    context = {'items':items,'order':order,'cartItem':cartItem,'categories':categories,'products':products}
    return render(request, 'appShop/detail.html',context)

def updateItem(request):
    if  request.method == 'POST':

        try:
            data = json.loads(request.body)
            productId = data['productId']
            action = data['action']
            customer = request.user
            product = Product.objects.get(id = productId)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            if action == 'add':
                orderItem.quatity +=1
            elif action == 'remove':
                orderItem.quatity -=1
            orderItem.save()
            if orderItem.quatity <= 0:
                orderItem.delete()
        except json.JSONDecodeError as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse('added',safe=False)

def information(request):
    return render(request,'appShop/information.html')



class GetAllProduct(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        productData = GetAllProductSerializer(products,many=True)
        return Response(data=productData.data)
    
class GetProductWithSearch(APIView):

    parser_classes = [FormParser, MultiPartParser]
    def get(self, request, format=None):
        name = request.data.get('name', '')
        if name:
            products = Product.objects.filter(name__icontains=name)
        else:
            products = Product.objects.all()

        productData = GetAllProductSerializer(products,many=True)
        return Response(data=productData.data)
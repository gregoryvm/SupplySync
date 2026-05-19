from rest_framework.decorators import APIView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, User
from .queries import (
    all_products,
    create_user,
    create_update_product,
    get_product
   
)
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
# User = get_user()

# https://medium.com/@michal.drozdze/setting-up-a-django-api-with-django-rest-framework-drf-a-beginners-guide-cee5d61f00a6
# https://www.youtube.com/watch?v=sAlRlLTWrHA
# ~~ Work in progress ~~


# Create your views here.
class UsersView(APIView):
#class ProductsView(generics.CreateAPIView):
    # temporary filler

    
    def signup_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                create_user(user_name=form.cleaned_data.get('username'), user_password=form.cleaned_data.get('password1'))
                user = form.get_user()
                login(request,user)
                return redirect('supplysync:inventory')
        else:
            form = UserCreationForm()
        return render(request,"signup.html",{'form':form})
    
    def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('supplysync:inventory')
        else:
            form = AuthenticationForm()
        return render(request,"login.html",{'form':form})

    def logout_view(request):
        if request.method == 'POST':
            logout(request)
            return redirect('supplysync:home')
    
    def home(request):
        return render(request,"home.html")
    
class ProductsView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def inventory_view(request):
        #products = all_products(request.user.username)
        products = get_product(name=request.GET.get('q'),
                                sku=request.GET.get('q'),
                                category=request.GET.get('q'),
                                user_name=request.user.username,
                                quantity_min=request.GET.get('q_min') or None,
                                quantity_max=request.GET.get('q_max') or None,
                                weight_min=request.GET.get('w_min') or None,
                                weight_max=request.GET.get('w_max') or None,
                                cost_min=request.GET.get('c_min') or None,
                                cost_max=request.GET.get('c_max') or None,
                                price_min=request.GET.get('p_min') or None,
                                price_max=request.GET.get('p_max') or None,
                                )
        
        return render(request,"inventory.html",{"products":products})

    def create_view(request):
        if request.method == 'POST':
           create_update_product(prod_name=request.POST.get('product_name'),
                                 prod_sku=request.POST.get('product_sku'),
                                 prod_category=request.POST.get('product_category'),
                                 user_name=request.user.username, 
                                 prod_quantity=request.POST.get('product_quantity'),
                                 prod_weight=request.POST.get('product_weight'),
                                 prod_cost=request.POST.get('product_cost'),
                                 prod_price=request.POST.get('product_price'))
           return redirect('supplysync:inventory')
            
        return render(request,"create_product.html")

    # def get(self, request):
    #    user = self.request.user
    #    products = all_products(user)
    #    serializer = ProductSerializer(products, many=True)
    #    return Response(serializer.data)

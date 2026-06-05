from rest_framework.decorators import APIView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Product, User
from .queries import (
    all_products,
    create_user,
    create_update_product,
    get_product,
    delete_product,
    update_user,
    delete_user,
    get_user
   
)
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
import re
# User = get_user()

# https://medium.com/@michal.drozdze/setting-up-a-django-api-with-django-rest-framework-drf-a-beginners-guide-cee5d61f00a6
# https://www.youtube.com/watch?v=sAlRlLTWrHA
# ~~ Work in progress ~~


# Create your views here.

def home(request):
        return render(request,"home.html")

class UsersView(APIView):
#class ProductsView(generics.CreateAPIView):
    # temporary filler

    
    def signup_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                create_user(user_name=form.cleaned_data.get('username'), user_password=form.cleaned_data.get('password1'))
                #user = form.get_user()
                login(request,user)
                return redirect('supplysync:products')
        else:
            form = UserCreationForm()
        return render(request,"signup.html",{'form':form})
    
    def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('supplysync:products')
        else:
            form = AuthenticationForm()
        return render(request,"login.html",{'form':form})

    def logout_view(request):
        if request.method == 'POST':
            logout(request)
            return redirect('supplysync:home')
        
    @login_required 
    def account_view(request):          
        if request.method == 'POST':
            new_username = request.POST.get('newname')
            new_password = request.POST.get('newpassword')     
            
            if new_username and not re.fullmatch(r"[A-Za-z0-9@.+_-]+", new_username):
                messages.error(request, "Invalid username characters.")
                return redirect('supplysync:account')
            elif len(new_username) > 150:
                messages.error(request, "Username too long.")
                return redirect('supplysync:account')
            elif new_password and len(new_password) < 8:
                messages.error(request, "Password too short.")
                return redirect('supplysync:account')
            elif new_username and get_user(new_username) != "User Not Found.":
                messages.error(request, "Username already taken.")
                return redirect('supplysync:account')
            elif new_password and validate_password(new_password,user=request.user) is not None:
                messages.error(request, "Invalid password.")
                return redirect('supplysync:account')
            else:
                update_user(user_name=request.user.username,
                            new_name=new_username or None,
                            new_password=new_password or None
                            )
                user = request.user
                if new_username:
                    user.username = request.POST.get('newname')
                if new_password:   
                    user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            return redirect('supplysync:products')
        return render(request,"account.html")
    
    @login_required 
    def delete_view(request):  
        if request.method == 'POST':
           delete_user(user_name=request.user.username)  
           request.user.delete()
           
        return redirect('supplysync:home')
    
    
class ProductsView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def inventory_view(request):
        #products = all_products(request.user.username)
        if request.method == 'GET':
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
           return redirect('supplysync:products')  
        return render(request,"create_product.html")
    
    def delete_view(request,name,sku):
        if request.method == 'POST':
           delete_product(prod_name=name,
                                 prod_sku=sku,
                                 user_name=request.user.username)  
        return redirect('supplysync:products')
    
    def edit_view(request,name,sku):
        product = get_product(name=name,
                                    sku=sku,
                                    user_name=request.user.username,
                                    )
        product = product.first()
        if request.method == 'POST':
            create_update_product(prod_name=request.POST.get('product_name'),
                                 prod_sku=request.POST.get('product_sku'),
                                 prod_category=request.POST.get('product_category'),
                                 user_name=request.user.username, 
                                 prod_quantity=request.POST.get('product_quantity'),
                                 prod_weight=request.POST.get('product_weight'),
                                 prod_cost=request.POST.get('product_cost'),
                                 prod_price=request.POST.get('product_price'))
            return redirect('supplysync:products')
        return render(request,"edit_product.html",{"product":product})

    # def get(self, request):
    #    user = self.request.user
    #    products = all_products(user)
    #    serializer = ProductSerializer(products, many=True)
    #    return Response(serializer.data)

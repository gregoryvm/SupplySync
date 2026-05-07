from rest_framework.decorators import APIView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, User
from .queries import (
    all_products,
    create_user
)
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
# User = get_user()

# https://medium.com/@michal.drozdze/setting-up-a-django-api-with-django-rest-framework-drf-a-beginners-guide-cee5d61f00a6
# https://www.youtube.com/watch?v=sAlRlLTWrHA
# ~~ Work in progress ~~


# Create your views here.
class ProductsView(APIView):

    # temporary filler
    def inventory_view(request):
        return render(request,"inventory.html")
    
    def signup_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                create_user(user_name=form.cleaned_data.get('username'), user_password=form.cleaned_data.get('password1'))
                #User.objects.create(name=form.get('username'),password=form.get('password'))
                return redirect('supplysync:inventory_view')
        else:
            form = UserCreationForm()
        return render(request,"signup.html",{'form':form})
    
    def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                return redirect('supplysync:inventory_view')
        else:
            form = AuthenticationForm()
        return render(request,"login.html",{'form':form})
    
    def home(request):
        return render(request,"home.html")

    # def get(self, request):
    #    user = self.request.user
    #    products = all_products(user)
    #    serializer = ProductSerializer(products, many=True)
    #    return Response(serializer.data)

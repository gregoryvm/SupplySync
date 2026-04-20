from rest_framework.decorators import APIView
from django.shortcuts import render
from .models import Product, User
from .queries import *
from rest_framework.response import Response
from .serializers import ProductSerializer 
#User = get_user()

# https://medium.com/@michal.drozdze/setting-up-a-django-api-with-django-rest-framework-drf-a-beginners-guide-cee5d61f00a6
# ~~ Work in progress ~~

# Create your views here.
class ProductsView(APIView):
    def get(self,request):
        user = self.request.user
        products = all_products(user)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
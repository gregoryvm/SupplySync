from rest_framework import serializers
from .models import  User, Product


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id','name','password']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_id','name','sku','category','user','quantity','weight','cost','price']





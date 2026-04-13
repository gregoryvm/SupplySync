from django.shortcuts import render
from .models import Product
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,'supplysync_app/home.html',{"products":products})
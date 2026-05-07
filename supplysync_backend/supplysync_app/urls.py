from django.urls import path
from . import views

app_name = 'supplysync'

urlpatterns = [
    path('inventory/', views.ProductsView.inventory_view, name='inventory_view'),
    path('signup/', views.ProductsView.signup_view, name='signup'),
    path('login/', views.ProductsView.login_view, name='login'),
    path('', views.ProductsView.home, name='home'),
]
    
from django.urls import path
from . import views
#from .views import ProductsView


urlpatterns = [
    path('',views.ProductsView.home_view,name='home_view'),
]
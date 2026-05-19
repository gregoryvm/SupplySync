from django.urls import path
from . import views
#from views import ProductsView
app_name = 'supplysync'

urlpatterns = [
    
    path('signup/', views.UsersView.signup_view, name='signup'),
    path('login/', views.UsersView.login_view, name='login'),
    path('logout/', views.UsersView.logout_view, name='logout'),
    path('', views.UsersView.home, name='home'),
    #path('', views.ProductsView.as_view(), name='home'),
    path('inventory/', views.ProductsView.inventory_view, name='inventory'),
    path('create/', views.ProductsView.create_view, name='create'),
]
    
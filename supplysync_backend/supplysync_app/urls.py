from django.urls import path
from . import views
#from views import ProductsView
app_name = 'supplysync'

urlpatterns = [
    path('', views.home, name='home'),

    path('account/signup/', views.UsersView.signup_view, name='signup'),
    path('account/login/', views.UsersView.login_view, name='login'),
    path('account/logout/', views.UsersView.logout_view, name='logout'),
    path('account/delete/', views.UsersView.delete_view, name='delete'),
    path('account/', views.UsersView.account_view, name='account'),

    path('products/', views.ProductsView.inventory_view, name='products'),
    path('products/create/', views.ProductsView.create_view, name='create-product'),
    path('products/delete/<str:name>/<str:sku>', views.ProductsView.delete_view, name='delete'),
    path('products/edit/<str:name>/<str:sku>', views.ProductsView.edit_view, name='edit'),
]
    
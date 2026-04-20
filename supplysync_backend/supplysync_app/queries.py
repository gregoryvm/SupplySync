from django.db.models.query import QuerySet

from .models import (
    User,
    Product
)

MAX_STRING = 200

#    user_id = models.AutoField(primary_key=True)
#    name = models.CharField(max_length=200)
#    password = models.CharField(max_length=200)

#    product_id = models.AutoField(primary_key=True)
#    name = models.CharField(max_length=200)
#    sku = models.CharField(max_length=200)
#    category = models.CharField(max_length=200)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    quantity = models.IntegerField()
#    weight = models.FloatField()
#    cost =  models.FloatField()
#    price =  models.FloatField()


# ADD CONTRAINTS VIA CONSTANTS

def create_update_user(user_name: str, user_password: str):
    product_obj, created = User.objects.get_or_create(name=user_name,password=user_password)
    if created is False:
        product_obj.name = user_name
        product_obj.password = user_password
        product_obj.save()
        result = "User Updated."
    else:
        result = "User Created."
    return result

def get_user(id: int, user_name: str):
    # Returns user object given user_id and/or name, hierarchical search 
    # starting with id and cascading to name if not found. Returns string
    # if user not found. 
    user_obj = User.objects.get(user_id=id).first()
    if user_obj is not None:
            result = user_obj
    else:
        user_obj = User.objects.get(name=user_name).first()
        if user_obj is not None:
            result = user_obj
        else:
            result = "User Not Found."
    return result

def delete_user_by_name(id: int, user_name: str):
    # Deletes user object given user_id and/or name, hierarchical search 
    # starting with id and cascading to name if not found. Returns string
    # if user not found. 
    user_obj = User.objects.get(user_id=id).first()
    if user_obj is not None:
        result = user_obj
    else:
        user_obj = User.objects.get(name=user_name).first()
        if user_obj is not None:
            result = user_obj
        else:
            result = "User Not Found."
    return result

def all_users():
    return User.objects.all()

def create_update_product(id: int, prod_name: str, prod_sku: str, prod_category: str, user: int, prod_quantity: int, prod_weight: float, prod_cost: float, prod_price: float):
    user_obj = User.objects.get(user_id=user).first()
    if user_obj is not None:
        product_obj, created = Product.objects.get_or_create(product_id=id,name=prod_name,sku=prod_sku,category=prod_category,user=user_obj,quantity=prod_quantity,weight=prod_weight,cost=prod_cost,price=prod_price).first()
        if created is False:
            product_obj.name = prod_name
            product_obj.sku = prod_sku
            product_obj.category = prod_category
            product_obj.user = user_obj
            product_obj.quantity = prod_quantity
            product_obj.weight = prod_weight
            product_obj.cost = prod_cost
            product_obj.cost = prod_price
            product_obj.save()
            result = "Product Updated."
        else:
            result = "Product Created."

    else:
        result = "User Not Found."
    return result

def get_product(name: str, sku: str, category: str, user: int, quantity_min: int, quantity_max: int, weight_min: float, weight_max: float, cost_min: float, cost_max: float, price_min: float, price_max: float) -> QuerySet:
    user_obj = User.objects.get(user_id=user).first()
    if user_obj is not None:
        products = Product.objects.get(user=user_obj)
        if name:
            products = Product.filter(name__icontains = name)
        if sku:
            products = Product.filter(sku__icontains = sku)
        if category:
            products = Product.filter(category__icontains = category)
        if quantity_min:
            products = Product.filter(quantity__gte = quantity_min)
        if quantity_max:
            products = Product.filter(quantity__lte = quantity_max)
        if weight_min:
            products = Product.filter(weight__gte = weight_min)
        if weight_max:
            products = Product.filter(weight__lte = weight_max)
        if cost_min:
            products = Product.filter(cost__gte = cost_min)
        if cost_max:
            products = Product.filter(cost__lte = cost_max)
        if price_min:
            products = Product.filter(price__gte = cost_min)
        if price_max:
            products = Product.filter(price__lte = cost_max)
    else:
        products = "User Not Found."
    return products

def delete_product(id: int, prod_name: str, prod_sku: str, prod_category: str, user: int, prod_quantity: int, prod_weight: float, prod_cost: float, prod_price: float) -> QuerySet:
    user_obj = User.objects.get(user_id=user).first()
    return_val = "User Not Found."
    if user_obj is not None:
        product = get_product(name=prod_name,sku=prod_sku,category=prod_category,user=user_obj,quantity=prod_quantity,weight=prod_weight,cost=prod_cost,price=prod_price).first()
        if product != "User Not Found." and product.exists():
            product.get.delete()
            return_val = Product.objects.all(user=user_obj)
 
    return return_val

def all_products(user: int):
    user_obj = User.objects.get(user_id=user).first()
    if user_obj is not None:
        return_val = Product.objects.all(user=user_obj)
    else:
        return_val = "User Not Found."
    return return_val 
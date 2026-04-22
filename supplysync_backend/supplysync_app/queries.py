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

def create_user(user_name: str, user_password: str):
    User.objects.all().values_list('user_id', flat=True)
    user_obj = User.objects.filter(name=user_name).first()
    if user_obj is None:
        User.objects.create(name=user_name,password=user_password)
        result = "User Created."
    else:
        result = "User Already Exists."
    return result

def update_user(user_name: str, new_name: str, new_password: str):
    result = "User Not Found."
    user_obj = User.objects.filter(name=user_name).first()
    if user_obj is not None:
        if new_name:
            user_obj2 = User.objects.filter(name=new_name).first()
            if user_obj2 is not None and user_obj != user_obj2:
                result = "Error Updating Username."
            else:
                user_obj.name = new_name
                result = "User Updated."
        if new_password:
            user_obj.password = new_password
            if result == "Error Updating Username." or result ==  "User Updated.":
                result += " Password Updated."
            else:
                result = "Password Updated."
            user_obj.password = new_password
        user_obj.save()

    return result

def get_user(user_name: str):
    
    user_obj = User.objects.filter(name=user_name).first()
    if user_obj is not None:
        result = user_obj
    else:
        result = "User Not Found."
    return result

def delete_user(user_name: str):
    # Deletes user object given user_id and/or name, hierarchical search 
    # starting with id and cascading to name if not found. Returns string
    # if user not found. 

    user_obj = User.objects.filter(name=user_name).first()
    if user_obj is not None:
        user_obj.delete()
    else:
        result = "User Not Found."
    return result

def all_users():
    return User.objects.all()

def create_update_product(prod_name: str, prod_sku: str, user_name: str, prod_category: str = None, prod_quantity: int = None, prod_weight: float = None, prod_cost: float = None, prod_price: float = None):
    user_obj = User.objects.filter(name=user_name).first()
    if user_obj is not None:
        # exists = Product.objects.filter(name=prod_name,sku=prod_sku,user=user_obj).first()
        name_exists = Product.objects.filter(name=prod_name,user=user_obj).first()
        sku_exists = Product.objects.filter(sku=prod_sku,user=user_obj).first()   
        # if name_exists is None and sku_exists is None and name_exists != sku_exists:
        if name_exists is None and sku_exists is None and name_exists != sku_exists:
            product_obj = Product.objects.create(name=prod_name,sku=prod_sku,user=user_obj)
            result = "Product Created."
        else:
            if name_exists is not None:
                product_obj = name_exists
            else:
                product_obj = sku_exists      
            result = "Product Updated."   
        product_obj.name = prod_name
        product_obj.sku = prod_sku
        product_obj.category = prod_category
        product_obj.quantity = prod_quantity
        product_obj.weight = prod_weight
        product_obj.cost = prod_cost
        product_obj.price = prod_price                
        product_obj.save()
    else:
        result = "User Not Found."
    return result

def get_product(name: str, sku: str, category: str, user_name: str, quantity_min: int, quantity_max: int, weight_min: float, weight_max: float, cost_min: float, cost_max: float, price_min: float, price_max: float) -> QuerySet:
    user_obj = User.objects.get(user_id=user_name).first()
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

def delete_product(id: int, prod_name: str, prod_sku: str, prod_category: str, user_name: str, prod_quantity: int, prod_weight: float, prod_cost: float, prod_price: float) -> QuerySet:
    user_obj = User.objects.filter(name=user_name).first()
    return_val = "User Not Found."
    if user_obj is not None:
        product = get_product(name=prod_name,sku=prod_sku,category=prod_category,user=user_obj,quantity=prod_quantity,weight=prod_weight,cost=prod_cost,price=prod_price).first()
        if product != "User Not Found." and product.exists():
            product.delete()
            return_val = Product.objects.all(user=user_obj)
 
    return return_val

def all_products(user_name: str):
    user_obj = User.objects.filter(name=user_name).first()
    if user_obj is not None:
        return_val = Product.objects.all(user=user_obj)
    else:
        return_val = "User Not Found."
    return return_val 
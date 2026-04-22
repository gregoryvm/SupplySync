from django.test import TestCase

from .models import (
    User,
    Product
)

from .queries import (
    create_user,
    update_user,
    get_user,
    all_users,
    create_update_product,

)
# Create your tests here.
class UserQueries(TestCase):

    def setUp(self):
        self.User1 = User.objects.create(name="User1",password="Password1")
        self.User2 = User.objects.create(name="User2",password="Password2")

    def test_create_user(self):
        
        result = create_user(user_name="Testing", user_password="1234")
        self.assertEqual(
            User.objects.filter(name="Testing", password="1234").exists(),
            True
        )
        self.assertEqual(
            result,
            "User Created."
        )
        self.assertEqual(len(User.objects.all()),3)
        
        result = create_user(user_name="Testing", user_password="1234")
        self.assertEqual(
            result,
            "User Already Exists."
        )
        self.assertEqual(len(User.objects.all()),3)
        
        result = create_user(user_name="Testing", user_password="12345")
        self.assertEqual(
            result,
            "User Already Exists."
        )
        self.assertEqual(len(User.objects.all()),3)

        result = create_user(user_name="Testing2", user_password="1234")
        self.assertEqual(
            User.objects.filter(name="Testing2", password="1234").exists(),
            True
        )
        self.assertEqual(
            result,
            "User Created."
        )
        self.assertEqual(len(User.objects.all()),4)

    def test_update_user(self):
        
        # Test All Update Cases for A Non-existant User
        result = update_user(user_name="Nonexistant", new_name="User3", new_password="Password3")
        self.assertEqual(
            result,
            "User Not Found."
        )
        result = update_user(user_name="Nonexistant", new_name=None, new_password="Password3")
        self.assertEqual(
            result,
            "User Not Found."
        )
        result = update_user(user_name="Nonexistant", new_name="User3", new_password=None)
        self.assertEqual(
            result,
            "User Not Found."
        )

        # Valid Cases ~~~ Find way to make pervious tests not affect future tests by changing values ~~~
        result = update_user(user_name="User1", new_name="User3", new_password="Password3")
        
        self.assertEqual(
            result,
            "User Updated. Password Updated."
        )

        result = update_user(user_name="User2", new_name="User4", new_password="Password3")
        self.assertEqual(
            result,
            "User Updated. Password Updated."
        )
        
        result = update_user(user_name="User4", new_name=None, new_password="Password3")
        self.assertEqual(
            result,
            "Password Updated."
        )

        result = update_user(user_name="User3", new_name="User7", new_password=None)
        self.assertEqual(
            result,
            "User Updated."
        )

        result = update_user(user_name="User4", new_name=None, new_password="Password3")
        self.assertEqual(
            result,
            "Password Updated."
        )

        result = update_user(user_name="User4", new_name=None, new_password="Password3")
        self.assertEqual(
            result,
            "Password Updated."
        )

        # Invalid Cases
        result = update_user(user_name="User4", new_name="User7", new_password=None)
        self.assertEqual(
            result,
            "Error Updating Username."
        )

        result = update_user(user_name="User4", new_name="User7", new_password="Password5")
        self.assertEqual(
            result,
            "Error Updating Username. Password Updated."
        )

    def test_get_user(self):
        result = get_user(user_name="User1")
        self.assertEqual(
            result,
            User.objects.get(name="User1")
        )

        result = get_user(user_name="DNE")
        self.assertEqual(
            result,
            "User Not Found."
        )
    
    def test_all_users(self):
        result = all_users()
        self.assertEqual(
            result[0],
            self.User1
        )

        self.assertEqual(
            result[1],
            self.User2
        )

        self.assertEqual(
            len(result),
            2
        )

#    product_id = models.AutoField(primary_key=True)
#    name = models.CharField(max_length=200)
#    sku = models.CharField(max_length=200)
#    category = models.CharField(max_length=200)
#    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
#    quantity = models.IntegerField()
#    weight = models.FloatField()
#    cost =  models.FloatField()
#    price =  models.FloatField()

class ProductQueries(TestCase):
    def setUp(self):
        self.User3 = User.objects.create(name="User3",password="Password3")
        self.User4 = User.objects.create(name="User4",password="Password4")
        self.Product1 = Product.objects.create(name="Product1",sku="4225-776-3234",category="category1",user=self.User3,quantity=50,weight=10.5,cost=7.99,price=11.99)
        self.Product2 = Product.objects.create(name="Product2",sku="JH433GTU",category="category2",user=self.User3,quantity=33,weight=24.4,cost=20.99,price=24.99)
        self.Product3 = Product.objects.create(name="Product3",sku="UI123QWO",category="category1",user=self.User4,quantity=4,weight=53.9,cost=54.99,price=74.99)

    # create_update_product(prod_name: str, prod_sku: str, prod_category: str, user_name: int, prod_quantity: int, prod_weight: float, prod_cost: float, prod_price: float):
    def test_create_update_product(self):

        # Test Cases where mandatory fields are updated (sku and name)
        result = create_update_product(prod_name="Product1",prod_sku="9442-009-2731",user_name="User3")
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product1").sku,
            "9442-009-2731"
        )

        result = create_update_product(prod_name="Product4",prod_sku="9442-009-2731",user_name="User3")
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(sku="9442-009-2731").name,
            "Product4"
        )
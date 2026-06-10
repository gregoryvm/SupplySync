from django.db import connections
from django.test import TestCase, Client
from django.urls import reverse
from .models import (
    User,
    Product
)
from django.contrib.auth.models import User as AuthUser

from .queries import (
    create_user,
    update_user,
    get_user,
    all_users,
    create_update_product,
    get_product,
    delete_product,
    all_products

)


# Create your tests here.
class UserQueries(TestCase):

    def setUp(self):
        self.User1 = User.objects.create(name="User1", password="Password1")
        self.User2 = User.objects.create(name="User2", password="Password2")

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
        self.assertEqual(len(User.objects.all()), 3)

        result = create_user(user_name="Testing", user_password="1234")
        self.assertEqual(
            result,
            "User Already Exists."
        )
        self.assertEqual(len(User.objects.all()), 3)

        result = create_user(user_name="Testing", user_password="12345")
        self.assertEqual(
            result,
            "User Already Exists."
        )
        self.assertEqual(len(User.objects.all()), 3)

        result = create_user(user_name="Testing2", user_password="1234")
        self.assertEqual(
            User.objects.filter(name="Testing2", password="1234").exists(),
            True
        )
        self.assertEqual(
            result,
            "User Created."
        )
        self.assertEqual(len(User.objects.all()), 4)

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
        self.User3 = User.objects.create(name="User3", password="Password3")
        self.User4 = User.objects.create(name="User4", password="Password4")
        self.User555 = None
        self.Product1 = Product.objects.create(
            name="Product1", sku="4225-776-3234", category="category1",
            user=self.User3, quantity=50, weight=10.5, cost=7.99, price=11.99)
        self.Product2 = Product.objects.create(
            name="Product2", sku="JH433GTU", category="category2",
            user=self.User3, quantity=33, weight=24.4, cost=20.99, price=24.99)
        self.Product3 = Product.objects.create(
            name="Product3", sku="UI123QWO", category="category1",
            user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

    def test_create_update_product(self):

        # Test Cases where mandatory fields are updated (sku and name)
        result = create_update_product(prod_name="Product1", prod_sku="9442-009-2731", user_name="User3")
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product1").sku,
            "9442-009-2731"
        )

        result = create_update_product(prod_name="Product4", prod_sku="9442-009-2731", user_name="User3")
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(sku="9442-009-2731").name,
            "Product4"
        )

        # Test Cases where non-mandatory fields are updated
        result = create_update_product(prod_name="Product4", prod_sku="9442-009-2731",
                                       user_name="User3", prod_category="category3")
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product4").category,
            "category3"
        )

        result = create_update_product(prod_name="Product4", prod_sku="9442-009-2731",
                                       user_name="User3", prod_quantity=100)
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product4").quantity,
            100
        )

        result = create_update_product(prod_name="Product4", prod_sku="9442-009-2731",
                                       user_name="User3", prod_weight=20.0)
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product4").weight,
            20.0
        )

        result = create_update_product(prod_name="Product4", prod_sku="9442-009-2731",
                                       user_name="User3", prod_cost=11.99)
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product4").cost,
            11.99
        )

        result = create_update_product(prod_name="Product4", prod_sku="9442-009-2731",
                                       user_name="User3", prod_price=13.99)
        self.assertEqual(
            result,
            "Product Updated."
        )
        self.assertEqual(
            Product.objects.get(name="Product4").price,
            13.99
        )

        # Test Cases where products are created
        result = create_update_product(prod_name="Product5", prod_sku="7524-554-9991", user_name="User4")
        self.assertEqual(
            result,
            "Product Created."
        )
        self.assertEqual(
            len(Product.objects.filter(user=self.User4)),
            2
        )

        # Invalid Test Cases where products are created missing mandatory fields
        try:
            result = create_update_product(prod_name="Product11", prod_sku="7842-314-9211")
        except Exception:
            result = "Unable to create product."
        self.assertEqual(
            result,
            "Unable to create product."
        )
        self.assertEqual(
            len(Product.objects.filter(name="Product5")),
            1
        )

        try:
            result = create_update_product(prod_name="Product11", user_name="User4")
        except Exception:
            result = "Unable to create product."
        self.assertEqual(
            result,
            "Unable to create product."
        )
        self.assertEqual(
            len(Product.objects.filter(name="Product5")),
            1
        )

        try:
            result = create_update_product(prod_name="Product11")
        except Exception:
            result = "Unable to create product."
        self.assertEqual(
            result,
            "Unable to create product."
        )
        self.assertEqual(
            len(Product.objects.filter(name="Product5")),
            1
        )
        try:
            result = create_update_product(prod_sku="7842-314-9211", user_name="User4")
        except Exception:
            result = "Unable to create product."
        self.assertEqual(
            result,
            "Unable to create product."
        )
        self.assertEqual(
            len(Product.objects.filter(name="Product5")),
            1
        )

        try:
            result = create_update_product(prod_sku="7842-314-9211")
        except Exception:
            result = "Unable to create product."
        self.assertEqual(
            result,
            "Unable to create product."
        )
        self.assertEqual(
            len(Product.objects.filter(name="Product5")),
            1
        )
        try:
            result = create_update_product(user_name="User4")
        except Exception:
            result = "Unable to create product."
        self.assertEqual(
            result,
            "Unable to create product."
        )
        self.assertEqual(
            len(Product.objects.filter(name="Product5")),
            1
        )

    def test_get_product(self):
        # Valid Test Cases with one search field
        result = get_product(name="Product2", user_name="User3")

        self.assertQuerySetEqual(
            result,
            Product.objects.filter(name=self.Product2.name, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(name=self.Product2.name, user=self.User3)),
            1
        )

        result = get_product(sku="JH433GTU", user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(sku=self.Product2.sku, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(sku=self.Product2.sku, user=self.User3)),
            1
        )

        result = get_product(category="category2", user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(category=self.Product2.category, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(category=self.Product2.category, user=self.User3)),
            1
        )

        result = get_product(quantity_min=33, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(quantity__gte=33, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(quantity__gte=33, user=self.User3)),
            2
        )

        result = get_product(quantity_max=50, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(quantity__lte=50, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(quantity__lte=50, user=self.User3)),
            2
        )

        result = get_product(weight_min=21, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(weight__gte=21, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(weight__gte=21, user=self.User3)),
            1
        )

        result = get_product(weight_max=25, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(weight__lte=25, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(weight__lte=25, user=self.User3)),
            2
        )

        result = get_product(cost_min=6.00, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(cost__gte=6.00, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(cost__gte=6.00, user=self.User3)),
            2
        )

        result = get_product(cost_max=20.00, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(cost__lte=20.00, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(cost__lte=20.00, user=self.User3)),
            1
        )

        result = get_product(price_min=15.00, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(price__gte=15.00, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(price__gte=15.00, user=self.User3)),
            1
        )

        result = get_product(price_max=27.99, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(price__lte=27.99, user=self.User3),
            ordered=False
        )
        self.assertEqual(
            len(Product.objects.filter(price__lte=27.99, user=self.User3)),
            2
        )

        # Valid Test Cases with multiple search fields
        result = get_product(category="category2", price_max=27.99, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(category=self.Product2.category, price__lte=27.99, user=self.User3)
        )
        self.assertEqual(
            len(Product.objects.filter(category=self.Product2.category, price__lte=27.99, user=self.User3)),
            1
        )

        result = get_product(category="category2", weight_min=10, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(category=self.Product2.category, weight__gte=10, user=self.User3)
        )
        self.assertEqual(
            len(Product.objects.filter(category=self.Product2.category, weight__gte=10, user=self.User3)),
            1
        )

        # Valid Test Cases where no results are returned
        result = get_product(price_max=1.99, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(price__lte=1.99, user=self.User3)
        )
        self.assertEqual(
            len(Product.objects.filter(price__lte=1.99, user=self.User3)),
            0
        )

        result = get_product(category="category40", price_min=15.00, user_name="User3")
        self.assertQuerySetEqual(
            result,
            Product.objects.filter(category="category40", price__gte=15.00, user=self.User3)
        )
        self.assertEqual(
            len(Product.objects.filter(category="category40", price__gte=15.00, user=self.User3)),
            0
        )

        # Invalid Test Cases where no user is found
        result = get_product(price_max=1.99, user_name="User555")
        self.assertEqual(
            result,
            "User Not Found."
        )
        self.assertEqual(
            len(Product.objects.filter(price__lte=1.99, user=self.User555)),
            0
        )

        result = get_product(category="category40", price_min=15.00, user_name="User555")
        self.assertEqual(
            result,
            "User Not Found."
        )
        self.assertEqual(
            len(Product.objects.filter(category="category40", price__gte=15.00, user=self.User555)),
            0
        )

    def test_delete_product(self):
        # Valid Test Cases
        result = delete_product(prod_name="Product3", user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3").first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        result = delete_product(prod_sku="UI123QWO", user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        result = delete_product(user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        result = delete_product(prod_quantity=4, user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        result = delete_product(prod_weight=53.9, user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)
        result = delete_product(prod_cost=54.99, user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        result = delete_product(prod_price=74.99, user_name=self.User4.name)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        result = delete_product(prod_name="Product3", prod_sku="UI123QWO", prod_category="category1",
                                user_name=self.User4.name, prod_quantity=4, prod_weight=53.9,
                                prod_cost=54.99, prod_price=74.99)
        self.assertEqual(
            len(result),
            0
        )
        self.assertEqual(
            Product.objects.filter(name="Product3", user=self.User4).first(),
            None
        )
        self.Product3 = Product.objects.create(name="Product3", sku="UI123QWO", category="category1",
                                               user=self.User4, quantity=4, weight=53.9, cost=54.99, price=74.99)

        # Invalid Test Cases
        result = delete_product(user_name="User666")
        self.assertEqual(
            result,
            "User Not Found."
        )

        result = delete_product(prod_name="Product200", user_name="User4")
        self.assertEqual(
            result,
            "Product Not Found."
        )

    def test_all_products(self):
        result = all_products(user_name="User3")
        self.assertEqual(
            len(result),
            2
        )

        result = all_products(user_name="User55")
        self.assertEqual(
            result,
            "User Not Found."
        )


class BaseTestCase(TestCase):
    def setUp(self):
        self.auth_user = AuthUser.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        create_user(
            user_name="testuser",
            user_password="testpass123"
        )

        self.client = Client()
        self.client.force_login(self.auth_user)
    
class HomeViewTests(BaseTestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("supplysync:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class SignupViewTests(TestCase):
    def test_signup_creates_user(self):
        response = self.client.post(reverse("supplysync:signup"), {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(AuthUser.objects.filter(username="newuser").exists())

    def test_signup_invalid_user_exists(self):
        response = self.client.post(reverse("supplysync:signup"), {
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(AuthUser.objects.filter(username="testuser", password="StrongPass123!").exists())
    
    def test_signup_invalid_user_password_len(self):
        response = self.client.post(reverse("supplysync:signup"), {
            "username": "newuser2",
            "password1": "4444",
            "password2": "4444"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(AuthUser.objects.filter(username="newuser2", password="4444").exists())
    
    def test_signup_invalid_user_password_match(self):
        response = self.client.post(reverse("supplysync:signup"), {
            "username": "newuser4",
            "password1": "StrongPass123!",
            "password2": "StrongPass1234!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(AuthUser.objects.filter(username="newuser3").exists())

    def test_signup_invalid_user_username(self):
        response = self.client.post(reverse("supplysync:signup"), {
            "username": "!!!!!!!!!!!!!!!!!!!!!!!",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(AuthUser.objects.filter(username="!!!!!!!!!!!!!!!!!!!!!!!", password="StrongPass123!").exists())

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_user(
            username="loginuser",
            password="testpass123"
        )

    def test_login_success(self):
        response = self.client.post(reverse("supplysync:login"), {
            "username": "loginuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, 302)

class LogoutViewTests(BaseTestCase):
    def test_logout_redirects(self):
        response = self.client.post(reverse("supplysync:logout"))
        self.assertEqual(response.status_code, 302)

class AccountViewTests(BaseTestCase):
    def test_account_username_change(self):
        response = self.client.post(reverse("supplysync:account"), {
            "newname": "updateduser"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(AuthUser.objects.filter(username="updateduser").exists())

    def test_invalid_username_rejected(self):
        response = self.client.post(reverse("supplysync:account"), {
            "newname": "invalid!!!"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(AuthUser.objects.filter(username="invalid!!!").exists())

    def test_account_password_change(self):
        response = self.client.post(reverse("supplysync:account"), {
            "newpassword": "StrongPass12345!"
        })

        self.assertEqual(response.status_code, 302)
        user = AuthUser.objects.get(pk=self.auth_user.pk)
        self.assertTrue(user.check_password("StrongPass12345!"))

    def test_invalid_password_rejected(self):
        response = self.client.post(reverse("supplysync:account"), {
            "newpassword": "4444"
        })

        self.assertEqual(response.status_code, 302)
        user = AuthUser.objects.get(pk=self.auth_user.pk)
        self.assertFalse(user.check_password("4444"))
class CreateProductViewTests(BaseTestCase):
    def test_valid_product_creation(self):
        response = self.client.post(reverse("supplysync:create-product"), {
            "product_name": "Widget",
            "product_sku": "SKU123",
            "product_category": "Tools",
            "product_quantity": "10",
            "product_weight": "1.5",
            "product_cost": "5",
            "product_price": "10"
        })

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertTrue(Product.objects.filter(user=user_obj, name="Widget").exists())
    
    def test_invalid_product_name(self):
        response = self.client.post(reverse("supplysync:create-product"), {
            "product_name": "!!!",
            "product_sku": "SKU123",
            "product_category": "Tools",
            "product_quantity": "10",
            "product_weight": "1.5",
            "product_cost": "5",
            "product_price": "10"
        })

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertFalse(Product.objects.filter(user=user_obj, name="!!!").exists())

    def test_invalid_product_quantity(self):
        response = self.client.post(reverse("supplysync:create-product"), {
            "product_name": "Widget2",
            "product_sku": "SKU123",
            "product_category": "Tools",
            "product_quantity": "test",
            "product_weight": "1.5",
            "product_cost": "5",
            "product_price": "10"
        })

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertFalse(Product.objects.filter(user=user_obj, name="Widget2").exists())
class InventoryViewTests(BaseTestCase):
    def test_inventory_get(self):
        response = self.client.get(reverse("supplysync:products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory.html")
        
class EditProductViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()

        create_update_product(
            prod_name="Item",
            prod_sku="SKU1",
            prod_category="Cat",
            user_name="testuser",
            prod_quantity=1,
            prod_weight=1,
            prod_cost=1,
            prod_price=2
        )

    def test_edit_product_valid(self):
        response = self.client.post(
            reverse("supplysync:edit", args=["Item", "SKU1"]),
            {
                "product_name": "Item2",
                "product_sku": "SKU1",
                "product_category": "Cat",
                "product_quantity": "2",
                "product_weight": "2",
                "product_cost": "2",
                "product_price": "4"
            }
        )

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertTrue(Product.objects.filter(user=user_obj, name="Item2").exists())
    
    def test_edit_invalid_product_name(self):
        response = self.client.post(
            reverse("supplysync:edit", args=["Item", "SKU1"]),
            {
                "product_name": "!!!!",
                "product_sku": "SKU1",
                "product_category": "Cat",
                "product_quantity": "2",
                "product_weight": "2",
                "product_cost": "2",
                "product_price": "4"
            }
        )

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertFalse(Product.objects.filter(user=user_obj, name="!!!!").exists())
        
    def test_edit_invalid_product_weight(self):
        response = self.client.post(
            reverse("supplysync:edit", args=["Item", "SKU1"]),
            {
                "product_name": "Item2",
                "product_sku": "SKU1",
                "product_category": "Cat",
                "product_quantity": "2",
                "product_weight": "test",
                "product_cost": "2",
                "product_price": "4"
            }
        )

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertFalse(Product.objects.filter(user=user_obj, name="Item2").exists())

class DeleteProductViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()

        create_update_product(
            prod_name="Item",
            prod_sku="SKU1",
            prod_category="Cat",
            user_name="testuser",
            prod_quantity=1,
            prod_weight=1,
            prod_cost=1,
            prod_price=2
        )

    def test_delete_product(self):
        response = self.client.post(
            reverse("supplysync:delete", args=["Item", "SKU1"])
        )

        self.assertEqual(response.status_code, 302)
        user_obj = User.objects.filter(name="testuser").first()
        self.assertFalse(Product.objects.filter(user=user_obj, name="Item").exists())
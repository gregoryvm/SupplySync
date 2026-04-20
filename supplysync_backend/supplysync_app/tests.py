from django.test import TestCase

from .models import (
    User,
    Product
)

from .queries import (
    create_user,
    update_user,
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

    

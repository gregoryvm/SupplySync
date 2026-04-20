from django.test import TestCase

from .models import (
    User,
    Product
)

from .queries import (
    create_update_user,
)
# Create your tests here.
class UserQueries(TestCase):
    user = None

    def test_create_update_user(self):
        result = create_update_user(user_name="Testing", user_password="1234")
        self.assertEqual(
            User.objects.filter(name="Testing", password="1234").exists(),
            True
        )
        self.assertEqual(
            result,
            "User Created."
        )
        self.assertEqual(len(User.objects.all()),1)

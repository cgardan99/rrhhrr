from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseTestCase(TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "password"
        user = User.objects.create(
            username=self.username,
            email="a@a.com"
        )
        user.set_password(self.password)
        user.save()
        self.user = user


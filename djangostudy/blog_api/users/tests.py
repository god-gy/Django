from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", password="testpass", bio="Test bio"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass"))
        self.assertEqual(user.bio, "Test bio")

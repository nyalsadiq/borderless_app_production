from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTests(TestCase):

    def test_profile_created(self):
        user = User.objects.create_user(
            username="koalabear",
            email="koalabear@example.com",
            password="secret")

        self.assertEqual(User.objects.get(username="koalabear").email,
                         "koalabear@example.com")

        user.profile.location = "Edinburgh"
        user.save()

        self.assertEqual(Profile.objects.get(pk=user.id).location, "Edinburgh")

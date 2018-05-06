from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.test import Client
from django.urls import reverse


class ProfileModelTests(TestCase):

    def test_profile_created(self):
        """
            Creates a user, makes sure the user is stored in DB with correct
            attributes
        """
        user = User.objects.create_user(
            username="koalabear",
            email="koalabear@example.com",
            password="secret")

        self.assertEqual(User.objects.get(username="koalabear").email,
                         "koalabear@example.com")

        user.profile.location = "Edinburgh"
        user.save()

        self.assertEqual(Profile.objects.get(pk=user.id).location, "Edinburgh")


class ProfileModel_HTTPTests(TestCase):

    def test_no_profiles(self):
        """
            Tests that user_list is empty if no users in DB
        """
        c = Client()
        response = c.get(reverse('profiles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),0)

    def test_one_profile(self):
        """
            Makes one user and tests that the index view gets the user
        """
        User.objects.create_user(
            username="koalabear",
            email="koalabear@example.com",
            password="secret")

        c = Client()
        response = c.get(reverse('profiles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_more_profiles(self):
        """
            Makes ten users and tests that the index view gets 10 users
        """

        for x in range(0, 10):
            User.objects.create_user(
                username="".join(("koalabear", str(x))),
                email="".join(("koalabear@example.com", str(x))),
                password="".join(("secret", str(x)))
                )

        c = Client()
        response = c.get(reverse('profiles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

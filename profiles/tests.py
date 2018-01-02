from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.test import Client
from django.urls import reverse


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


class ProfileModel_HTTPTests(TestCase):

    def test_no_profiles(self):
        c = Client()
        response = c.get(reverse('profiles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['user_list'], [])

    def test_one_profile(self):
        User.objects.create_user(
            username="koalabear",
            email="koalabear@example.com",
            password="secret")

        c = Client()
        response = c.get(reverse('profiles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 1)
        self.assertEqual(response.context['user_list'][0].username, "koalabear")

import json
import base64
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Dummy password
PASSWORD = "password@12345"


def create_user(username="user@example.com", password=PASSWORD):
    """
    Create user function with dummy username and password
    :param username:
    :param password:
    :return:
    """
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        last_name="User",
        first_name="Test"
    )


class AuthenticationTest(APITestCase):
    """
    Test user authentication
    """

    def test_user_sign_up(self):
        """
        user signup test case
        :return:
        """
        response = self.client.post(reverse("sign_up"), data={
            'username': "amber@nickelfox.com",
            "first_name": "Amber",
            "last_name": "Mike",
            "password1": PASSWORD,
            "password2": PASSWORD
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['username'], user.username)

    def test_user_login(self):
        """
        User login test case
        :return:
        """
        user = create_user()
        response = self.client.post(reverse("login"), data={
            "username": user.username,
            "password": PASSWORD
        })

        # Parse payload data from access token
        access = response.data['access']
        header, payload, signature = access.split('.')
        decode_payload = base64.b64decode(f'{payload}==')
        payload_data = json.loads(decode_payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data['refresh'])
        self.assertEqual(payload_data['id'], user.id)

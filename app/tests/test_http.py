from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Dummy password
PASSWORD = "password@12345"


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

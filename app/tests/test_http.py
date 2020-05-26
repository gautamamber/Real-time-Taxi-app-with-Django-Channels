import json
import base64
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from app import models

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


class TripTest(APITestCase):
    """
    Test case for Trips
    """

    def setUp(self):
        """
        Setup the database
        :return:
        """
        user = create_user()
        response = self.client.post(reverse('login'), data={
            "username": user.username,
            "password": PASSWORD
        })
        self.access = response.data['access']

    def test_user_can_list_trips(self):
        """
        User can see his all trips
        :param self:
        :return:
        """
        trips = [
            models.Trip.objects.create(pick_up_address='A', drop_off_address='B'),
            models.Trip.objects.create(pick_up_address='B', drop_off_address='C')
        ]
        response = self.client.get(reverse('trip_list'),
                                   HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_trip = [str(trip.id) for trip in trips]
        act_trip = [trip.get('id') for trip in response.data]
        self.assertCountEqual(exp_trip, act_trip)

    def test_user_can_retrieve_trip(self):
        """
        Get trip using uuid
        :return:
        """
        trip = models.Trip.objects.create(pick_up_address='A', drop_off_address='B')
        response = self.client.get(trip.get_absolute_url(),
                                   HTTP_AUTHORIZATION=f'Bearer {self.access}'
                                   )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(trip.id), response.data.get('id'))

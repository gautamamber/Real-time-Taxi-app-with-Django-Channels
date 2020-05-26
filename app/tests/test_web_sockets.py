from channels.testing import WebsocketCommunicator
import pytest
from channels.layers import get_channel_layer
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from taxiapp.routing import application


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


@database_sync_to_async
def create_user(username, password, group="rider"):
    """
    Create dummy username password
    helper function creates a new user in the database and then generates an access token for it.
    :param group:
    :param username:
    :param password:
    :return:
    """
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    user_group, _ = Group.objects.get_or_create(name=group)  # new
    user.groups.add(user_group)
    user.save()
    access = AccessToken.for_user(user)
    return user, access


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    """
    Test web sockets
    We’re also using coroutines that were introduced with the asyncio module
    Django Channels mandates the use of both pytest and asyncio
    """

    async def test_can_connect_to_server(self, settings):
        """
        Connect of test server
        WebSocket test proves that a client can connect to the server.
        :param settings:
        :return:
        """
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(  # new
            'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'  # changed
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_join_driver_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'password123', 'driver'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('drivers', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_request_trip(self, settings):
        """
        Test case for trip
        When a rider requests a trip, the server will create a new Trip record and will broadcast the request to the
        driver pool. But from the rider’s perspective, he will only get a message back confirming the creation of a new
        trip. That’s what this test does.
        :param settings:
        :return:
        """
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            'test.user@example.com', 'password123', 'rider'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        await communicator.send_json_to({
            'type': 'create.trip',
            'data': {
                'pick_up_address': '123 Main Street',
                'drop_off_address': '456 Piney Road',
                'rider': user.id,
            },
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')
        assert response_data['id'] is not None
        assert response_data['pick_up_address'] == '123 Main Street'
        assert response_data['drop_off_address'] == '456 Piney Road'
        assert response_data['status'] == 'REQUESTED'
        assert response_data['rider']['username'] == user.username
        assert response_data['driver'] is None
        await communicator.disconnect()

    async def test_driver_alert_on_request(self, settings):
        """
        A ride request should be broadcast to all drivers in the driver pool the moment it is sent. Let’s create a
        test to capture that behavior.
        We start off by creating a channel layer and adding it to the driver pool. Every message that is broadcast to
        the drivers group will be captured on the test_channel . Next, we establish a connection to the server as a
        rider, and we send a new request message over the wire. Finally, we wait for the broadcast message to reach the
        drivers group, and we confirm the identity of the rider who sent it.
        :param settings:
        :return:
        """
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        channel_layer = get_channel_layer()
        await channel_layer.group_add(
            group="drivers",
            channel="test_channel"
        )

        user, access = await create_user(
            "test.user@example.com", "password", "rider"
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()

        # Request a trip

        await communicator.send_json_to({
            'type': 'create.trip',
            'data': {
                'pick_up_address': '123 Main Street',
                'drop_off_address': '456 Piney Road',
                'rider': user.id,
            },
        })
        # Receive JSON message from server on test channel.
        response = await channel_layer.receive('test_channel')
        response_data = response.get("data")
        assert response_data['id'] is not None
        assert response_data['rider']['username'] == user.username
        assert response_data['driver'] is None

        await communicator.disconnect()

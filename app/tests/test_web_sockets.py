from channels.testing import WebsocketCommunicator
import pytest
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
def create_user(username, password):
    """
    Create dummy username password
    helper function creates a new user in the database and then generates an access token for it.
    :param username:
    :param password:
    :return:
    """
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
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

    async def test_can_send_receive_message(self, settings):
        """
        Test case for send and receive message
        In this test, after we establish a connection with the server,
        we send a message and wait to get one back. We expect the server
        to echo our message right back to us exactly the way we sent it. In fact,
        we need to program this behavior on the server.
        :return:
        """
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        """
        Unfortunately, the JavaScript WebSocket API does not support custom headers. That means we need to find a
        different way to authenticate our WebSocket connection than an authorization header.
        :param settings:
        :return:
        """
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is False

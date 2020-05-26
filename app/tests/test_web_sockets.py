from channels.testing import WebsocketCommunicator
import pytest
from taxiapp.routing import application


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


@pytest.mark.asyncio
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
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

from channels.generic.websocket import AsyncWebsocketConsumer


class TaxiConsumer(AsyncWebsocketConsumer):
    """
    Taxi consumer
    A Channels consumer is like a Django view with extra steps to support the WebSocket protocol. Whereas a Django view
    can only process an incoming request, a Channels consumer can send and receive messages to the WebSocket
    connection being opened and closed.
    """

    async def connect(self):
        """
        connect with web socket
        :return:
        """
        await self.accept()

    async def disconnect(self, code):
        """
        disconnect with web socket
        :param code:
        :return:
        """
        await super().disconnect(code)

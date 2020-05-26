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
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                group='test',
                channel=self.channel_name
            )
            await self.accept()

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def disconnect(self, code):
        """
        disconnect with web socket
        :param code:
        :return:
        """
        await self.channel_layer.group_discard(
            group='test',
            channel=self.channel_name
        )
        await super().disconnect(code)

    async def receive_json(self, content, **kwargs):
        """
        The receive_json() function is responsible for processing all messages that come to the server. Our message is
        an object with a type and a data payload.
        Passing a type is a Channels convention that serves two purposes. First, it helps differentiate incoming
        messages and tells the server how to process them. Second, the type maps directly to a consumer function when
        sent from another channel layer.
        :param content:
        :param kwargs:
        :return:
        """
        message_type = content.get("type")
        if message_type == "echo.message":
            await self.send_json({
                "type": message_type,
                "data": content.get("data")
            })

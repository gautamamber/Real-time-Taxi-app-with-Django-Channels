from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app import consumers


application = ProtocolTypeRouter(
    {
        # Channels implicitly handles the HTTP URL configuration, we need to explicitly handle WebSocket routing.
        # (A router is the Channels counterpart to Django’s URL configuration.)
        # the app initializes an HTTP router by default if one isn’t explicitly specified.
        # If an http argument is not provided, it will default to the Django view system’s
        # ASGI interface, channels.http.AsgiHandler , which means that for most projects
        # that aren’t doing custom long-poll HTTP handling, you can simply not specify an
        # http option and leave it to work the “normal” Django way.
        "websocket": URLRouter([
            path('taxi/', consumers.TaxiConsumer),
        ])
    }
)

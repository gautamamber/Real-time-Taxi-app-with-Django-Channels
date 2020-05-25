from channels.routing import ProtocolTypeRouter


application = ProtocolTypeRouter(
    {
        # the app initializes an HTTP router by default if one isn’t explicitly specified.
        # If an http argument is not provided, it will default to the Django view system’s
        # ASGI interface, channels.http.AsgiHandler , which means that for most projects
        # that aren’t doing custom long-poll HTTP handling, you can simply not specify an
        # http option and leave it to work the “normal” Django way.
    }
)

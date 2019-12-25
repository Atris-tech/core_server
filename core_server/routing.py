from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from web_socket.consumers import AtrisConsumer
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter([
        re_path('ws/', AtrisConsumer),
    ])
})

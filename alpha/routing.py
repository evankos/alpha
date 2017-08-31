from channels.routing import route
from alpha.consumers import ws_connect, ws_disconnect, message_handler

channel_routing = [
    route("websocket.receive", message_handler),
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]
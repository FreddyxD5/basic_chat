from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/chatapp/(?P<room_name>\w+)/$', consumers.ChatAppConsumer.as_asgi()),    
]
from django.urls import path
from .consumers import MiConsumer

websocket_urlpatterns = [
    path('ws/vara/', MiConsumer.as_asgi()),
]

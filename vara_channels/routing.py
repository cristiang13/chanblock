from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import MiConsumer

websocket_urlpatterns = [
    path('ws/vara/', MiConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})

"""
Este script configura las rutas de WebSocket para una aplicación Django usando Channels.

Se definen las rutas de WebSocket mediante la variable `websocket_urlpatterns`, que incluye
una ruta específica ('ws/vara/') vinculada al consumidor `MiConsumer`. Esta configuración permite
que las conexiones WebSocket entrantes en la ruta especificada sean manejadas por `MiConsumer`.

La variable `application` es una instancia de `ProtocolTypeRouter`, la cual es configurada para
utilizar `URLRouter` con las `websocket_urlpatterns` definidas. Esto establece cómo la aplicación
debe manejar las conexiones WebSocket en función de las rutas definidas.

Esta configuración es crucial para el manejo asincrónico de WebSockets en aplicaciones Django
que utilizan Channels, permitiendo la comunicación en tiempo real entre el servidor y los clientes.

Uso:
- Se debe incluir este script en el enrutamiento de la aplicación Django para activar el manejo
  de conexiones WebSocket según las rutas definidas.
- `MiConsumer` debe estar definido y ser capaz de manejar eventos como conectar, desconectar,
  y recibir mensajes a través del WebSocket.
"""
import os
import django
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chanblockweb.settings.local')
django.setup()



class MiConsumer(AsyncWebsocketConsumer):
    """
    Un consumidor de WebSocket asíncrono para gestionar conexiones, desconexiones,
    recepción y envío de mensajes en tiempo real.

    Esta clase extiende de AsyncWebsocketConsumer y proporciona una implementación específica
    para manejar eventos de conexión, desconexión, y recepción de mensajes a través de WebSockets.
    Mantiene un registro de los últimos tres bloques de datos recibidos y proporciona una forma de
    actualizar y enviar estos bloques a los clientes conectados.

    Attributes:
        last_three_blocks (list): Almacena los últimos tres bloques de datos recibidos.

    Methods:
        connect: Gestiona las acciones a realizar al establecer una conexión WebSocket.
        disconnect: Define las acciones a realizar cuando una conexión WebSocket se cierra.
        update_last_three_blocks: Actualiza la lista de los últimos tres bloques con nuevos datos.
        receive: Procesa los datos recibidos por WebSocket y actualiza los últimos tres bloques.
        send_message: Envía un mensaje a través del WebSocket al cliente conectado.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_three_blocks = []

    async def connect(self):
        """Maneja el evento de conexión WebSocket, aceptándola e informando al cliente."""
        print("Conectado")
        await self.accept()
        await self.send_message({"message": "Conexión WebSocket establecida."})

    async def disconnect(self, close_code):
        """Maneja el evento de desconexión WebSocket."""
        print("desconectado")

    def update_last_three_blocks(self, block_data):
        """
        Actualiza la lista de los últimos tres bloques de datos.

        Args:
            block_data: El nuevo bloque de datos a agregar a la lista.
        """
        self.last_three_blocks.append(block_data)
        if len(self.last_three_blocks) > 3:
            self.last_three_blocks.pop(0)
        


    async def receive(self, text_data):
        """
        Maneja los datos recibidos a través del WebSocket.

        Args:
            text_data: Datos en formato de texto recibidos por el WebSocket.
        """
        text_data_json = json.loads(text_data)
        
        # Procesar y actualizar los últimos tres bloques
        self.update_last_three_blocks(text_data_json)
        cache.set('last_three_blocks', self.last_three_blocks, timeout=60*2)
        await self.send_message({"message": self.last_three_blocks})
   

    async def send_message(self, message):
        """
        Envía un mensaje a través del WebSocket al cliente.

        Args:
            message: El mensaje a enviar.
        """
        text_data1=json.dumps(message)
        try:
            await self.send(text_data=text_data1)
            print("Mensaje enviado")
        except Exception as e:
            # Manejo de excepción en caso de un error al enviar el mensaje
            print(f"Error al enviar el mensaje: {e}")
    

        


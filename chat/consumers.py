from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Logica di connessione al canale WebSocket
        pass

    async def disconnect(self, close_code):
        # Logica di disconnessione dal canale WebSocket
        pass

    async def receive(self, text_data):
        # Logica di ricezione dei messaggi dal canale WebSocket
        pass

    async def send_message(self, message):
        # Logica di invio dei messaggi al canale WebSocket
        pass

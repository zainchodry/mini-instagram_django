import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if user is None or isinstance(user, AnonymousUser) or not user.is_authenticated:
            # reject the connection for non-authenticated users
            await self.close()
            return

        self.user = user
        self.group_name = f'notifications_{self.user.pk}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # receive message from group
    async def notify(self, event):
        """
        event expected to contain: {
            'type': 'notify',
            'payload': { ... JSON-serializable payload ... }
        }
        """
        payload = event.get('payload', {})
        await self.send(text_data=json.dumps(payload))

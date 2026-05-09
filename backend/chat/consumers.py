import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = f'chat_{self.room_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        allowed = await self.is_room_member()
        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', 'text')
        content = data.get('content', '').strip()

        if not content:
            return

        msg = await self.save_message(msg_type, content)

        await self.channel_layer.group_send(
            self.room_group,
            {
                'type': 'chat_message',
                'id': str(msg.id),
                'sender_id': str(self.user.id),
                'sender_nickname': self.user.nickname,
                'msg_type': msg_type,
                'content': content,
                'created_at': msg.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_room_member(self):
        from .models import ChatRoom
        try:
            room = ChatRoom.objects.select_related('match__user_a', 'match__user_b').get(id=self.room_id)
            return self.user in (room.match.user_a, room.match.user_b)
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, msg_type, content):
        from .models import ChatRoom, Message
        room = ChatRoom.objects.get(id=self.room_id)
        msg = Message.objects.create(
            chat_room=room,
            sender=self.user,
            msg_type=msg_type,
            content=content,
        )
        room.last_message_at = timezone.now()
        room.save(update_fields=['last_message_at'])
        return msg

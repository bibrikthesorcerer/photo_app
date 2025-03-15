import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils.timezone import now

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            'server-wide-shout',
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            f'user_{self.user.id}',
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        if self.user.role == self.user.ROLE_USER:
            return
        data = json.loads(text_data)
        message = data.get('message')
        group = data.get('group')
        async_to_sync(self.channel_layer.group_send)(
            group,
            {
                'type': 'send_notification',
                'message': message
            }
        )
    
    def send_notification(self, event):
        self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event.get('message'),
            'timestamp': now().strftime("%H:%M:%S")
        }))

    def notify_like(self, event):
        self.send(text_data=json.dumps({
            'type': 'notify_like',
            'message': event.get('message'),
            'timestamp': now().strftime("%H:%M:%S"),
            'likes_count': event.get('likes_count'),
            'photo_id': event.get('photo_id')
        }))

    def notify_comment(self, event):
        self.send(text_data=json.dumps({
            'type': 'notify_comment',
            'message': event.get('message'),
            'timestamp': now().strftime("%H:%M:%S"),
            'comments_count': event.get('comments_count'),
            'photo_id': event.get('photo_id')
        }))

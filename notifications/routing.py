from django.urls import path
from . import consumers

url_patterns = [
    path('notify/', consumers.NotificationConsumer.as_asgi())
]
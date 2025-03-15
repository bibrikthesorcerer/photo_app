from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_message_to_list_of_users(user_ids: list, msg_type:str, message: str, **kwargs):
    '''Send message to a number of users via individual channel'''
    channel_layer = get_channel_layer()
    for id in user_ids:
        async_to_sync(channel_layer.group_send)(
            f'user_{id}',
            {
                'type': msg_type,
                'message': message,
                **kwargs
            }
        )
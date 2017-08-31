from channels import Group
from .authentication import rest_auth
import json

@rest_auth
def ws_connect(message):
    Group('posts').add(message.reply_channel)
    Group('posts').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })

@rest_auth
def ws_disconnect(message):
    Group('posts').discard(message.reply_channel)

@rest_auth
def message_handler(message):
    print(message['text'])
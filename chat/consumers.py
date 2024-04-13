import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.contrib.auth import get_user_model

from .models import Message
from .helpers import message_to_json, messages_to_json

User = get_user_model()



class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print("fetch_messages function")

        messages = Message.last_10_message()
        content = {"messages": messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        print("new_message function")

        author = self.scope["user"].username
        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            author=author_user, content=data['message'])
        
        content = {
            'command': 'new_message',
            'message': message_to_json(message)
        }

        return self.send_chat_message(content)

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
        }

    def connect(self):
        print("connect function")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # accepts websocket connection
        # if you don't call accept() the connection will be rejected
        # maybe you want to reject for authoriazation reasons
        self.accept()

    def disconnect(self, close_code):
        print("disconnect function")

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("receive function")

        data = json.loads(text_data)
        print(data)
        self.commands[data["command"]](self, data)
    
    # send message to chat
    def send_chat_message(self, message):
        print("send_chat_message function")

        # Send message to room group (Sends an event to a group)
        async_to_sync(self.channel_layer.group_send)(
            # chat.message calls the chat_message method
            self.room_group_name, {
                "type": "chat.message",
                "message": message
                }
            )
    
    # send messages to chat romm (display message there)
    def send_message(self, message):
        print("send_message function")

        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        print("chat_message function")

        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

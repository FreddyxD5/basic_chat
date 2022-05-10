import json
from random import randint
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # await if self.scope["user"].is_anonymous:
        #     self.close()  
        self.user = self.scope['user']
        print(self.user)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # a = randint(1,555)
        # self.channel_name = f'user-{a}'
        print('ROOM GROUP NAME')
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,                
            }
        )
    

    async def chat_message(self,event):
        message = event['message']
        #send a message to web socket
        await self.send(text_data=json.dumps({
            'message':message,
            'name':self.channel_name
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('se ha desconectado del chat')


#Sync To sync
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         #Join the room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )        
#         self.accept()        

#     #Receive a message from WebSocket
#     def receive(self, text_data):        
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']        


#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type':'chat_message',
#                 'message':message
#             }
#         )

#     def chat_message(self, event):
#         message = event['message']
#         #Send a message to WebSocket

#         self.send(text_data=json.dumps({
#             'message':message
#         }))
    
#     def disconnect(self, close_code):
#         #Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )



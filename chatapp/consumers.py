import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


from .models import Room,Message

class ChatAppConsumer(WebsocketConsumer):

    def __init__(self,*args,**kwargs):
        super().__init__(args,kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

        self.user_inbox = None

    
    def connect(self):        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chatapp_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'
        #Conexion aceptada    
        self.accept()
        
        #Ingresar a un grupo
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )        
        #Enviar la lista de usuarios de los nuevos usuarios que entran
        self.send(json.dumps({
            'type':'user_list',
            'users':[user.username for user in self.room.online.all()]
        }))
        
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'user_join',
                    'user':self.user.username
                }
            )
            #Crea un inbos al usuario para mensajes privados
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )

            self.room.online.add(self.user)


    
    def disconnect(self, close_code):        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name        
        )

        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'user_leave',
                    'user':self.user.username
                }
            )

            #Borramos el inbox una vez que se haya desconectado
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name
            )
            self.room.online.remove(self.user)

    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        #Enviar el chat como evento a la sala
        user = 'AnonymousUser'
        if self.user.is_authenticated:
            user = self.user.username
        
        if message.startswith('/pm'):
            split = message.split(' ',2)
            target = split[1]
            target_msg = split[2]

            #Enviar un mensaje privado
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{target}',
                {
                    'type':'private_message',
                    'user':self.user.username,
                    'message':target_msg
                }
            )
            
            self.send(json.dumps({
                'type':'private_message_delivered',
                'target':target,
                'message':target_msg
            }))

            return 

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'user':user,
                'message':message
            }
        )
        if self.user.is_authenticated:
            Message.objects.create(user=self.user, room=self.room, content=message)


    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))
    
    def user_leave(self,event):
        self.send(text_data=json.dumps(event))

    def user_list(self,event):        
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))




import socketio
from sqlalchemy.orm import Session
from fastapi import Depends, status ,HTTPException
from . import database, models


sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)
connected_users = set()  # Set to store connected users

@sio_server.event
async def connect(sid, environ, auth=None): 
    if auth:
        userId = auth.get('userId'), 
        print(f'{sid}: connected as {userId}')
    else:
        print(f'{sid}: connected')
    # print(f'{sid}: connected as {userId}')
    connected_users.add(sid)  # Add connected user to the set
    await sio_server.emit('join', {'sid': sid, 'userId': userId})
    await sio_server.emit('connected_users', list(connected_users)) 

@sio_server.event
async def chat(sid, data):
    message = data['message']
    clientId = data['clientId']
    userId = data['userId']
    print(f'Received message from {userId} (client ID: {clientId}): {message}')
    await sio_server.emit('chat', {'sid': sid, 'message': message})

@sio_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected')
    connected_users.remove(sid)  # Remove disconnected user from the set
    await sio_server.emit('connected_users', list(connected_users))  # Emit the updated list of connected users to the client
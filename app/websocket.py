from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from app.mongo_connection import save_message, get_all_messages
socketio = SocketIO()


# When a client connects
@socketio.on("connect")
def handle_connect():
    print("Client connected !")


# When a client disconnects
@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected !")



@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room_id = data['room_id']
    
    print(f"Username: {username} has joined room: {room_id}")
    
    # Faire rejoindre le client à la room
    join_room(room_id)
    
    # Envoyer l'annonce seulement aux clients de cette room
    socketio.emit('join_room_announcement', {
        'username': username,
        'room_id': room_id
    }, room=room_id)
@socketio.on("leave_room")
def handle_leave_room(data):
    username = data['username']
    room_id = data['room_id']
    leave_room(room_id)
    print(f"{data.username} has left the room {data.room_id}")
    socketio.emit('leave_room_announcement',  {
        'username': username,
        'room_id': room_id
    }, room=room_id)

@socketio.on("send_message")
def handle_send_message(data):
    username = data['username']
    room_id = data['room_id']
    message = data['message']
    if message:
        print(message)
        save_message(room_id, message, username)

    print(f"[{room_id}] {username}: {message}")

    # Send message only to users in the same room
    socketio.emit("receive_message", {
        "username": username, 
        "message": message,
        "room_id": room_id
    }, room=room_id)   
    return message

@socketio.on("load_all_messages")
def handle_load_all_messages(data):
    room_id = data['room_id']
    
    # Get all messages for the room
    messages = get_all_messages(room_id)
    
    print(f"Loading all {len(messages)} messages for room: {room_id}")
    
    # Send messages only to the requesting user
    socketio.emit("all_messages_loaded", {
        "room_id": room_id,
        "messages": messages
    })



from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.mongo_connection import save_room, get_room, is_room_member, get_room_members, save_message, get_messages, is_room_admin, add_room_member, get_all_rooms
from app.websocket import handle_send_message
from bson.json_util import dumps

def chat_routes(app):
    @app.route('/')
    @login_required
    def index():
        username = current_user.username
        return render_template('index.html', username = username)
    
    @app.route('/room', methods = ['GET', 'POST'])
    @login_required
    def room():
        username = current_user.username
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            if len(room_name):
                room_id = save_room(room_name, username)
                return redirect(url_for('view_room', room_id = room_id))
            else:
                flash("Failed to create room", 'error')
        rooms = get_all_rooms()
        return render_template('room.html', rooms = rooms)



    @app.route('/rooms/<room_id>',methods = ['POST', 'GET'])
    @login_required
    def view_room(room_id):
        room = get_room(room_id)
        if room:
            username = current_user.username
            if not is_room_admin(room_id, username) and not is_room_member(room_id, username):
                add_room_member(room_id, room['room_name'], username)
            room_members = get_room_members(room_id)
        
                
            messages = get_messages(room_id)

            return render_template('view_room.html', username = current_user.username, room = room, room_members=room_members, messages = messages)

        else:
            return "Room not found", 404
        
    @app.route('/rooms/<room_id>/messages')
    @login_required
    def get_older_messages(room_id):
        room = get_room(room_id)
        if room:
            page = int(request.args.get('page', 0))
            messages = get_messages(room_id, page)
            return dumps(messages)
        else:
            return "Room not found", 404

    @app.route('/rooms/<room_id>/edit')
    @login_required
    def edit_room(room_id):
        room = get_room(room_id)
        if room and is_room_admin(room_id ,current_user.username):
            return render_template('edit_room.html')
        
        else:
            return "Room not found", 404


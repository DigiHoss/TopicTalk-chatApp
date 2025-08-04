import pymongo
from pymongo.server_api import ServerApi
from bson import ObjectId
from datetime import datetime
# MongoDB driver "PyMongo" connection
uri = "mongodb+srv://user:Q1URsRGD8VSSKpRc@cluster0.nxt4mmc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
myclient = pymongo.MongoClient(uri, server_api=ServerApi('1'))

# Create our db
chatDB = myclient["ChatDB"]

rooms_collection = chatDB["rooms"]
room_members_collection = chatDB["room_members"]
messages_collection = chatDB["messages"]

# myMessages_col = chatDB["messages"]


# Create a new room by a username that is its admin
def save_room(room_name, created_by):
    room_id = rooms_collection.insert_one(
        {'room_name': room_name, 'created_by': created_by, 'created_at': datetime.now()}
    ).inserted_id
    add_room_member(room_id, room_name, created_by, is_room_admin=True)
    return room_id

# Add a room member
def add_room_member(room_id, room_name, username, is_room_admin=False):
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})

# Get the room created or existed
def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})

def update_room(room_id, room_name):
    rooms_collection.update_one({'_id': ObjectId(room_id)}, {'$set': {'name': room_name}})
    room_members_collection.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})



# def add_room_members(room_id, room_name, usernames, added_by):
#     room_members_collection.insert_many(
#         [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
#           'added_at': datetime.now(), 'is_room_admin': False} for username in usernames])


def remove_room_members(room_id, usernames):
    room_members_collection.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})


def get_room_members(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))


def get_rooms_for_user(username):
    return list(room_members_collection.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    return room_members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'is_room_admin': True})


def save_message(room_id, text, sender):
    messages_collection.insert_one({'room_id': room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})


MESSAGE_FETCH_LIMIT = 3


def get_messages(room_id, page=0):
    offset = page * MESSAGE_FETCH_LIMIT
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', -1).limit(MESSAGE_FETCH_LIMIT).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages[::-1]

def get_all_messages(room_id):
    """Get all messages for a specific room"""
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', 1))  # Sort by creation time ascending
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages


def get_all_rooms():
    return rooms_collection.find()

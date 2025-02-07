from flask import Flask, request, jsonify, send_from_directory
import uuid
import time
import os

app = Flask(__name__, static_folder='static')

chats = {}  # Store active chats with expiration
users = {}  # Store user sessions

EXPIRATION_TIME = 86400  # Default to 1 day

@app.route('/')
def serve_frontend():
    return send_from_directory('templates', 'home.html')

@app.route('/create')
def create_frontend():
    return send_from_directory('templates', 'create.html')

@app.route('/create_chat', methods=['POST'])
def create_chat():
    chat_id = str(uuid.uuid4())
    expiration = time.time() + EXPIRATION_TIME
    chats[chat_id] = {"messages": [], "expires_at": expiration}
    return jsonify({"chat_id": chat_id, "expires_at": expiration})

@app.route('/join_chat', methods=['POST'])
def join_chat():
    data = request.json
    chat_id = data.get('chat_id')
    username = data.get('username')
    access_code = data.get('access_code', str(uuid.uuid4()))
    
    if chat_id not in chats or time.time() > chats[chat_id]['expires_at']:
        return jsonify({"error": "Chat does not exist or has expired"}), 400
    
    users[(chat_id, username)] = access_code
    return jsonify({"access_code": access_code})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    chat_id = data.get('chat_id')
    username = data.get('username')
    access_code = data.get('access_code')
    message = data.get('message')
    
    if users.get((chat_id, username)) != access_code:
        return jsonify({"error": "Invalid access code"}), 403
    
    if chat_id not in chats or time.time() > chats[chat_id]['expires_at']:
        return jsonify({"error": "Chat does not exist or has expired"}), 400
    
    chats[chat_id]['messages'].append({"username": username, "message": message})
    return jsonify({"success": True})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    chat_id = request.args.get('chat_id')
    
    if chat_id not in chats or time.time() > chats[chat_id]['expires_at']:
        return jsonify({"error": "Chat does not exist or has expired"}), 400
    
    return jsonify(chats[chat_id]['messages'])

if __name__ == '__main__':
    app.run(debug=True)

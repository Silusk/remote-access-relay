# relay_server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "remote-access")
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

@app.route("/")
def home():
    return "🔗 Relay server running successfully on Render!"

# When a client connects (either host or viewer)
@socketio.on("connect")
def connect():
    print("Client connected:", request.sid)

@socketio.on("disconnect")
def disconnect():
    print("Client disconnected:", request.sid)
    # remove from mapping if exists
    for k, v in list(clients.items()):
        if v == request.sid:
            del clients[k]

# Register each device (host or controller)
@socketio.on("register")
def register(data):
    role = data.get("role")
    pin = data.get("pin")
    clients[(role, pin)] = request.sid
    print(f"Registered {role} with PIN {pin}")

# Relay messages between host and controller
@socketio.on("relay")
def relay(data):
    pin = data.get("pin")
    target_role = "controller" if data.get("from") == "host" else "host"
    target_sid = clients.get((target_role, pin))
    if target_sid:
        socketio.emit("relay", data, room=target_sid)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)

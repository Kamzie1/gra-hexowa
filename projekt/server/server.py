from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask
import random


class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.sio = SocketIO(self.app)
        self.app.config["SECRET_KEY"] = "aiagfibogie"
        self._setup_events()
        self.rooms = {}

    def run(self):
        self.sio.run(self.app, host="0.0.0.0", port=5000, debug=True)

    def _setup_events(self):
        @self.app.route("/")
        def main():
            return "SocketIO server działa!"

        @self.sio.on("connect")
        def connect():
            print("Client connected.")
            emit("message", "Welcome!", broadcast=True)

        @self.sio.on("disconnect")
        def disconnect(name):
            print("Client disconnected.")

        @self.sio.on("join")
        def join(id, name):
            flag = False
            for room_id, data in self.rooms.items():
                if room_id == id and not data["active"]:
                    data["users"].append(name)
                    join_room(room_id)
                    if len(data["users"]) == 2:
                        data["active"] = True
                        self.uruchom_gre(room_id)
                    flag = True

            if flag:
                print("joined")
                return {"joined": True, "name": name}
            print("not joined")
            return {"joined": False}

        @self.sio.on("create")
        def create(name):
            try:
                room_id = self.generate(4)
                self.rooms[room_id] = {"users": [name], "active": False}
                join_room(room_id)
                return {"created": True, "id": room_id}
            except:
                return {"created": False}

    def uruchom_gre(self, room):
        emit("start_game", room=room)

    @staticmethod
    def generate(length=4):
        wynik = ""
        for _ in range(length):
            wynik += str(random.randint(0, 9))
        return wynik

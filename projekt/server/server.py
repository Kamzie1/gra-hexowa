from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, request
import random
from .state import create_state
import os


class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.sio = SocketIO(self.app)
        self.app.config["SECRET_KEY"] = "aiagfibogie"
        self._setup_events()
        self.rooms = {}
        self.users = {}

    def run(self):
        self.sio.run(self.app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    def _setup_events(self):
        @self.app.route("/")
        def main():
            return "SocketIO server działa!"

        @self.sio.on("connect")
        def connect():
            print("Client connected.")

        @self.sio.on("disconnect")
        def disconnect():
            print("Client disconnected.")

        @self.sio.on("join")
        def join(id, name):
            flag = False
            sid = request.sid
            if sid in self.users:
                return {"joined": False, "message": "Nazwa już istnieje"}
            for room_id, data in self.rooms.items():
                if room_id == id and not data["active"]:
                    data["users"].append(name)
                    data["sid"].append(sid)
                    self.users[sid] = room_id
                    join_room(room_id)
                    if len(data["users"]) == 2:
                        print(self.rooms[room_id])
                        data["active"] = True
                        self.uruchom_gre(room_id)
                    flag = True

            if flag:
                print("joined")
                return {"joined": True}
            print("not joined")
            return {"joined": False, "message": "nie ma takiego pokoju"}

        @self.sio.on("create")
        def create(name):
            sid = request.sid
            if sid in self.users:
                return {"created": False, "message": "Nazwa już istnieje"}
            try:
                room_id = self.generate(4)
                self.rooms[room_id] = {"users": [name], "active": False, "sid": [sid]}
                self.users[sid] = room_id
                join_room(room_id)
                return {"created": True, "id": room_id}
            except:
                return {"created": False, "message": "Coś poszło nie tak"}

        @self.sio.on("new_state")
        def new_state(data):
            print("new state incoming!!")
            sid = request.sid
            room_id = self.users[sid]
            emit("new_state", data, room=room_id)

        @self.sio.on("end_game")
        def end_game(result):
            sid = request.sid
            room_id = self.users[sid]
            emit("end_game", result, to=sid)
            emit("end_game", -1 * result, to=room_id, skip_sid=sid)

    def uruchom_gre(self, room_id):
        data = self.rooms[room_id]
        package1 = {"x": 6, "y": 6, "frakcja": "japonia", "color": "red", "id": 1}
        package2 = {
            "x": 20,
            "y": 12,
            "frakcja": "japonia",
            "color": "blue",
            "id": 0,
        }
        starting_state = create_state(
            package1, data["users"][0], package2, data["users"][1]
        )
        if random.randint(1, 2) == 1:
            emit(
                "start_game",
                {
                    data["users"][0]: package1,
                    data["users"][1]: package2,
                    "users": [data["users"][0], data["users"][1]],
                    "state": starting_state,
                },
                to=data["sid"][0],
            )
            emit(
                "start_game",
                {
                    data["users"][0]: package1,
                    data["users"][1]: package2,
                    "users": [data["users"][1], data["users"][0]],
                    "state": starting_state,
                },
                to=data["sid"][1],
            )
        else:
            emit(
                "start_game",
                {
                    data["users"][0]: package2,
                    data["users"][1]: package1,
                    "users": [data["users"][0], data["users"][1]],
                    "state": starting_state,
                },
                to=data["sid"][0],
            )
            emit(
                "start_game",
                {
                    data["users"][0]: package2,
                    data["users"][1]: package1,
                    "users": [data["users"][1], data["users"][0]],
                    "state": starting_state,
                },
                to=data["sid"][1],
            )

    @staticmethod
    def generate(length=4):
        wynik = ""
        for _ in range(length):
            wynik += str(random.randint(0, 9))
        return wynik

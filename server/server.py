import eventlet

eventlet.monkey_patch()

from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, request, session
import random
from .state import create_state
import os


class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.sio = SocketIO(self.app, async_mode="eventlet")
        self.app.config["SECRET_KEY"] = "aiagfibogie"
        self.app.config["SESSION_PERMANENT"] = True
        self.app.config["SESSION_TYPE"] = "filesystem"
        self._setup_events()
        self.rooms = {}
        self.last_state = None
        print("init finished")

    def run(self):
        print("run started")
        self.sio.run(
            self.app,
            host="::",
            port=int(os.environ.get("PORT", 5000)),
            debug=False,
        )

    def _setup_events(self):
        @self.app.route("/")
        def main():
            print("main route viewed")
            return "SocketIO server 1 działa!"

        @self.sio.on("connect")
        def connect():
            print("Client connected.")
            if session.get("name") and session.get("room_id"):
                join_room(session["room_id"])

        @self.sio.on("disconnect")
        def disconnect(sid):
            print("Client disconnected.")

        @self.sio.on("join")
        def join(id, name):
            flag = False
            if session.get("name") and session.get("room_id"):
                return {"joined": False, "message": "Nazwa już istnieje"}
            for room_id, data in self.rooms.items():
                if room_id == id and not data["active"]:
                    data["users"].append(name)
                    session["name"] = name
                    session["room_id"] = room_id
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
            if session.get("name") and session.get("room_id"):
                return {"created": False, "message": "Nazwa już istnieje"}
            try:
                room_id = self.generate(4)
                self.rooms[room_id] = {"users": [name], "active": False}
                session["room_id"] = room_id
                session["name"] = name
                join_room(room_id)
                return {"created": True, "id": room_id}
            except:
                return {"created": False, "message": "Coś poszło nie tak"}

        @self.sio.on("new_state")
        def new_state(data):
            room_id = session["room_id"]
            self.last_state = data
            self.sio.emit("new_state", data, to=room_id)

        @self.sio.on("end_game")
        def end_game(result):
            sid = request.sid
            room_id = session["room_id"]
            self.sio.emit("end_game", result, to=sid)
            self.sio.emit("end_game", -1 * result, to=room_id, skip_sid=sid)
            session.pop("name", default=None)
            session.pop("room_id", default=None)
            self.rooms.pop(room_id)

    def uruchom_gre(self, room_id):
        sid = request.sid
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
        self.last_state = starting_state
        if random.randint(1, 2) == 1:
            emit(
                "start_game",
                {
                    data["users"][0]: package1,
                    data["users"][1]: package2,
                    "users": [data["users"][0], data["users"][1]],
                    "state": starting_state,
                },
                to=sid,
            )
            emit(
                "start_game",
                {
                    data["users"][0]: package1,
                    data["users"][1]: package2,
                    "users": [data["users"][1], data["users"][0]],
                    "state": starting_state,
                },
                to=room_id,
                skip_sid=sid,
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
                to=sid,
            )
            emit(
                "start_game",
                {
                    data["users"][0]: package2,
                    data["users"][1]: package1,
                    "users": [data["users"][1], data["users"][0]],
                    "state": starting_state,
                },
                to=room_id,
                skip_sid=sid,
            )

    @staticmethod
    def generate(length=4):
        wynik = ""
        for _ in range(length):
            wynik += str(random.randint(0, 9))
        return wynik

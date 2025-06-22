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
        self.last_state = None
        print("init finished")

    def run(self):
        print("run started")
        self.sio.run(
            self.app,
            host="0.0.0.0",
            port=5000,
            debug=True,
        )

    def _setup_events(self):
        @self.app.route("/")
        def main():
            print("main route viewed")
            return "SocketIO server 2 działa!"

        @self.sio.on("connect")
        def connect():
            print("Client connected.")

        @self.sio.on("disconnect")
        def disconnect(sid):
            print("Client disconnected.")

        @self.sio.on("sync")
        def sync(name):
            print("name", name)
            if name is not None and name in self.users:
                print("name is found...")
                for client in self.rooms[self.users[name]]["users"]:
                    if client["name"] == name:
                        client["sid"] = request.sid
                        join_room(self.users[name], sid=client["sid"])
                        room_id = self.users[name]
                        print("reconnected")
                        emit(
                            "new state",
                            {
                                "state": self.rooms[room_id]["state"],
                                "turn": self.rooms[room_id]["turn"],
                                "players": self.rooms[room_id]["players"],
                            },
                            to=room_id,
                        )

        @self.sio.on("join")
        def join(id, name):
            flag = False
            if name in self.users:
                return {"joined": False, "message": "Nazwa już istnieje"}
            for room_id, data in self.rooms.items():
                if room_id == id and not data["active"]:
                    client = {"name": name, "sid": request.sid}
                    data["users"].append(client)
                    self.rooms[room_id]["players"][name] = 1000
                    self.users[name] = room_id
                    join_room(room_id, sid=request.sid)
                    if len(data["users"]) == 2:
                        print("start: ", self.rooms[room_id])
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
            if name in self.users:
                return {"created": False, "message": "Nazwa już istnieje"}
            try:
                room_id = self.generate(4)
                client = {"name": name, "sid": request.sid}
                self.rooms[room_id] = {
                    "users": [client],
                    "active": False,
                    "state": None,
                    "players": {name: 1000},
                    "turn": 0,
                }
                join_room(room_id, sid=request.sid)
                self.users[name] = room_id
                return {"created": True, "id": room_id}
            except:
                return {"created": False, "message": "Coś poszło nie tak"}

        @self.sio.on("new_state")
        def new_state(data):
            print("got state")
            room_id = self.users[data["nadawca"]]
            self.rooms[room_id]["state"] = data["state"]
            self.rooms[room_id]["players"][data["player"]["name"]] = data["player"][
                "gold"
            ]
            self.rooms[room_id]["turn"] += 1
            print(
                "Turn",
                self.rooms[room_id]["turn"],
                "----------------------------------------------",
            )
            self.sio.emit(
                "new_state",
                {
                    "state": self.rooms[room_id]["state"],
                    "turn": self.rooms[room_id]["turn"],
                    "players": self.rooms[room_id]["players"],
                },
                to=room_id,
            )

        @self.sio.on("end_game")
        def end_game(data):
            room_id = self.users[data["nadawca"]]
            self.sio.emit("end_game", data["result"], to=room_id)
            clients = self.rooms[room_id]["users"]
            for client in clients:
                self.users.pop(client["name"])
                leave_room(room_id, sid=client["sid"])
            self.rooms.pop(room_id)

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
        num = random.randint(0, 1)
        starting_state = create_state(
            package1,
            data["users"][num]["name"],
            package2,
            data["users"][1 - num]["name"],
        )
        self.last_state = starting_state
        emit(
            "start_game",
            {
                data["users"][num]["name"]: package1,
                data["users"][1 - num]["name"]: package2,
                "users": [data["users"][0]["name"], data["users"][1]["name"]],
                "state": starting_state,
            },
            to=data["users"][0]["sid"],
        )
        emit(
            "start_game",
            {
                data["users"][num]["name"]: package1,
                data["users"][1 - num]["name"]: package2,
                "users": [data["users"][1]["name"], data["users"][0]["name"]],
                "state": starting_state,
            },
            to=data["users"][1]["sid"],
        )

    @staticmethod
    def generate(length=4):
        wynik = ""
        for _ in range(length):
            wynik += str(random.randint(0, 9))
        return wynik

from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, request
import random
from .state import create_state
from .mapa import create_map
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
            return "SocketIO server działa!"

        @self.sio.on("connect")
        def connect():
            print("Client connected.")

        @self.sio.on("disconnect")
        def disconnect():
            sid = request.sid
            for id, data in self.rooms.items():
                for client in data["users"]:
                    if client["sid"] == sid:
                        client["online"] = False
            print("Client disconnected.")

        @self.sio.on("sync")
        def sync(name):
            print("name", name)
            if name is not None and name in self.users:
                print("name is found...")
                for client in self.rooms[self.users[name]]["users"]:
                    if client["name"] == name:
                        client["sid"] = request.sid
                        client["online"] = True
                        join_room(self.users[name], sid=client["sid"])
                        room_id = self.users[name]
                        print("reconnected")
                        emit(
                            "new state",
                            {
                                "state": self.rooms[room_id]["state"],
                                "turn": self.rooms[room_id]["turn"],
                                "users": self.rooms[room_id]["users"],
                                "spectators": self.rooms[room_id]["spectators"],
                            },
                            to=room_id,
                        )

        @self.sio.on("join")
        def join(id, name):
            flag = False
            if name in self.users:
                if id == self.users[name]:
                    for client in self.rooms[self.users[name]]["users"]:
                        if not client["online"]:
                            client["online"] = True
                            join_room(id, sid=request.sid)
                            self.sio.emit(
                                "start_game",
                                {
                                    "users": self.rooms[self.users[name]]["users"],
                                    "spectators": self.rooms[self.users[name]][
                                        "spectators"
                                    ],
                                    "state": self.rooms[self.users[name]]["state"],
                                    "turn": self.rooms[self.users[name]]["turn"],
                                    "mapa": self.rooms[self.users[name]]["mapa"],
                                },
                                to=request.sid,
                            )
                            flag = True
                if not flag:
                    return {"joined": False, "message": "Nazwa już istnieje"}
            for room_id, data in self.rooms.items():
                if room_id == id and not data["active"]:
                    client = {
                        "name": name,
                        "sid": request.sid,
                        "online": True,
                        "fraction": "Japonia",
                        "color": "red",
                        "gold": 1000,
                        "ready": 0,
                    }
                    data["users"].append(client)
                    self.users[name] = room_id
                    join_room(room_id, sid=request.sid)
                    flag = True
                    self.sio.emit("ustawienia", self.rooms[room_id], to=room_id)

            if flag:
                print("joined")
                return {"joined": True, "room": self.rooms[id]}
            print("not joined")
            return {"joined": False, "message": "nie ma takiego pokoju"}

        @self.sio.on("create")
        def create(name):
            if name in self.users:
                return {"created": False, "message": "Nazwa już istnieje"}
            try:
                room_id = self.generate(4)
                client = {
                    "name": name,
                    "sid": request.sid,
                    "online": True,
                    "fraction": "Japonia",
                    "color": "red",
                    "gold": 1000,
                    "ready": 0,
                }
                self.rooms[room_id] = {
                    "users": [client],
                    "spectators": [],
                    "active": False,
                    "state": None,
                    "turn": 0,
                    "room_id": room_id,
                }
                join_room(room_id, sid=request.sid)
                self.users[name] = room_id
                return {"created": True, "room": self.rooms[room_id]}
            except:
                return {"created": False, "message": "Coś poszło nie tak"}

        @self.sio.on("settings")
        def new_settings(data):
            print(data)
            nadawca = data["nadawca"]
            ustawienia = data["settings"]
            room_id = self.users[nadawca]

            for client in self.rooms[room_id]["spectators"]:
                if client["name"] == nadawca:
                    client["fraction"] = ustawienia["fraction"]
                    client["color"] = ustawienia["color"]
                    client["ready"] = ustawienia["ready"]
                    if client["fraction"] != "Spectator":
                        self.rooms[room_id]["spectators"].remove(client)
                        self.rooms[room_id]["users"].append(client)

            for client in self.rooms[room_id]["users"]:
                if client["name"] == nadawca:
                    client["fraction"] = ustawienia["fraction"]
                    client["color"] = ustawienia["color"]
                    client["ready"] = ustawienia["ready"]
                    if client["fraction"] == "Spectator":
                        self.rooms[room_id]["users"].remove(client)
                        self.rooms[room_id]["spectators"].append(client)
            self.rooms[room_id]["ustawienia"] = ustawienia["ustawienia"]

            ready = False
            for client in self.rooms[room_id]["users"]:
                ready = True
                if client["ready"] == 0:
                    ready = False
                    break

            if ready:
                print("start: ", self.rooms[room_id])
                data["active"] = True
                self.uruchom_gre(room_id)

            else:
                self.sio.emit("ustawienia", self.rooms[room_id], to=room_id)

        @self.sio.on("new_state")
        def new_state(data):
            print("got state")
            room_id = self.users[data["nadawca"]]
            self.rooms[room_id]["state"] = data["state"]
            for client in self.rooms[room_id]["users"]:
                if client["name"] == data["nadawca"]:
                    client["gold"] = data["gold"]

            self.rooms[room_id]["turn"] += 1
            print(
                "Turn",
                self.rooms[room_id]["turn"],
                "----------------------------------------------",
            )
            self.sio.emit(
                "new_state",
                {
                    "users": self.rooms[room_id]["users"],
                    "spectators": self.rooms[room_id]["spectators"],
                    "state": self.rooms[room_id]["state"],
                    "turn": self.rooms[room_id]["turn"],
                },
                to=room_id,
            )

        @self.sio.on("end_game")
        def end_game(data):
            room_id = self.users[data["nadawca"]]
            result = data["result"]
            for client in self.rooms[room_id]["users"]:
                if client["name"] == result:
                    self.rooms[room_id]["users"].remove(client)
                    self.rooms[room_id]["spectators"].append(client)
            print(self.rooms[room_id]["users"])
            print(self.rooms[room_id]["spectators"])

            self.rooms[room_id]["state"]["jednostki"] = [
                jednostka
                for jednostka in self.rooms[room_id]["state"]["jednostki"]
                if jednostka["owner"] != result
            ]

            self.rooms[room_id]["state"]["budynki"] = [
                budynek
                for budynek in self.rooms[room_id]["state"]["budynki"]
                if budynek["owner"] != result
            ]

            i = 0
            for user in self.rooms[room_id]["users"]:
                for jednostka in self.rooms[room_id]["state"]["jednostki"]:
                    if jednostka["owner_id"] == user["id"]:
                        jednostka["owner_id"] = i
                for budynek in self.rooms[room_id]["state"]["budynki"]:
                    if budynek["owner_id"] == user["id"]:
                        budynek["owner_id"] = i
                user["id"] = i
                i += 1

            print(self.rooms[room_id]["state"]["jednostki"])
            print(self.rooms[room_id]["state"]["budynki"])

            emit(
                "new_state",
                {
                    "state": self.rooms[room_id]["state"],
                    "turn": self.rooms[room_id]["turn"],
                    "users": self.rooms[room_id]["users"],
                    "spectators": self.rooms[room_id]["spectators"],
                },
                to=room_id,
            )

            if len(self.rooms[room_id]["users"]) == 1:
                print(self.rooms[room_id]["users"])
                emit("end_game", self.rooms[room_id]["users"][0]["name"], to=room_id)

            """
            self.sio.emit("end_game", data["result"], to=room_id)
            clients = self.rooms[room_id]["users"]
            for client in clients:
                self.users.pop(client["name"])
                leave_room(room_id, sid=client["sid"])
            self.rooms.pop(room_id)"""

        @self.sio.on("leave")
        def leave(name):
            room_id = self.users[name]
            leave_room(room_id, sid=request.sid)
            for client in self.rooms[room_id]["users"]:
                if client["name"] == name:
                    self.rooms[room_id]["users"].remove(client)
                    break
            self.users.pop(name)
            if len(self.rooms[room_id]["users"]) == 0:
                self.rooms.pop(room_id)
            else:
                self.sio.emit("ustawienia", self.rooms[room_id], to=room_id)

    def uruchom_gre(self, room_id):
        data = self.rooms[room_id]
        random.shuffle(data["users"])
        i = 0
        for client in data["users"]:
            client["id"] = i
            i += 1
        mapa = create_map(data["ustawienia"])
        print("mapped")
        starting_state = create_state(data["users"], data["ustawienia"])
        data["state"] = starting_state
        data["mapa"] = mapa
        print("emitting...")
        print(len(starting_state["budynki"]))
        emit(
            "start_game",
            {
                "users": self.rooms[room_id]["users"],
                "spectators": self.rooms[room_id]["spectators"],
                "state": starting_state,
                "turn": self.rooms[room_id]["turn"],
                "mapa": mapa,
            },
            to=room_id,
        )

    @staticmethod
    def generate(length=4):
        wynik = ""
        for _ in range(length):
            wynik += str(random.randint(0, 9))
        return wynik

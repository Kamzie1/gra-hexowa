from projekt.narzedzia import Singleton, KoniecGry, oblicz_pos
from projekt.player import Player
from projekt.assetMenager import AssetManager
import socketio
import threading
import socketio.exceptions
import time
from projekt.akcjeMenager import AkcjeMenager


class Client(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.turn = 0
        self.ekran = 0
        self.start_game = False
        self.connected = False
        self.sio = socketio.Client(reconnection=True)
        self._setup_events()
        self.state_loaded = True
        self.name = "anonim"

    def load_player(self):
        return {
            "name": self.name,
            "x": self.users[self.id]["x"],
            "y": self.users[self.id]["y"],
            "frakcja": AssetManager.frakcja[self.users[self.id]["fraction"]],
            "num": self.users[self.id]["id"],
            "pos": oblicz_pos(self.users[self.id]["x"], self.users[self.id]["y"]),
            "color": self.users[self.id]["color"],
            "id": self.id,
            "gold": self.users[self.id]["gold"],
            "akcje": self.users[self.id]["akcje"],
        }

    def load_spectator(self):
        return {
            "name": self.name,
            "x": self.width / 2,
            "y": self.height / 2,
            "frakcja": AssetManager.frakcja["Japonia"],
            "num": -1,
            "pos": oblicz_pos(self.width / 2, self.height / 2),
            "color": "red",
            "id": -1,
            "gold": 0,
            "akcje": None,
        }

    def _setup_events(self):
        @self.sio.event
        def connect():
            print("[CLIENT] Connected to server")
            self.connected = True
            self.sio.emit("sync", self.name)

        @self.sio.event
        def disconnect():
            print("[CLIENT] Disconnected from server")
            self.connected = False

        @self.sio.on("message")
        def on_message(data):
            print(f"[SERVER] Message: {data}")

        @self.sio.on("start_game")
        def start_game(data):
            print("start game")
            self.map = data["mapa"]
            self.width = data["ustawienia"]["width"]
            self.height = data["ustawienia"]["height"]
            self.users = data["users"]
            self.spectators = data["spectators"]
            self.turn = data["turn"]
            self.start_game = True
            self.ekran = 2
            self.state = data["state"]
            self.pogoda = data["pogoda"]
            for user in self.users:
                if user["name"] == self.name:
                    self.id = user["id"]
                    self.player = Player(self.load_player())
            for user in self.spectators:
                if user["name"] == self.name:
                    self.player = Player(self.load_spectator())
                    self.ekran = 3

        @self.sio.on("new_state")
        def import_state(data):
            print("got new state")
            print(data["state"]["jednostki"])
            self.users = data["users"]
            self.state = data["state"]
            self.pogoda = data["pogoda"]
            print(self.users)
            self.spectators = data["spectators"]
            for user in data["users"]:
                if user["name"] == self.name:
                    self.id = user["id"]
                    self.player.id = self.id
                    self.ekran = 2

            for user in data["spectators"]:
                if user["name"] == self.name:
                    self.id = -1
                    self.player.id = self.id
                    self.ekran = 3
            self.state_loaded = False
            self.player.akcje = self.users[self.id]["akcje"]
            self.turn = data["turn"]
            if self.ekran == 2:
                self.player.gold = data["users"][self.id]["gold"]
                if self.turn % len(self.users) == self.player.id and self.turn >= len(
                    self.users
                ):
                    self.player.akcjeMenager.turn()
                    self.player.gold += self.player.zloto_income
                    self.mapa.heal()
            self.mapa.import_state(self.state, self.users)
            match (self.pogoda[0]):
                case 1:
                    print("słońce")
                    self.mapa.refresh_movement(-4)
                case 2:
                    print("mgła")
                    self.mapa.refresh_wzrok(-4)
                case _:
                    pass
            self.mapa.calculate_widok()
            self.state_loaded = True

        @self.sio.on("end_game")
        def end_game(result):
            self.ekran = 3
            self.id = -1
            if result == self.name:
                KoniecGry().display("Wygrałeś", self.player.color)
            else:
                KoniecGry().display("Przegrałeś", self.player.color)

        @self.sio.on("ustawienia")
        def ustawienia(room):
            self.room = room

    def start(self, url="http://192.168.50.205:5000"):
        def run():
            while True:
                try:
                    self.sio.connect(
                        "https://gra-hexowa-production.up.railway.app",
                        transports=["websocket"],
                    )
                    break
                except socketio.exceptions.ConnectionError as e:
                    print(f"cant connect with a server, {e}")
                    time.sleep(5)

        threading.Thread(target=run, daemon=True).start()

    def test(self):
        def run():
            while True:
                try:
                    self.sio.connect(
                        "http://localhost:5000",
                        transports=["websocket"],
                    )
                    break
                except socketio.exceptions.ConnectionError as e:
                    print(f"cant connect with a server, {e}")

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.sio.disconnect()

    def handle_join(self, data):
        if data.get("joined") == False:
            print("wrong room id or else")
        else:
            self.ekran = 1
            self.room = data["room"]

    def handle_create(self, data):
        if data.get("created") == False:
            print("something went wrong")
        else:
            print(f"created room: {data["room"]["room_id"]}")
            self.ekran = 1
            self.room = data["room"]

    def join_room(self, id, name):
        if self.connected:
            self.sio.emit("join", (id, name), callback=self.handle_join)
            self.name = name
            print("new name:", self.name)

    def create_room(self, name):
        if self.connected:
            self.sio.emit("create", name, callback=self.handle_create)
            self.name = name
            print("new name:", self.name)

    def send_state(self, state):
        self.sio.emit(
            "new_state",
            {
                "state": state,
                "nadawca": self.name,
                "gold": self.player.gold,
                "akcje": self.player.akcje,
            },
        )

    def send_result(self, result):
        self.sio.emit("end_game", {"result": result, "nadawca": self.name})

    def leave(self):
        self.sio.emit("leave", self.name)

    def ustawienia(self, ustawienia):
        self.sio.emit("settings", {"settings": ustawienia, "nadawca": self.name})

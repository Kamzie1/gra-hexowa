import socketio
import threading
import socketio.exceptions
from projekt.narzedzia import KoniecGry
from projekt.ustawienia import Width, Height


class Client:
    def __init__(self):
        self.ekran = 0
        self.start_game = False
        self.connected = False
        self.sio = socketio.Client()
        self._setup_events()
        self.state_loaded = True
        self.turn = 0
        self.koniecGry = KoniecGry(Width, Height)
        self.name = None

    def _setup_events(self):
        @self.sio.event
        def connect():
            print("[CLIENT] Connected to server")
            self.connected = True

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
            self.info = data
            self.names = data["users"]
            self.start_game = True
            self.state = data["state"]

        @self.sio.on("new_state")
        def import_state(data):
            print("got new state")
            self.state_loaded = False
            self.turn = data["turn"]
            self.mapa.player.gold = data["players"][self.name]
            self.mapa.import_state(data["state"])
            if self.turn % 2 == self.mapa.player.id and self.turn != 1:
                self.mapa.zarabiaj()
                self.mapa.heal()
            self.state_loaded = True

        @self.sio.on("end_game")
        def end_game(result):
            if result == self.name:
                self.koniecGry.display("Wygrałeś", self.mapa.player.color)
            else:
                self.koniecGry.display("Przegrałeś", self.mapa.player.color)

    def start(self, url="http://192.168.50.205:5000"):
        def run():
            try:
                self.sio.connect(
                    "https://gra-hexowa-production.up.railway.app",
                    transports=["websocket"],
                    auth={"name": self.name},
                )
                self.sio.wait()
            except socketio.exceptions.ConnectionError as e:
                print(f"cant connect with a server, {e}")

        threading.Thread(target=run, daemon=True).start()

    def test(self):
        def run():
            try:
                self.sio.connect(
                    "http://localhost:5000",
                    transports=["websocket"],
                    auth={"name": self.name},
                )
                self.sio.wait()
            except socketio.exceptions.ConnectionError as e:
                print(f"cant connect with a server, {e}")

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.sio.disconnect()

    @staticmethod
    def handle_join(data):
        if data.get("joined") == False:
            print("wrong room id or else")
        else:
            print("joined")

    @staticmethod
    def handle_create(data):
        if data.get("created") == False:
            print("something went wrong")
        else:
            print(f"created room: {data.get('id')}")

    def join_room(self, id, name):
        if self.connected:
            self.sio.emit("join", (id, name), callback=self.handle_join)
            self.name = name

    def create_room(self, name):
        if self.connected:
            self.sio.emit("create", name, callback=self.handle_create)
            self.name = name

    def send_state(self, state):
        player = {"name": self.name, "gold": self.mapa.player.gold}
        self.sio.emit(
            "new_state", {"state": state, "nadawca": self.name, "player": player}
        )

    def send_result(self, result):
        self.sio.emit("end_game", {"result": result, "nadawca": self.name})

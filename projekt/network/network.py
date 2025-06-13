import socketio
import threading
import socketio.exceptions
import random
from projekt.jednostki import Japonia, Japonia2


class Client:
    def __init__(self):
        self.start_game = False
        self.connected = False
        self.sio = socketio.Client()
        self._setup_events()
        self.state_loaded = True
        self.turn = 0

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
            self.turn += 1
            self.mapa.import_state(data)
            if self.turn % 2 == self.mapa.player.id and self.turn != 1:
                self.mapa.zarabiaj()
                self.mapa.heal()
            self.state_loaded = True

    def start(self, url="http://192.168.50.195:5000"):
        def run():
            try:
                self.sio.connect(url)
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

    def create_room(self, name):
        if self.connected:
            self.sio.emit("create", name, callback=self.handle_create)

    def send_state(self, state):
        self.sio.emit("new_state", state)

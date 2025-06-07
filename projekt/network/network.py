import socketio
import threading
from projekt.gra import Gra
import pygame
import socketio.exceptions


class Client:
    def __init__(self):
        self.sio = socketio.Client()
        self._setup_events()

    def _setup_events(self):
        @self.sio.event
        def connect():
            print("[CLIENT] Connected to server")

        @self.sio.event
        def disconnect():
            print("[CLIENT] Disconnected from server")

        @self.sio.on("message")
        def on_message(data):
            print(f"[SERVER] Message: {data}")

        @self.sio.on("start_game")
        def start_game():
            pygame.quit()
            gra = Gra(
                6,
                6,
                6,
                6,
                1,
                2,
            )
            gra.run()

    def start(self, url="http://127.0.0.1:5000"):
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
        self.sio.emit("join", (id, name), callback=self.handle_join)

    def create_room(self, name):
        self.sio.emit("create", name, callback=self.handle_create)

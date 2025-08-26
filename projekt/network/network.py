from .state import create_state
from projekt.narzedzia import Singleton, KoniecGry, oblicz_pos
from projekt.player import Player
from projekt.assetMenager import AssetManager


class Client(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.turn = 0

    def start_game(self, data):
        print("start game")
        self.info = data
        self.names = data["users"]
        self.start_game = True
        self.state = data["state"]
        self.player = Player(self.load_player(0))
        self.opponent = Player(self.load_player(1))

    def load_player(self, id):
        name = self.names[id]
        return {
            "name": name,
            "x": self.info[name]["x"],
            "y": self.info[name]["y"],
            "frakcja": AssetManager.frakcja[self.info[name]["frakcja"]],
            "num": self.info[name]["id"],
            "pos": oblicz_pos(self.info[name]["x"], self.info[name]["y"]),
            "color": self.info[name]["color"],
            "id": id,
            "akcje": self.load_akcje(),
        }

    def load_akcje(self):
        return {
            "zloto_upgrade": 1,
            "srebro_upgrade": 1,
            "stal_upgrade": 1,
            "food_upgrade": 1,
            "mury_upgrade": 1,
            "zloto_rozkaz_cooldown": False,
            "zloto_rozkaz": 1,
            "srebro_rozkaz": 1,
            "stal_rozkaz": 1,
            "food_rozkaz": 1,
            "movement_rozkaz_cooldown": False,
            "movement_rozkaz": 0,
        }

    def import_state(self):
        print("got new state")
        self.turn += 1
        bufor = self.player
        self.player = self.opponent
        self.opponent = bufor

        self.user = self.player.name
        self.id = self.player.id

    def send_state(self, state):
        self.state = state
        self.import_state()

    def uruchom_gre(self):
        package1 = {"x": 6, "y": 6, "frakcja": "Japonia", "color": "red", "id": 0}
        package2 = {
            "x": 10,
            "y": 10,
            "frakcja": "Prusy",
            "color": "blue",
            "id": 1,
        }
        starting_state = create_state(package1, package2)

        return {
            "client1": package1,
            "client2": package2,
            "users": ["client1", "client2"],
            "state": starting_state,
        }

    def end_game(self, result):
        match (result):
            case -1:
                KoniecGry().display("Przegrałeś", self.player.color)
            case 1:
                KoniecGry().display("Wygrałeś", self.player.color)

    def pay(self, cost):
        Client().player.gold -= cost["zloto"]
        Client().player.srebro -= cost["srebro"]
        Client().player.stal -= cost["stal"]
        Client().player.food -= cost["food"]
        Client().player.medals -= cost["medale"]

    def validate_cost(self, cost):
        if Client().player.gold < cost["zloto"]:
            return False
        if Client().player.srebro < cost["srebro"]:
            return False
        if Client().player.stal < cost["stal"]:
            return False
        if Client().player.food < cost["food"]:
            return False
        if Client().player.medals < cost["medale"]:
            return False
        return True

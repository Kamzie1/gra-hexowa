from .state import create_state


class Client:
    def __init__(self):
        self.state_loaded = True
        self.turn = 0

    def start_game(self, data):
        print("start game")
        self.info = data
        self.names = data["users"]
        self.start_game = True
        self.state = data["state"]

    def import_state(self):
        print("got new state")
        self.state_loaded = False
        self.turn += 1
        self.mapa.import_state(self.state)
        bufor = self.mapa.player
        self.mapa.player = self.mapa.opponent
        self.mapa.opponent = bufor

        self.user = self.mapa.player.name
        self.id = self.mapa.player.id
        if self.turn % 2 == self.mapa.player.id and self.turn != 1:
            self.mapa.zarabiaj()
            self.mapa.heal()
        self.state_loaded = True

    def send_state(self, state):
        self.state = state
        self.import_state()

    def uruchom_gre(self):
        package1 = {"x": 6, "y": 6, "frakcja": "Japonia", "color": "red", "id": 0}
        package2 = {
            "x": 2,
            "y": 2,
            "frakcja": "Japonia",
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

    def end_game(self, result, koniecGry):
        match (result):
            case -1:
                koniecGry.display("Przegrałeś", self.mapa.player.color)
            case 1:
                koniecGry.display("Wygrałeś", self.mapa.player.color)

from .state import starting_state

tile_width = 112
tile_height = 108


def id_to_pos(x, y):
    if y % 2 == 0:
        pos = (
            x * tile_width + tile_width / 2,
            y * tile_height / 4 * 3 + tile_height / 2,
        )
    else:
        pos = (
            x * tile_width + tile_width,
            y * tile_height / 4 * 3 + tile_height / 2,
        )
    return pos


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
        package1 = {"x": 6, "y": 6, "frakcja": "japonia", "color": "blue", "id": 1}
        package2 = {
            "x": 6,
            "y": 9,
            "frakcja": "japonia",
            "color": "red",
            "id": 0,
        }
        starting_state["budynek"][0]["pos"] = id_to_pos(package1["x"], package1["y"])
        starting_state["budynek"][0]["owner_id"] = package1["id"]
        starting_state["budynek"][0]["color"] = package1["color"]
        starting_state["budynek"][1]["owner_id"] = package2["id"]
        starting_state["budynek"][1]["color"] = package2["color"]
        starting_state["budynek"][1]["pos"] = id_to_pos(package2["x"], package2["y"])
        return {
            "client1": package2,
            "client2": package1,
            "users": ["client1", "client2"],
            "state": starting_state,
        }

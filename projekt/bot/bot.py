from os.path import join
import random
import yaml
from projekt.narzedzia import get_sasiedzi, id_to_pos, priority_queue, pos_to_id
from projekt.assetMenager import AssetManager


class Bot:
    def __init__(self):
        with open(
            join("projekt", "bot", "action_scores.yaml"), "r", encoding="utf-8"
        ) as f:
            self.action_scores = yaml.safe_load(f)

        with open(
            join("projekt", "bot", "ustawienia.yaml"), "r", encoding="utf-8"
        ) as f:
            self.ustawienia = yaml.safe_load(f)

    def turn(self, state, mapa, user):
        state = self.move_phase(state, mapa, user)
        state = self.recruit_phase(state, mapa, user)
        return state

    def aquire_targets(self, state, user_id, user_team):
        targets = []
        for budynek in state["budynki"]:
            if budynek["team"] == user_team:
                continue
            for jednostka in state["jednostki"]:
                if jednostka["owner_id"] != user_id:
                    continue
                if self.get_squad_ruch(jednostka) <= 0:
                    continue
                distance = self.calculate_distance(jednostka["pos"], budynek["pos"])
                if budynek["id"] == 0:
                    score = self.action_scores["Miasto"] - distance
                elif budynek["id"] < 5:
                    score = self.action_scores["Wioska"] - distance
                    targets.append(
                        (
                            score,
                            jednostka["pos"],
                            budynek["pos"],
                        )
                    )
        for enemyUnit in state["jednostki"]:
            if enemyUnit["team"] == user_team:
                continue
            for unit in state["jednostki"]:
                if unit["owner_id"] != user_id:
                    continue
                if self.get_squad_ruch(unit) <= 0:
                    continue
                distance = self.calculate_distance(unit["pos"], enemyUnit["pos"])
                score = (
                    self.action_scores["EnemyUnit"]
                    + self.calculate_squad_score(enemyUnit)
                    - distance
                )
                targets.append((score, unit["pos"], enemyUnit["pos"]))

        return sorted(targets, reverse=True)

    def calculate_squad_score(self, unit):
        score = 0
        for wojownik in unit["jednostki"]:
            score += self.calculate_wojownik_score(wojownik)
        return score

    def calculate_wojownik_score(self, wojownik):
        return wojownik["zdrowie"]

    def calculate_distance(self, pos1, pos2):
        return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

    def move_phase(self, state, mapa, user):
        targets = self.aquire_targets(state, user["id"], user["team"])
        used_units = set()
        for score, unit_pos, enemy_pos in targets:
            if unit_pos in used_units:
                continue
            for wojownik in state["jednostki"]:
                if wojownik["pos"] == unit_pos:
                    used_units.add(wojownik["pos"])
                    self.move(wojownik, enemy_pos, mapa, state)
        return state

    def move(self, unit, enemyPos, mapa, state):
        trail, tablica_odwiedzonych = self.get_trail(unit, enemyPos, mapa)
        x, y = pos_to_id(enemyPos)
        my_x, my_y = pos_to_id(unit["pos"])
        goal = str(my_x) + "," + str(my_y)
        current = str(x) + "," + str(y)
        current_pos = (x, y)
        while (
            tablica_odwiedzonych[current_pos[0]][current_pos[1]] < 0
            and trail[current] != goal
            and trail[current] is not None
        ):
            if current not in trail:
                break
            current = trail[current]
            x, y = current.split(",")
            current_pos = (int(x), int(y))
        unit["pos"] = id_to_pos(current_pos[0], current_pos[1])
        for budynek in state["budynki"]:
            if budynek["pos"] == unit["pos"]:
                if budynek["id"] > 0:
                    budynek["team"] = unit["team"]
                    budynek["owner_id"] = unit["owner_id"]
                    budynek["owner"] = unit["owner"]
                    budynek["color"] = unit["color"]
                    print(budynek)

    def get_trail(self, unit, enemyUnit, mapa):
        Map = mapa["mapa"]
        tablica_odwiedzonych = [
            [-1 for _ in range(mapa["width"])] for _ in range(mapa["height"])
        ]
        queue = priority_queue()
        find_x, find_y = pos_to_id(enemyUnit)
        x, y = pos_to_id(unit["pos"])
        came_from = dict()
        came_from[str(x) + "," + str(y)] = None
        tablica_odwiedzonych[x][y] = self.get_squad_ruch(unit)
        queue.append((x, y, self.get_squad_ruch(unit)))
        while not queue.empty():
            x, y, ruch = queue.pop()
            if x == find_x and y == find_y:
                break
            sasiedzix, sasiedziy = get_sasiedzi(x, y)
            for i in range(6):
                if x + sasiedzix[i] >= mapa["width"] or x + sasiedzix[i] < 0:
                    continue
                if y + sasiedziy[i] >= mapa["height"] or y + sasiedziy[i] < 0:
                    continue
                if (
                    str(x + sasiedzix[i]) + "," + str(y + sasiedziy[i]) in came_from
                    or tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] >= 0
                ):
                    continue
                tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] = (
                    ruch
                    - AssetManager.get_tiles_property(
                        Map[x + sasiedzix[i]][y + sasiedziy[i]] - 1
                    )["koszt_ruchu"]
                )
                queue.append(
                    (
                        x + sasiedzix[i],
                        y + sasiedziy[i],
                        ruch
                        - AssetManager.get_tiles_property(
                            Map[x + sasiedzix[i]][y + sasiedziy[i]] - 1
                        )["koszt_ruchu"],
                    )
                )
                came_from[str(x + sasiedzix[i]) + "," + str(y + sasiedziy[i])] = (
                    str(x) + "," + str(y)
                )
        return came_from, tablica_odwiedzonych

    def recruit_phase(self, state, mapa, user):
        sasiedzix, sasiedziy = get_sasiedzi(user["x"], user["y"])
        i = random.randint(0, 5)
        state["jednostki"].append(
            self.get_squad(
                user,
                id_to_pos(sasiedzix[i] + user["x"], sasiedziy[i] + user["y"]),
                AssetManager.frakcja[user["frakcja"]]["jednostka"][0],
            )
        )
        return state

    def atak_phase(self, state, mapa, user):
        return state

    def get_squad_ruch(self, squad):
        min_ruch = 1000
        for wojownik in squad["jednostki"]:
            if wojownik["ruch"] < min_ruch:
                min_ruch = wojownik["ruch"]
        return min_ruch

    def get_jednostka(self, wojownik):
        return {
            "zdrowie": wojownik["zdrowie"],
            "morale": wojownik["morale"],
            "id": wojownik["id"],
            "kategoria": wojownik["kategoria"],
            "array_pos": 3,
            "ruch": wojownik["ruch"],
        }

    def get_squad(self, user, pos, wojownik):
        info = {}
        info["color"] = user["color"]
        info["owner"] = user["name"]
        info["owner_id"] = user["id"]
        info["pos"] = pos
        info["strategy"] = self.ustawienia["strategy"]
        info["wzmocnienie"] = False
        info["team"] = user["team"]
        info["jednostki"] = []
        jednostka = self.get_jednostka(wojownik)
        info["jednostki"].append(jednostka)
        return info

    def join_squads(self, squad1, squad2):
        for wojownik in squad2["jednostki"]:
            squad1["jednostki"].append(wojownik)

        i = 0
        for wojownik in squad1["jednostki"]:
            wojownik["array_pos"] = i
            i += 1

    def validate_join(self, squad1, squad2):
        if len(squad1["jednostki"] + squad2["jednostki"]) > 7:
            return False
        return True

    def validate_cost(self, user, cost):
        if user["gold"] < cost["gold"]:
            return False
        if user["srebro"] < cost["srebro"]:
            return False
        if user["stal"] < cost["stal"]:
            return False
        if user["food"] < cost["food"]:
            return False
        if user["medale"] < cost["medale"]:
            return False
        return True

    def pay(self, user, cost):
        user["gold"] -= cost["gold"]
        user["srebro"] -= cost["srebro"]
        user["stal"] -= cost["stal"]
        user["food"] -= cost["food"]
        user["medale"] -= cost["medale"]
        return user

from .map1 import mapa

with open("mapa1(30x30).yaml", mode="wt", encoding="utf-8") as f:
    for row in mapa:
        f.write("   - " + str(row) + "\n")

# Plik ze stałymi służącymi do ustawień, będzie ich duża zapewne, a takie rozmieszczenie ułatwi ich edycję
folder_grafiki = "grafika"
# ekran
Width = 1200
Height = 800
srodek = (Width / 2, Height / 2)
Title = "Gra"

FPS = 60

# mapa
Mapa_width = 3416
Mapa_height = 2500

mapa_x_offset = srodek[0]
mapa_y_offset = srodek[1]

plik_mapy = "mapa_test.tmx"

map_original_pos = (0, 0)

# mini_mapa
skala = 10
mini_width = Mapa_width / skala
mini_height = Mapa_height / skala

mini_map_pos = (Width, 0)
minimapa_image = "mapa_test.png"

# tiles
tile_height = 108
tile_width = 112


# mini map rect
mini_map_mouse_rect_width = Width / skala
mini_map_mouse_rect_height = Height / skala

# Plik ze stałymi służącymi do ustawień, będzie ich duża zapewne, a takie rozmieszczenie ułatwi ich edycję
folder_grafiki = "grafika"
# ekran
Width = 1600
Height = 800
srodek = (Width / 2, Height / 2)
Title = "Gra"

FPS = 60

# recruit
pos_rec_x = 6
pos_rec_y = 6
budynek_img = "recruit_test.png"

# mapa
Mapa_width = 3416
Mapa_height = 2457
map_tile_width = 30
map_tile_height = 30

mapa_x_offset = srodek[0]
mapa_y_offset = srodek[1]

mouse_boundry_offset_x = 2
mouse_boundry_offset_y = 2
mouse_border_speed = 20

plik_mapy = "mapa_test.tmx"

map_original_pos = (-728 + srodek[0], -540 + srodek[1])

# mini_mapa
skala = 10
mini_width = Mapa_width / skala
mini_height = Mapa_height / skala

mini_map_pos = (Width, 0)
minimapa_image = "mapa_test.png"

# tiles
tile_height = 108
tile_width = 112

# resource
resource_width = Width
resource_height = 50

resource_pos = (0, 0)
resource_color = (0, 0, 0, 100)
font = "consolas.ttf"
font_size = 32
font_color = "yellow"

# side-menu
menu_width = 300
menu_height = Height
menu_color = (0, 0, 0, 100)
menu_pos = (0, 0 + resource_height)

# mini map rect
mini_map_mouse_rect_width = (Width) / skala
mini_map_mouse_rect_height = (Height) / skala
mini_map_rect_color = "red"

import pygame

def main():
  """
    główna pętla pygame
  """

  pygame.init() #inicjalizacja pygame

  Width, Height = 600, 600
  screen = pygame.display.set_mode((Width, Height)) #okienko
  clock = pygame.time.Clock() #czas
  FPS = 60

  dziala = True
  while dziala:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: #jeżeli nacisnąłeś wyjście z okienka to wychodzisz z pętli, pygame dziala tak ze input użytkownika nie stopuje programu 
        dziala = False

    screen.fill('blue') #wypaełnia screena na niebiesko
    pygame.display.flip() #odświeża display

    clock.tick(FPS) # maks 60 FPS, szybkosc petli bedzie mniej wiecej taka sama dla wszystkich użytkowników nawet tych z wypasionym kompem

  
# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się main()
if __name__ == '__main__':
  main()
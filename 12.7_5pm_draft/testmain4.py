import pygame
from three_ui import Menus
from three_ui import MenuManager
from placeholderplayer import Player
from three_gamelogic import GameLogic
from three_gamelogic import GamePlay

pygame.init()

screen = pygame.display.set_mode((800, 800))

ui = Menus()

game = GameLogic()

gameplay = GamePlay(800, 800, game)

menu = MenuManager(gameplay)
state = "mainmenu"

clock = pygame.time.Clock()
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state = menu.escape_logic(state, event)

    if state is not None and "menu" in state:
        new_state = menu.display_menus(screen, state)
        if new_state == "close":
            run = False
        else:
            state = new_state

    # dummy code until we integrate Kyler's maps and Woorim's character movement
    elif state == "playstate":
        gameplay.update()
        gameplay.draw(screen)

    clock.tick(60)
    pygame.display.update()

pygame.quit()
import pygame
import three_buttons as buttons
from three_savecode import SaveManager
from two_enemy import Enemy

class Menus:

    def __init__(self):
        # loads all images and buttons so they are ready to use
        self.load_images()
        self.create_buttons()

    def load_images(self):
        # loads each image file into a variable
        self.startimage = pygame.image.load('three_start_btn.png').convert_alpha()
        self.exitimage = pygame.image.load('three_exit_btn.png').convert_alpha()
        self.saveimage = pygame.image.load('three_save_btn.png').convert_alpha()
        self.resumeimage = pygame.image.load('three_resume_btn.png').convert_alpha()
        self.save1image = pygame.image.load('three_save1_btn.png').convert_alpha()
        self.save2image = pygame.image.load('three_save2_btn.png').convert_alpha()
        self.newimage = pygame.image.load('three_new_btn.png').convert_alpha()

    def create_buttons(self):
        #creates button class instances for each button, using the button image variables created above
        self.startbtn = buttons.Button(100, 500, self.startimage, 1.5)
        self.exitbtn = buttons.Button(500, 500, self.exitimage, 1.5)
        self.pauseexitbtn = buttons.Button(300, 500, self.exitimage, 1.5)
        self.savebtn = buttons.Button(300, 300, self.saveimage, 1.5)
        self.resumebtn = buttons.Button(260, 100, self.resumeimage, 1.5)
        self.save1btn = buttons.Button(210, 180, self.save1image, 2)
        self.save2btn = buttons.Button(210, 480, self.save2image, 2)
        self.newbtn = buttons.Button(250, 100, self.newimage, 1.5)
        self.load1btn = buttons.Button(250, 300, self.save1image, 1.5)
        self.load2btn = buttons.Button(250, 500, self.save2image, 1.5)


    def main_menu(self, surface):
        # draws a main menu over the whole screen, including title, color, and buttons
        # the button boolean functionality allows if statements to be used with the draw() method
        # returned string values are used later as references to game states
        surface.fill((50, 0, 20))
        self.draw_text(surface, 100, 200, "Rat-a-tat-tat")
        if self.startbtn.draw(surface):
            return "start"
        elif self.exitbtn.draw(surface):
            return "quit"


    def pause_menu(self, surface):
        # draws a pause menu over the screen, including play, save, and exit buttons
        surface.fill((50, 0, 20))
        if self.resumebtn.draw(surface):
            return "play"
        elif self.savebtn.draw(surface):
            return "save"
        elif self.pauseexitbtn.draw(surface):
            return "quit"


    def save_menu(self, surface):
        # draws a save menu over the screen, including a Save File 1 and Save File 2 button
        surface.fill((50, 0, 20))
        if self.save1btn.draw(surface):
            return "save1"
        elif self.save2btn.draw(surface):
            return "save2"

    def start_menu(self, surface):
        # draws a start menu over the screen, including New Game, Save File 1, and Save File 2 buttons
        surface.fill((50, 0, 20))
        if self.newbtn.draw(surface):
            return "play"
        elif self.load1btn.draw(surface):
            return "play1"
        elif self.load2btn.draw(surface):
            return "play2"

    def draw_text(self, surface, x, y, text, font=None, color=(255, 255, 255)):
        # this is added arbitrarily into this class, serves only once to draw the title on the main menu
        if font == None:
            font = pygame.font.SysFont(None, 150)
        printed_text = font.render(text, True, color)
        surface.blit(printed_text, (x, y))

class MenuManager:

    def __init__(self, gameplay):
        # creates an instance of the Menus class and SaveManager class, uses gameplay to allow
        # integration with the GameLogic class in the main file
        self.ui = Menus()
        self.saves = SaveManager()
        self.gameplay = gameplay

    def display_menus(self, surface, state):
        # contains logic for all menus. For each button in each menu, will return a game state
        if state == "mainmenu":
            result = self.ui.main_menu(surface)
            if result is None:
                return state
            if result == "start":
                state = "startmenu"
            elif result == "quit":
                state = "close"
            return state

        elif state == "pausemenu":
            result = self.ui.pause_menu(surface)
            if result is None:
                return state
            if result == "play":
                state = "playstate"
            elif result == "save":
                state = "savemenu"
            elif result == "quit":
                state = "mainmenu"
            return state

        elif state == "savemenu":
            # extra code here will record current game data and save it to the save file
            # chosen by the user. Actual save functionality is in the savecode file.
            result = self.ui.save_menu(surface)
            if result is None:
                return state
            gamedata = {
                "used" : True,
                "player_x": self.gameplay.player.x,
                "player_y": self.gameplay.player.y,
                "current_map": self.gameplay.gamedata.current_map,
                "health": self.gameplay.player.health,
                "score": self.gameplay.gamedata.score,
                "enemies": [
                    {
                        "x": enemy.x,
                        "y": enemy.y,
                        "health": enemy.health,
                        "timer": enemy.timer,
                        "pause_time": enemy.pause_time,
                    }
                    for enemy in self.gameplay.enemies
                ]
            }
            if result == "save1":
                self.saves.save("save1", gamedata)
                state = "playstate"
            elif result == "save2":
                self.saves.save("save2", gamedata)
                state = "playstate"
            return state

        elif state == "startmenu":
            # similar to the save menu before, this loads in data from the save file chosen by the user
            # and starts the gameplay with that game data
            result = self.ui.start_menu(surface)

            if result in ('play1', 'play2'):
                if result == "play1":
                    slot = "save1"
                else:
                    slot = "save2"
                gamedata = self.saves.load(slot)

                if gamedata["used"] is False:
                    self.gameplay.reset()
                    return "playstate"

                # takes data from save files and assigns it to current gameplay
                self.gameplay.player.x = gamedata["player_x"]
                self.gameplay.player.y = gamedata["player_y"]
                self.gameplay.player.health = gamedata["health"]
                self.gameplay.gamedata.current_map = gamedata["current_map"]
                self.gameplay.gamedata.score = gamedata["score"]

                self.gameplay.enemies = []
                for ed in gamedata["enemies"]:
                    enemy = Enemy(ed["x"], ed["y"])
                    enemy.health = ed["health"]
                    enemy.timer = ed["timer"]
                    enemy.pause_time = ed["pause_time"]
                    self.gameplay.enemies.append(enemy)

                self.gameplay.player_bullets.clear()
                self.gameplay.enemy_bullets.clear()

                state = "playstate"
            elif result == "play":
                self.gameplay.reset()
                state = "playstate"
            return state

    def escape_logic(self, state, event):
        # allows the escape key to be used both as a pause button during gameplay
        # and as a "back" button in nested menus
        if event.key == pygame.K_ESCAPE and state == "playstate":
            state = "pausemenu"
        elif event.key == pygame.K_ESCAPE and state == "savemenu":
            state = "pausemenu"
        elif event.key == pygame.K_ESCAPE and state == "pausemenu":
            state = "playstate"
        elif event.key == pygame.K_ESCAPE and state == "startmenu":
            state = "mainmenu"
        return state
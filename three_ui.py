# this class also contains the draw text method
import pygame
import three_buttons as buttons

class Menus:

    def __init__(self):
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.startimage = pygame.image.load('three_start_btn.png').convert_alpha()
        self.exitimage = pygame.image.load('three_exit_btn.png').convert_alpha()
        self.saveimage = pygame.image.load('three_save_btn.png').convert_alpha()
        self.resumeimage = pygame.image.load('three_resume_btn.png').convert_alpha()
        self.save1image = pygame.image.load('three_save1_btn.png').convert_alpha()
        self.save2image = pygame.image.load('three_save2_btn.png').convert_alpha()
        self.newimage = pygame.image.load('three_new_btn.png').convert_alpha()

    def create_buttons(self):
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
        surface.fill((50, 0, 20))
        self.draw_text(surface, 100, 200, "Rat-a-tat-tat")
        if self.startbtn.draw(surface):
            return "start"
        elif self.exitbtn.draw(surface):
            return "quit"


    def pause_menu(self, surface):
        surface.fill((50, 0, 20))
        if self.resumebtn.draw(surface):
            return "play"
        elif self.savebtn.draw(surface):
            return "save"
        elif self.pauseexitbtn.draw(surface):
            return "quit"


    def save_menu(self, surface):
        surface.fill((50, 0, 20))
        if self.save1btn.draw(surface):
            return "save1"
        elif self.save2btn.draw(surface):
            return "save2"

    def start_menu(self, surface):
        surface.fill((50, 0, 20))
        if self.newbtn.draw(surface):
            return "play"
        elif self.load1btn.draw(surface):
            return "play1"
        elif self.load2btn.draw(surface):
            return "play2"

    def draw_text(self, surface, x, y, text, font=None, color=(255, 255, 255)):
        if font == None:
            font = pygame.font.SysFont(None, 150)
        printed_text = font.render(text, True, color)
        surface.blit(printed_text, (x, y))
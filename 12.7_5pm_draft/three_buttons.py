import pygame

class Button:
    # initialize the class with a position
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        button_hover = self.rect.collidepoint(pos)

        if button_hover and left_click and not self.clicked:
            self.clicked = True
        if self.clicked and not left_click:
            if button_hover:
                action = True
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, self.rect.topleft)

        return action
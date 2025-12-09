import pygame
class Button:

    def __init__(self, x, y, image, scale):
        # uses built-in get_width and get_height functions to automatically create accurate
        # rectangle layers over each button
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # clicked flag is used later for checking if the left mouse button has been
        # both clicked down and released
        self.clicked = False

    def draw(self, surface): #draws buttons, checks if button has been clicked
        action = False
        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        # check if cursor is over the button
        button_hover = self.rect.collidepoint(pos)

        # this checks if left button has been clicked down, then released
        if button_hover and left_click and not self.clicked:
            self.clicked = True
        if self.clicked and not left_click:
            if button_hover:
                action = True
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, self.rect.topleft)

        # returning an action lets a user use draw in an if statement to check clicked condition
        return action
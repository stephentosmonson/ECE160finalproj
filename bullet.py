import pygame

BULLET_SIZE = 6


class Bullet:
    def __init__(self, x, y, vx, vy, color, can_hit=True):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.can_hit = can_hit  # used in your main.py

        # for collisions & drawing
        self.rect = pygame.Rect(int(self.x), int(self.y),
                                BULLET_SIZE, BULLET_SIZE)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def get_rect(self):
        return self.rect

    def off_screen(self, width, height):
        return (
            self.x < -BULLET_SIZE or self.x > width + BULLET_SIZE or
            self.y < -BULLET_SIZE or self.y > height + BULLET_SIZE
        )

import pygame
import math
from two_bullet import Bullet, BULLET_SIZE


class Player:
    def __init__(self, x, y, size=20, speed=4, health=5,
                 shoot_cooldown=20, attack_range=250):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.health = health

        # shooting behavior
        self.shoot_cooldown = shoot_cooldown  # frames between shots
        self.shoot_timer = 0                  # frames since last shot
        self.attack_range = attack_range      # auto-aim range

        # facing direction
        self.facing_dx = 0
        self.facing_dy = -1  # start facing up

    def handle_input(self, WIDTH, HEIGHT):
        keys = pygame.key.get_pressed()

        move_dx = 0
        move_dy = 0

        if keys[pygame.K_w]:
            move_dy -= 1
        if keys[pygame.K_s]:
            move_dy += 1
        if keys[pygame.K_a]:
            move_dx -= 1
        if keys[pygame.K_d]:
            move_dx += 1

        if move_dx != 0 or move_dy != 0:
            length = math.hypot(move_dx, move_dy)
            move_dx /= length
            move_dy /= length

            self.x += move_dx * self.speed
            self.y += move_dy * self.speed

            # update facing to last movement direction
            self.facing_dx = move_dx
            self.facing_dy = move_dy

        # keep player on screen
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.get_rect())

    def auto_shoot(self, enemies, shooting):
        """
        enemies: list of Enemy objects
        shooting: bool -> True if shoot button is held
        returns: Bullet or None
        """
        # cooldown
        if self.shoot_timer < self.shoot_cooldown:
            self.shoot_timer += 1
            return None

        if not shooting:
            return None

        px = self.x + self.size / 2
        py = self.y + self.size / 2

        # find closest enemy within attack_range
        target = None
        min_dist_sq = self.attack_range * self.attack_range

        for enemy in enemies:
            ex = enemy.x + enemy.size / 2
            ey = enemy.y + enemy.size / 2
            dx = ex - px
            dy = ey - py
            dist_sq = dx * dx + dy * dy

            if dist_sq <= min_dist_sq:
                min_dist_sq = dist_sq
                target = enemy

        bullet_speed = 7

        if target is not None:
            # enemy in range → auto aim + can_hit=True
            ex = target.x + target.size / 2
            ey = target.y + target.size / 2
            dx = ex - px
            dy = ey - py
            dist = math.hypot(dx, dy)
            if dist == 0:
                return None

            vx = bullet_speed * dx / dist
            vy = bullet_speed * dy / dist
            can_hit = True
        else:
            # no enemy in range → shoot in facing direction, can_hit=False (dummy bullet)
            if self.facing_dx == 0 and self.facing_dy == 0:
                self.facing_dx = 0
                self.facing_dy = -1

            vx = bullet_speed * self.facing_dx
            vy = bullet_speed * self.facing_dy
            can_hit = False

        # reset cooldown
        self.shoot_timer = 0

        bx = px - BULLET_SIZE / 2
        by = py - BULLET_SIZE / 2
        return Bullet(bx, by, vx, vy, (255, 0, 0), can_hit=can_hit)

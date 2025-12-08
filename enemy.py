import pygame
import random
import math
from bullet import Bullet

ENEMY_SIZE = 20


class Enemy:
    def __init__(self, x, y, speed=1, size=ENEMY_SIZE,
                 shoot_cooldown=100, health=3):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.shoot_cooldown = shoot_cooldown
        self.timer = random.randint(0, shoot_cooldown)

        self.health = health
        self.max_health = health

        # stop when shooting
        self.pause_time = 0
        self.pause_duration = 20  # enemy will not move for 20 frames after shooting

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.get_rect())

    def update(self, player, enemies, enemy_bullets):
        # If paused from shooting, do not move
        if self.pause_time > 0:
            self.pause_time -= 1
        else:
            # normal movement toward player
            old_x, old_y = self.x, self.y

            if self.x < player.x:
                self.x += self.speed
            elif self.x > player.x:
                self.x -= self.speed

            if self.y < player.y:
                self.y += self.speed
            elif self.y > player.y:
                self.y -= self.speed

            # prevent overlapping
            my_rect = self.get_rect()
            for other in enemies:
                if other is self:
                    continue
                if my_rect.colliderect(other.get_rect()):
                    self.x, self.y = old_x, old_y
                    break

        # avoid overlapping other enemies
        my_rect = self.get_rect()
        for other in enemies:
            if other is self:
                continue
            if my_rect.colliderect(other.get_rect()):
                self.x, self.y = old_x, old_y
                my_rect = self.get_rect()
                break

        # shooting timer
        self.timer += 1
        if self.timer >= self.shoot_cooldown:
            self.timer = 0
            bullet = self.shoot_at_player(player)
            if bullet:
                enemy_bullets.append(bullet)
                self.pause_time = self.pause_duration

    def shoot_at_player(self, player):
        bullet_speed = 5
        ex = self.x + self.size / 2
        ey = self.y + self.size / 2
        px = player.x + player.size / 2
        py = player.y + player.size / 2

        dx = px - ex
        dy = py - ey
        dist = math.hypot(dx, dy)
        if dist == 0:
            return None

        vx = bullet_speed * dx / dist
        vy = bullet_speed * dy / dist

        # enemy bullets always can hit
        return Bullet(ex, ey, vx, vy, (255, 255, 0), can_hit=True)

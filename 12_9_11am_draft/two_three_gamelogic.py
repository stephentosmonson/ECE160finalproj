import random
import pygame
from two_player import Player
from two_enemy import Enemy, ENEMY_SIZE

class GameLogic:
    def __init__(self):
        self.current_map = 1
        self.health = 100
        self.score = 0

class GamePlay:
    def __init__(self, width, height, gamedata):
        self.WIDTH = width
        self.HEIGHT = height

        self.player = Player(width // 2, height // 2)
        self.enemies = self.spawn_enemies_away(self.player, random.randint(5, 10))
        self.player_bullets = []
        self.enemy_bullets = []

        self.font = pygame.font.SysFont(None, 36)

        self.BLACK = (30, 30, 30)
        self.WHITE = (255, 255, 255)

        self.gamedata = gamedata

    # CODE FROM WOORIM, def spawn_enemies_away is a direct copy from his main
    # file, used here in a class
    def spawn_enemies_away(self, player, count, min_dist=250):
        enemies = []
        for _ in range(count):
            while True:
                x = random.randint(0, self.WIDTH - ENEMY_SIZE)
                y = random.randint(0, self.HEIGHT - ENEMY_SIZE)

                ex = x + ENEMY_SIZE / 2
                ey = y + ENEMY_SIZE / 2
                px = player.x + player.size / 2
                py = player.y + player.size / 2

                dx = ex - px
                dy = ey - py

                if dx * dx + dy * dy >= min_dist * min_dist:
                    enemies.append(Enemy(x, y))
                    break

        return enemies

    # CODE FROM WOORIM, this is his main game loop used here as
    # the update() method
    def update(self):

        self.player.handle_input(self.WIDTH, self.HEIGHT)


        keys = pygame.key.get_pressed()
        shooting = keys[pygame.K_SPACE]
        new_bullet = self.player.auto_shoot(self.enemies, shooting)
        if new_bullet:
            self.player_bullets.append(new_bullet)


        for enemy in self.enemies:
            enemy.update(self.player, self.enemies, self.enemy_bullets)


        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.off_screen(self.WIDTH, self.HEIGHT):
                self.player_bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.off_screen(self.WIDTH, self.HEIGHT):
                self.enemy_bullets.remove(bullet)


        for enemy in self.enemies[:]:
            for bullet in self.player_bullets[:]:
                if not bullet.can_hit:
                    continue
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    enemy.health -= 1
                    self.player_bullets.remove(bullet)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                    break


        for bullet in self.enemy_bullets[:]:
            if bullet.get_rect().colliderect(self.player.get_rect()):
                self.player.health -= 1
                self.enemy_bullets.remove(bullet)
                break


        for enemy in self.enemies:
            if enemy.get_rect().colliderect(self.player.get_rect()):
                self.player.health -= 1
                break

    def draw(self, screen):

        screen.fill(self.BLACK)


        self.player.draw(screen)


        for enemy in self.enemies:
            enemy.draw(screen)


        for b in self.player_bullets:
            b.draw(screen)

        for b in self.enemy_bullets:
            b.draw(screen)


        health_surf = self.font.render(f"Health: {self.player.health}", True, self.WHITE)
        screen.blit(health_surf, (10, 10))

    def reset(self):

        self.player.x = self.WIDTH // 2
        self.player.y = self.HEIGHT // 2

        self.player.health = 5  # or whatever default health is
        self.player.shoot_timer = 0


        self.enemies = self.spawn_enemies_away(self.player, random.randint(5, 10))


        self.player_bullets.clear()
        self.enemy_bullets.clear()


        self.gamedata.current_map = 1
        self.gamedata.score = 0


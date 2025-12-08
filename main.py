import pygame
import sys
import random

from player import Player
from enemy import Enemy, ENEMY_SIZE

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)


def spawn_enemies_away(player, count, min_dist=250):
    enemies = []
    for _ in range(count):
        while True:
            x = random.randint(0, WIDTH - ENEMY_SIZE)
            y = random.randint(0, HEIGHT - ENEMY_SIZE)

            ex = x + ENEMY_SIZE / 2
            ey = y + ENEMY_SIZE / 2
            px = player.x + player.size / 2
            py = player.y + player.size / 2

            dx = ex - px
            dy = ey - py

            # ensure enemy spawns far away from player
            if dx * dx + dy * dy >= min_dist * min_dist:
                enemies.append(Enemy(x, y))
                break
    return enemies


def main():
    player = Player(WIDTH // 2, HEIGHT // 2)
    enemies = spawn_enemies_away(player, random.randint(5, 10))

    player_bullets = []
    enemy_bullets = []

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player movement
        player.handle_input(WIDTH, HEIGHT)

        # Auto shooting 
        keys = pygame.key.get_pressed()
        shooting = keys[pygame.K_SPACE]  # hold space to fire
        new_bullet = player.auto_shoot(enemies, shooting)
        if new_bullet:
            player_bullets.append(new_bullet)

        # Update enemies
        for enemy in enemies:
            enemy.update(player, enemies, enemy_bullets)

        # Update player bullets
        for bullet in player_bullets[:]:
            bullet.update()
            if bullet.off_screen(WIDTH, HEIGHT):
                player_bullets.remove(bullet)

        # Update enemy bullets
        for bullet in enemy_bullets[:]:
            bullet.update()
            if bullet.off_screen(WIDTH, HEIGHT):
                enemy_bullets.remove(bullet)

        # COLLISION: player bullets → enemies
        for enemy in enemies[:]:
            enemy_rect = enemy.get_rect()
            for bullet in player_bullets[:]:
                # only bullets with can_hit=True can damage enemies
                if not getattr(bullet, "can_hit", True):
                    continue

                if bullet.get_rect().colliderect(enemy_rect):
                    enemy.health -= 1      # basic damage
                    player_bullets.remove(bullet)

                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    break

        # COLLISION: enemy bullets → player
        player_rect = player.get_rect()
        for bullet in enemy_bullets[:]:
            if bullet.get_rect().colliderect(player_rect):
                player.health -= 1
                enemy_bullets.remove(bullet)
                if player.health <= 0:
                    print("GAME OVER")
                    running = False
                break

        # COLLISION: enemies touching the player (melee)
        for enemy in enemies:
            if enemy.get_rect().colliderect(player_rect):
                player.health -= 1
                # push enemy away to avoid instant drain
                enemy.x += random.choice([-50, 50])
                enemy.y += random.choice([-50, 50])
                if player.health <= 0:
                    print("GAME OVER")
                    running = False
                break

        # draw everything
        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        for b in player_bullets:
            b.draw(screen)

        for b in enemy_bullets:
            b.draw(screen)

        health = font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(health, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

import pygame
from pygame.locals import *
import pickle
pygame.init()
from os import path
from two_enemy import Enemy, ENEMY_SIZE

screen_width = 800
screen_height = 800


class Back_ground():
    def __init__(self,x,y):
        img = pygame.image.load('img/Bg.png')
        self.image = pygame.transform.scale(img,(screen_width,screen_height))
        screen.blit(self.image)
    def draw(self):
        screen.blit(self.image)
        
		
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("collision test")

tile_size = 40

#images load
#egg_img = pygame.image.load('img/place_floor.png')
#bg_img = pygame.image.load('img/place_bg2.png')

#def draw_grid():
    #for lin in range(0,20):
        #pygame.draw.line(screen,(255,255,255), (0,line * tile_size), (screenwith, line)

#the player image and functions
class Player():
    def __init__(self,x,y):
        img = pygame.image.load('img/place_player.png')
        self.image = pygame.transform.scale(img,(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width
        self.hight = self.image.get_height

    def update(self):

        dx = 0
        dy = 0
        #get key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            dy -= 1
        if key[pygame.K_DOWN]:
            dy += 1
        if key[pygame.K_LEFT]:
            dx -= 1
        if key[pygame.K_RIGHT]:
            dx += 1
        
        #for tile in map.tile_list:
            #if tile[1].colliderect(self.rect.x + dx, self.rect.y , self.width, self.hight):
                #dx = 0

            #collision in y
            #if tile [1].colliderect(self.rect.x,self.rect.y + dy, self.width, self.hight):
                #dy = 0


        self.rect.x += dx
        self.rect.y += dy


        #draws player on screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen,(255,255,255),self.rect,1)


                    



class Map():
    def __init__(self,data):
        self.tile_list =[]
        #images/assets
        wall = pygame.image.load('img/wall_tile.png')
        pipe_side = pygame.image.load('img/pipe_side.png')
        pipe_down = pygame.image.load('img/pipe_down.png')
        #exit = pygame.image.load('img/ex.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame .transform.scale(wall, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img , img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame .transform.scale(pipe_side, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img , img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame .transform.scale(pipe_down, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img , img_rect)
                    self.tile_list.append(tile)
                
                if tile == 4:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(enemy)
                    
                if tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            #pygame.draw.rect(screen, (255,255,255), tile[1], 1)


#class Enemy

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit_tile.png')
        self.image = pygame .transform.scale(img, (tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

exit_group = pygame.sprite.Group()

#enemys
enemy_group = pygame.sprite.Group()


map_data = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,1],
[1,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

player = Player(200,200)

bg = Back_ground(0,0)


#if path.exists(f"map1_data"):
    #pickle_in = open('map1_data','rb')
    #map_data = pickle.load(pickle_in)
map = Map(map_data)

run = True
while run:

    

    #screen.blit(bg_img, (0, 0))
    #screen.blit(egg_img, (10, 10))

    map.draw()

    exit_group.draw(screen)

    enemy_group.draw(screen)

    player.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()
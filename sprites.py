# This file was created by Tyler Reed

# import moduels
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import time

# create a player class
# Our player charcter


class Player(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0     
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.status = ""
        self.hitpoints = 100
        # Cozort Code
        self.weapon_drawn = False
        self.weapon = ""
    
    def get_mouse(self):
        if pg.mouse.get_rel()[0]:
            self.weapon_drawn = False
        if pg.mouse.get_pressed()[0]:
            if not self.weapon_drawn:
                self.weapon_drawn = True
        

    # def move(self, dx= 0, dy = 0):
    #     self.x += dx
    #     self.y += dy

    def get_keys(self): 
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_a]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_a]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_a]:
            self.vy= PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071 
    def collide_with_walls(self, dir):
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits: 
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits: 
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.width
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                self.rect.y = self.y

    def collide_with_obj(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "coin":
            self.image.fill(BLUE)

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x') 
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_obj(self.game.coins, True, "coin")

# Sword Class 
# Cozort Code
class Sword(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dir):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.dir = dir
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("I created a sword")
    def collide_with_group(self, group, kill):
                if hits[0].hitpoints -= 1
    
    def update(self):
        self.pos = self.game.player.pos
        self.collide_with_group(self.game.mobs, False)
        if not self.game.player.weapon_drawn:
            self.kill()
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
        def update(self):
            if self.hitpoints < 1:
                self.kill()
# create a wall class
# a colladiable object
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()     
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0     
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    

def collide_with_obj(self, group, kill, desc):
    hits = pg.sprite.spritecollide(self, group, kill)
    if hits and desc == "coin":
        self.image.fill(YELLOW)

def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
# def spawn_boss():

#     if self.moneybag >= 1:
#         boss = 2

def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x') 
        self.collect_coins('x')
        self.rect.y = self.y
        self.collide_with_Player('y')
        self.collide_with_obj(self.game.coins, True, "coin")
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height

class enemy(Sprite):
    # enemy size/summon
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect() 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = ENEMY_SPEED
        self.vy = ENEMY_SPEED
        self.vx *= 0.7071
        self.vy *= 0.7071 
        self.hitpoints = 10
        
    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x') 
        self.rect.y = self.y
        self.collide_with_walls('y')
    
    def collide_with_walls(self, dir):
            #wall collsion w/ enemy
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.enemy, False)
                if hits: 
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.enemy, False)
                if hits: 
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.width
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                self.rect.y = self.y


class boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(RED)
        self.rect = self.image.get_rect() 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = BOSS_SPEED
        self.vy = BOSS_SPEED
        self.vx *= 0.7071
        self.vy *= 0.7071 
        
    def collide_with_walls(self, dir):
            #wall collsion w/ enemy
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.boss, False)
                if hits: 
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.boss, False)
                if hits: 
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.width
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                self.rect.y = self.y

            
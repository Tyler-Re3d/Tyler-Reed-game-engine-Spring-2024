# This file was created by Tyler Reed

# import moduels
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import time
from math import floor

vec = pg.math.Vector2

# create a player class
# Our player charcter
# Cozort Code
# Cooldown class (set up time)
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
        # the time and how it works
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
        # resets time
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
# me / player character
class Player(Sprite): 
    def __init__(self, game, x, y):
        self.hit_cooldown = Cooldown()
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
        self.hitpoints = 3
        # Cozort Code
        self.sword = None
        
    # weapon getting
    def get_mouse(self):
        if pg.mouse.get_rel()[0]:
            self.weapon_drawn = False
        if pg.mouse.get_pressed()[0]:
            if not self.weapon_drawn:
                self.weapon_drawn = True
        

    # def move(self, dx= 0, dy = 0):
    #     self.x += dx
    #     self.y += dy
# the keys you use
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
            # slide collision
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
# kills coins
    def collide_with_obj(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "coin":
            self.image.fill(BLUE)
        

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x') 
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_obj(self.game.coins, True, "coin")
# AI Code
        # Checks for collisions with enemies
        hits_enemies = pg.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits_enemies:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1  # Reduce player's hitpoints by 1 when hit by enemy
                self.hit_cooldown.event_reset()
# AI Code
        # Check for collisions with boss
        hits_boss = pg.sprite.spritecollide(self, self.game.boss, False)
        for boss in hits_boss:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1  # Reduce player's hitpoints by 1 if hit by boss
                self.hit_cooldown.event_reset()
# AI Code
            # Checks for sword collisions with enemies and da boss
        if self.sword:
            hits_enemies = pg.sprite.spritecollide(self.sword, self.game.enemy, True)
            hits_boss = pg.sprite.spritecollide(self.sword, self.game.boss, True)

            # Enemy goes byebye (dies)
            for enemy in hits_enemies:
                pass  
            # Boss goes byebye (dies)
            for boss in hits_boss:
                pass  
# AI Code
        # Sword handling and how you use sword/appears on screen
        if pg.key.get_pressed()[pg.K_SPACE] and not self.sword:
            self.sword = Sword(self.game, self)
            self.game.all_sprites.add(self.sword)
# AI Code
        # Updates the sword if it is on screen
        if self.sword:
            self.sword.update()
            # If the sword is no longer on screen it goes bye bye
            if not self.sword.alive():
                self.sword = None
        

# Ai code
                # Creates Sword class so sword appears on screen and does its job
class Sword(Sprite):
    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.player = player
        self.image = pg.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
         # AI Code 
         # Calculates the position of the sword based from the player's center so it can spawn
        offset = pg.math.Vector2(30, 0)  
        self.rect.center = player.rect.center + offset

        self.duration = 0.5  # Duration the sword stays active on da screen
        self.timer = 0
# AI Code 
    def update(self):
        # makes its time relative to delta time
        self.timer += self.game.dt
        if self.timer >= self.duration:
            self.kill()  # Removes the sword after the time duration
        # Updates sword position with the player
        offset = pg.math.Vector2(30, 0)  
        self.rect.center = self.player.rect.center + offset


        # Checks for collisions with da enemies and with da bosses
        hits = pg.sprite.spritecollide(self, self.game.enemies, self.game.boss, False)
        for enemy in hits:
            enemy.hitpoints -= 1  # Reduce enemy/boss hitpoints by 1 when hit by sword
        for boss in hits:
            boss.hitpoints -= 1   # reduces boss hitpoints when hit by sword by 1
       



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

# money
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

    
# when collides
def collide_with_obj(self, group, kill, desc):
    hits = pg.sprite.spritecollide(self, group, kill)
    if hits and desc == "coin":
        self.image.fill(YELLOW)


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
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = ENEMY_SPEED  
        self.hitpoints = 3
 # AI Code       
    def update(self):
         # Calculates direction vector to player and makes it follow player
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalizes the direction vector and scales by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
# dies when hitpoints run out
        if self.hitpoints <= 0:
            self.kill()

    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for wall in hits:
                if self.vx > 0:
                    self.rect.right = wall.rect.left
                if self.vx < 0:
                    self.rect.left = wall.rect.right
                self.vx *= -1  # Reverse direction

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for wall in hits:
                if self.vy > 0:
                    self.rect.bottom = wall.rect.top
                if self.vy < 0:
                    self.rect.top = wall.rect.bottom
                self.vy *= -1  # Reverse direction

# the big boi (bigger enemy) and faster
class boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = BOSS_SPEED  
        self.hitpoints = 10
        
# AI Code
    def update(self):
        # Calculates direction vector to player and makes it follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalizes the direction vector and scales the boss by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

# multiplies velocity by delta time
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # dies when hitpoints are gone
        if self.hitpoints <= 0:
            self.kill()

        # Allows Collision with wall
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for wall in hits:
                if self.vx > 0:
                    self.rect.right = wall.rect.left
                if self.vx < 0:
                    self.rect.left = wall.rect.right
                self.vx *= -1  

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for wall in hits:
                if self.vy > 0:
                    self.rect.bottom = wall.rect.top
                if self.vy < 0:
                    self.rect.top = wall.rect.bottom
                self.vy *= -1  
            
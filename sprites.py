# This file was created by Tyler Reed

# import moduels
import pygame as pg
from os import path
from pygame.sprite import Sprite
from settings import *
import time
from random import randint
import random
from math import floor
SPRITESHEET = "theBell.png"

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

vec = pg.math.Vector2

# create a player class
# Our player charcter
# Cozort Code

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        # image = pg.transform.scale(image, (width * 4, height * 4))
        return image


# Cooldown class (set up time)
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
        #must use ticking to count up or down
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
        self.vx, self.vy = 0, 0     
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 500
        # Cozort Code
        self.sword = None
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.jumping = False
        self.walking = False
        
    # weapon getting
    def get_mouse(self):
        if pg.mouse.get_rel()[0]:
            self.weapon_drawn = False
        if pg.mouse.get_pressed()[0]:
            if not self.weapon_drawn:
                self.weapon_drawn = True

# the keys you use
    def get_keys(self): 
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
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
        
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        self.animate()
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
        hits_enemy= pg.sprite.spritecollide(self, self.game.enemy, False)
        for enemy in hits_enemy:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 0.1  # Reduce player's hitpoints by 1 when hit by enemy
                self.hit_cooldown.event_reset()
# AI Code
        # Check for collisions with bosses
        hits_boss = pg.sprite.spritecollide(self, self.game.boss, False)
        for boss in hits_boss:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1  # Reduce player's hitpoints by 1 if hit by boss
                self.hit_cooldown.event_reset()
                
        hits_Kaido = pg.sprite.spritecollide(self, self.game.kaido, False)
        for Kaido in hits_Kaido:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1  # Reduce player's hitpoints by 1 if hit by boss
                self.hit_cooldown.event_reset()

        hits_Kb = pg.sprite.spritecollide(self, self.game.kb, False)
        for Kb in hits_Kb:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1
                self.hit_cooldown.event_reset()
        
        hits_Bigmom = pg.sprite.spritecollide(self, self.game.bigmom, False)
        for Bigmom in hits_Bigmom:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1  # Reduce player's hitpoints by 1 if hit by boss
                self.hit_cooldown.event_reset()

        hits_Buggy = pg.sprite.spritecollide(self, self.game.buggy, False)
        for Buggy in hits_Buggy:
            if self.hit_cooldown.countdown(1):
                self.hitpoints -= 1  # Reduce player's hitpoints by 1 if hit by boss
                self.hit_cooldown.event_reset()

        hits_Shanks = pg.sprite.spritecollide(self, self.game.shanks, False)
        for Shanks in hits_Shanks:
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
        
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
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
        self.timer += self.game.dt
        if self.timer >= self.duration:
            self.kill()
        offset = pg.math.Vector2(30, 0)
        self.rect.center = self.player.rect.center + offset

        # Check for collisions with enemies and bosses
        hits_enemies = pg.sprite.spritecollide(self, self.game.enemy, False)
        for enemy in hits_enemies:
            enemy.hitpoints -= 1
            self.game.enemy_kills += 1
            if enemy.hitpoints <= 0:
                enemy.kill()
        hits_boss = pg.sprite.spritecollide(self, self.game.boss, False)
        for boss in hits_boss:
            boss.hitpoints -= 1
            if boss.hitpoints <= 0:
                boss.kill()
        hits_kaido = pg.sprite.spritecollide(self, self.game.kaido, False)
        for kaido in hits_kaido:
            kaido.hitpoints -= 1
            if kaido.hitpoints <= 0:
                print("mmmm")
                kaido.spawn_enemies(1)
                kaido.kill()
                # Adrian Code;Spawn Kaido B after death
                kaido.spawn_Kb()
                self.kill()
        hits_kb = pg.sprite.spritecollide(self, self.game.kb, False)
        for kb in hits_kb:
            kb.hitpoints -= 1
            kb.spawn_enemies(1)
            kb.kill()
            self.kill()
        hits_buggy = pg.sprite.spritecollide(self, self.game.buggy, False)
        for buggy in hits_buggy:
            buggy.hitpoints -= 1
            if buggy.hitpoints <= 0:
                buggy.spawn_enemies(1)
                buggy.kill()
                self.kill()
        hits_bigmom = pg.sprite.spritecollide(self, self.game.bigmom, False)
        for bigmom in hits_bigmom:
            bigmom.hitpoints -= 1
            if bigmom.hitpoints <= 0:
                bigmom.spawn_enemies(1)
                bigmom.kill()
                self.kill()
        hits_shanks = pg.sprite.spritecollide(self, self.game.shanks, False)
        for shanks in hits_shanks:
            shanks.hitpoints -= 1
            if shanks.hitpoints <= 0:
                shanks.spawn_enemies(1)
                shanks.kill()
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
        hits[0].kill()


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
    def __init__(self, game, x, y, WIDTH, HEIGHT):
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
        self.spawn(WIDTH, HEIGHT)

    def spawn(self, WIDTH, HEIGHT):
        # Set initial position to a random location within the game area
        self.rect.x = random.randint(0, WIDTH - TILESIZE)
        self.rect.y = random.randint(0, HEIGHT - TILESIZE)
        # Ensure enemy does not spawn on top of player
        while self.game.player and self.rect.colliderect(self.game.player.rect):
            self.rect.x = random.randint(0, WIDTH - TILESIZE)
            self.rect.y = random.randint(0, HEIGHT - TILESIZE)


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
            

class Kaido(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.kaido
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(DARKBLUE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = KAIDO_SPEED  
        self.hitpoints = 500
        
# AI Code
    def update(self):
        # Calculate direction vector to player and make Bigmom follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalize the direction vector and scale the boss by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

        # Multiply velocity by delta time 
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
        # Ai Code
        # checks if Kaido has been hit by sword
        sword_hit = pg.sprite.spritecollideany(self, self.game.sword)
        if sword_hit:
            print("hits")
            self.hitpoints -= 1  # When sword hits Reduces da hitpoints
            sword_hit.kill()  # Remove the sword
            if self.hitpoints <= 0:
                print("Kaido ded, spawning K2")
                self.spawn_enemies(1)  # Spawn da enemies if hitpoints are gone
                self.spawn_Kb()
                self.kill()  # Kills Kaido if hitpoints = 0
# Ai Code spawns the enemy randomly
    def spawn_enemies(self, num_enemies):
        print("Spawning enemies")
        for _ in range(num_enemies): #da number of enemies
            col = random.randint(0, len(self.game.map_data[0]) - 1)  # Spawn at Random column
            row = random.randint(0, len(self.game.map_data) - 1)     # Spawn at Random row
            if self.game.map_data[row][col] == '.':
                enemy(self.game, col, row, self.game.screen.get_width(), self.game.screen.get_height())
    
    def spawn_Kb(self):
        print("Spawning KB")
        for _ in range(1): # we only spawn 1 Kb
            print("x")
            col = random.randint(0, len(self.game.map_data[0]) - 1)  # Spawn at Random column
            row = random.randint(0, len(self.game.map_data) - 1)     # Spawn at Random row
            if self.game.map_data[row][col] == '.':
                Kb(self.game, col, row)

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
# Stands for Kaido B; Kaido's second phase
class Kb(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.kb
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(INDIGO)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = K2_SPEED  
        self.hitpoints = 1000
        
# AI Code
    def update(self):
        # Calculate direction vector to player and make KB follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalize the direction vector and scale the boss by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

        # Multiply velocity by delta time 
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
        # Ai Code
        # checks if Kb has been hit by sword
        sword_hit = pg.sprite.spritecollideany(self, self.game.sword)
        if sword_hit:
            self.hitpoints -= 1  # When sword hits Reduces da hitpoints
            sword_hit.kill()  # Remove the sword
            if self.hitpoints <= 0:
                self.kill()  # Kills Kaido B if hitpoints = 0
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

    def spawn_enemies(self, num_enemies):
        print("Spawning enemies")
        for _ in range(num_enemies): #da number of enemies
            col = random.randint(0, len(self.game.map_data[0]) - 1)  # Spawn at Random column
            row = random.randint(0, len(self.game.map_data) - 1)     # Spawn at Random row
            if self.game.map_data[row][col] == '.':
                enemy(self.game, col, row, self.game.screen.get_width(), self.game.screen.get_height())

class Bigmom(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bigmom
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = BIGMOM_SPEED  
        self.hitpoints = 500
        self.last_spawn_time = 0
    
    def update(self):
        # Calculate direction vector to player and make Bigmom target player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalizes the direction vector and scale the boss by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

        # Multiplies velocity by delta time 
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # Ai Code: Spawns enemies every 2 seconds
        now = pg.time.get_ticks()
        if now - self.last_spawn_time > 2000:  # 2000 milliseconds = 2 seconds
            self.last_spawn_time = now
            self.spawn_enemies(3) # number of enemies spawned every 2 seconds

        # Checking if Bigmom collides with da sword
        sword_hit = pg.sprite.spritecollideany(self, self.game.sword)
        if sword_hit:
            self.hitpoints -= 1  # When sword hits Reduces da hitpoints
            sword_hit.kill()  # Remove the sword
            if self.hitpoints <= 0:
                self.spawn_enemies()  # Spawn da enemies if hitpoints are gone
                self.kill()  # Kill Bigmom if hp = 0
# Modiefied Ai code
# spawn enemies randomly
    def spawn_enemies(self, num_enemies):
        for _ in range(num_enemies): # number o'enemies
            col = random.randint(0, len(self.game.map_data[0]) - 1)  # Spawns at Random column
            row = random.randint(0, len(self.game.map_data) - 1)     # Spawn at Random row
            if self.game.map_data[row][col] == '.':
                enemy(self.game, col, row, self.game.screen.get_width(), self.game.screen.get_height())

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
            
class Buggy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.buggy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = BUGGY_SPEED  
        self.hitpoints = 500
        self.shoot_delay = 1000  # Shoot every 1 second
        self.last_shot = pg.time.get_ticks()  # Time of the last shot
        
# AI Code
    def update(self):
        # Calculate direction vector to player and make Buggy follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalizes the direction vector and scale the boss by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

        # Multiply velocity by delta time 
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        #Ai code shoots bullets after shoot delay over
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now # shoots when delay over
            self.shoot()
        
        # Check if Buggy collides with the sword
        sword_hit = pg.sprite.spritecollideany(self, self.game.sword)
        if sword_hit:
            self.hitpoints -= 1  # If hit it shall Reduce hitpoints
            sword_hit.kill()  # Remove the sword
            if self.hitpoints <= 0:
                self.spawn_enemies()  # Spawns da enemies if hitpoints are zero
                self.kill()  # Kills Buggy if hp = 0
# Ai Code Modified Spawns enemies randomly
    def spawn_enemies(self, num_enemies):
        for _ in range(num_enemies):
            col = random.randint(0, len(self.game.map_data[0]) - 1)  # Spawns at Random column
            row = random.randint(0, len(self.game.map_data) - 1)     # Spawns at Random row
            if self.game.map_data[row][col] == '.':
                enemy(self.game, col, row, self.game.screen.get_width(), self.game.screen.get_height())
    # Ai modified Code; adds bullets
    def shoot(self):
        bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, self.vx, self.vy) #launches from center
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

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

class Bullet(Sprite):
    def __init__(self, game, x, y, vx, vy):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = vx * 5  # Bullet speed is multiplied by the buggy speed
        self.vy = vy * 5  # Bullet speed is multiplies by the buggy speed
# Ai modified code
#updates relative to games delta time
    def update(self):
        self.rect.x += self.vx * self.game.dt
        self.rect.y += self.vy * self.game.dt
# allows to hit player and - hitpoints
        hits = pg.sprite.spritecollide(self, self.game.player_group, False)
        for hit in hits:
            hit.hitpoints -= 1
            self.kill()
        # Kills the bullet if it goes off screen
        if not self.game.screen.get_rect().colliderect(self.rect):
            self.kill()

        # Check for collision with walls
        wall_hit = pg.sprite.spritecollideany(self, self.game.walls)
        if wall_hit:
            self.kill() #kills if touches walls
            
class Shanks(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.shanks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((64, 64))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = SHANK_SPEED  
        self.hitpoints = 500
        self.swinging = False #Katana activated
        self.katana = None
        self.swing_cooldown = Cooldown()  # Add cooldown instance/Swing Cooldown!

    def update(self):
        # Calculate direction vector to player and make Shanks follow player's center
        direction = pg.math.Vector2(self.game.player.rect.center) - pg.math.Vector2(self.rect.center)
        # Normalize the direction vector and scale the velocity by speed
        if direction.length() > 0:
            self.vx, self.vy = direction.normalize() * self.speed

        # Update position with delta time
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

        # Handle swinging katana with cooldown
        self.swing_cooldown.ticking() #starts timer
        if self.swing_cooldown.countdown(3) <= 0 and not self.swinging:
            self.swinging = True #swings/activates katana!
            self.katana = Katana(self.game, self)
            self.game.all_sprites.add(self.katana)
            self.swing_cooldown.event_reset()

        # Check if Shanks collides with the sword
        sword_hit = pg.sprite.spritecollideany(self, self.game.sword)
        if sword_hit:
            self.hitpoints -= 1  # Reduce hitpoints
            sword_hit.kill()  # Remove the sword
            if self.hitpoints <= 0:
                self.spawn_enemies()  # Spawn enemies if Shanks' hitpoints are 0
                self.kill()  # Kill Shanks if hitpoints are 0

    def spawn_enemies(self, num_enemies):
        for _ in range(num_enemies):
            col = random.randint(0, len(self.game.map_data[0]) - 1)  # Random column
            row = random.randint(0, len(self.game.map_data) - 1)  # Random row
            if self.game.map_data[row][col] == '.':
                enemy(self.game, col, row, self.game.screen.get_width(), self.game.screen.get_height())

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

class Katana(Sprite):
    def __init__(self, game, shanks):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((80, 29))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.shanks = shanks  # Relates to Shanks 
        self.duration = 100  # Duration the katana stays active on the screen
        self.timer = 0  

    def update(self):
        self.timer += self.game.dt
        if self.timer >= self.duration:
            self.kill()

        offset = pg.math.Vector2(30, 0)
        self.rect.center = self.shanks.rect.center + offset # gives shanks the katana based on center

        hits_player = pg.sprite.spritecollide(self, [self.game.player], False)
        if hits_player:
            for player in hits_player:
                player.hitpoints -= 20
                if player.hitpoints <= 0:
                    player.kill()
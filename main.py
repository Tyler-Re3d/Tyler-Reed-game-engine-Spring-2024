# This file was created by: Tyler Reed
# My FiRsT sOuRcE CoNtRoL EdIt
#Importing Required Modules
import pygame as pg
import sys 
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep
from math import floor
import images

# Goal: Win
# 3 things want to add: weapons, boss/different enemies, and hp bar more collectables

# Creating the Game Class
# This is a function
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
     

class Game:
    # Initiates all code in a class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        # Load save game Data
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'download-compresskaru.com.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    def new(self):
        self.test_timer = Cooldown()
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.boss = pg.sprite.Group()
       # self.player = Player(self, 10, 10)
       # for x in range(10, 20):
        #    Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            # print(row)
            for col, tile in enumerate(tiles):
                # print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'E':
                    enemy(self, col, row)
                if tile == 'B':
                    boss(self, col, row)

   
        boss_spawned = True
    # Run Method
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    # Quit Method (X in corner)
    def quit(self):
        pg.quit()
        sys.exit()
# Updates charactar after it moves
    def update(self):
        self.test_timer.ticking()
        self.all_sprites.update()
# the Backround Grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    # The sprites
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.test_timer.countdown(45)), 24, YELLOW, WIDTH/2 - 32, 2)
        pg.display.flip()

# Key Inputs ( how you move )
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx = -1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx = 1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
    # def load_data(self):
    #     game_folder = path.dirname(__file__)
    #     img_folder = path.join(game_folder, 'images')
    #     self.player_img = pg.image.load(path.join(img_folder, 'download-compresskaru.com.png')).convert_alpha()
    #     self.map_data = []
    #     with open(path.join(game_folder, 'map.txt'), 'rt') as f:
    #         for line in f:
    #             self.map_data.append(line)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()    




    
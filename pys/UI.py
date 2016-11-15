from pico2d import *
import math
import random

class UI:
    def __init__(self):
        self.menu_image = load_image('Resources/Menu_Image.png')
        self.status_image = load_image('Resources/Status_Image_empty.png')
        self.status_inner_image = load_image('Resources/Status_Image_inner.png')
        self.red_image = load_image('Resources/red.png')
        self.black_image = load_image('Resources/black.png')
        self.yellow_image = load_image('Resources/yellow.png')
        self.BGNames = ['Resources/BG_Blue.png', 'Resources/BG_Blue2.png', 'Resources/BG_Brown.png', 'Resources/BG_Orange.png', 'Resources/BG_Purple.png', 'Resources/BG_Silk.png', 'Resources/BG_Sky.png']
        self.BGImages = []
        for i in range(len(self.BGNames)):
            self.BGImages.append(load_image(self.BGNames[i]))
        self.nowBGIdx = random.randint(0, len(self.BGImages) - 1)
        self.pattern_image = load_image('Resources/pattern_3_40_600.png')
        self.ground_image = load_image('Resources/ground_40x2.png')


    def draw(self):
        global mx, my, hero
        self.BGImages[self.nowBGIdx].draw(400, 300, 799, 599)
        for j in range(math.floor(800/20 + 1)):
            self.pattern_image.draw(j*20 + 10 - camX % 20, 300)
        self.ground_image.draw(400, 280, 800, 30)
        self.menu_image.draw(75, 555, 100, 50)
        self.status_image.draw(400, 130, 800, 256)
        self.status_inner_image.draw(395, 130)
        self.black_image.draw(335, 178, 200, 25)
        self.black_image.draw(335, 130, 200, 25)
        self.black_image.draw(80 + 640/2, 80 - 50/2, 640, 50)
        if hero.direction == "RIGHT":
            hero.image.clip_draw(math.floor(hero.animFrame / 3) * 36, 38, 36, 36, 145, 160, 120, 120)
        else:
            hero.image.clip_draw(math.floor(hero.animFrame / 3) * 36, 1, 36, 36, 145, 160, 120, 120)
pass
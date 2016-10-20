from pico2d import *
import game_framework
import math
import random

mx, my = 0, 0
ui, hero = None, None

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
        self.pattern_image = load_image('Resources/pattern_3_40.png')
        self.ground_image = load_image('Resources/ground_40x2.png')


    def draw(self):
        global mx, my
        self.BGImages[self.nowBGIdx].draw(400, 300, 799, 599)
        for i in range(math.floor(600/20)):
            for j in range(math.floor(800/20)):
                self.pattern_image.draw(j*20 + 10, i*20 + 10)
        self.ground_image.draw(400, 280, 800, 30)
        self.menu_image.draw(75, 555, 100, 50)
        self.status_image.draw(400, 130, 800, 256)
        self.status_inner_image.draw(395, 130)
        self.black_image.draw(335, 178, 200, 25)
        self.black_image.draw(335, 130, 200, 25)

pass

class Hero:
    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('Resources/character.png')
        self.animFrame = 0
        self.direction = "LEFT"
        self.state = "RUN"


    def update(self):
        self.animFrame = (self.animFrame + 1) % (6 * 10)

    def draw(self):
        global mx, my
        self.image.clip_draw(6 + math.floor(self.animFrame / 10) * 36, 325 - 93 - 1, 36, 36, mx, my, 60, 60)
pass


def enter():
    global ui, hero
    ui = UI()
    hero = Hero()
    pass

def exit():
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    global mx, my
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, 599 - event.y
            print(mx, my)


def update():
    global hero
    hero.update()
    delay(0.016)

def draw():
    global ui, hero
    clear_canvas()
    ui.draw()
    hero.draw()
    update_canvas()

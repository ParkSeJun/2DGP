from pico2d import *
import game_framework
import math
import random

mx, my = 0, 0
ui, hero = None, None
camX = 0
isClicked = False
isRightClicked = False

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
        global mx, my
        self.BGImages[self.nowBGIdx].draw(400, 300, 799, 599)
        for j in range(math.floor(800/20 + 1)):
            self.pattern_image.draw(j*20 + 10 - camX % 20, 300)
        self.ground_image.draw(400, 280, 800, 30)
        self.menu_image.draw(75, 555, 100, 50)
        self.status_image.draw(400, 130, 800, 256)
        self.status_inner_image.draw(395, 130)
        self.black_image.draw(335, 178, 200, 25)
        self.black_image.draw(335, 130, 200, 25)

pass

class Hero:
    def __init__(self):
        self.x, self.y = 75, 305
        self.image = load_image('Resources/character.png')
        self.animFrame = 0
        self.direction = "RIGHT"
        self.state = "RUN"
        self.isAttacking = False
        self.isGuarding = False
        self.attackFrame = 0
        self.attackAnimation = [load_image('Resources/attack1.png'), load_image('Resources/attack2.png'),load_image('Resources/attack3.png'),load_image('Resources/attack4.png'),load_image('Resources/attack5.png')]
        self.guardImage = load_image('Resources/guard.png')

    def update(self):
        global camX, isClicked, isRightClicked


        if isRightClicked == True:
            self.isGuarding = True
        else:
            self.isGuarding = False

        if self.isGuarding == True and self.isAttacking:
            self.attackFrame += 1
        elif self.isGuarding == False:
            self.animFrame = (self.animFrame + 1) % (6 * 3)
            self.attackFrame += 1
            if isClicked:
                if self.direction == "LEFT":
                    self.direction = "RIGHT"
                else:
                    self.direction = "LEFT"
                isClicked = False

            if self.direction == "RIGHT":
                self.x += 5
            else:
                self.x -= 2

        camX += 1.5

        if self.x - camX > 270:
            camX += self.x - camX - 270
        elif self.x - camX < 50:
            self.x = camX + 50

        if self.isAttacking == False and self.attackFrame >= 20:
            self.attackFrame = 0
            self.isAttacking = True

        if self.isAttacking == True and self.attackFrame >= 5 * 3:
            self.attackFrame = 0
            self.isAttacking = False

        if self.isAttacking == True:
            # attack Monster
            pass


    def draw(self):
        global mx, my, camX
        if self.direction == "RIGHT":
            self.image.clip_draw(math.floor(self.animFrame / 3) * 36, 38, 36, 36, self.x - camX, self.y, 60, 60)
        else:
            self.image.clip_draw(math.floor(self.animFrame / 3) * 36, 1, 36, 36, self.x - camX, self.y, 60, 60)
        if self.isAttacking == True:
            self.attackAnimation[math.floor(self.attackFrame / 3)].draw(self.x - camX + 50, self.y + 30, 180, 180)
        if self.isGuarding == True:
            self.guardImage.draw(self.x - camX, self.y)
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
    global mx, my, isClicked, isRightClicked
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, 599 - event.y
            print(mx, my)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == 1:
                isClicked = True
            elif event.button == 3:
                isRightClicked = True
        elif event.type == SDL_MOUSEBUTTONUP:
            print(event.button)
            if event.button == 3:
                isRightClicked = False

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

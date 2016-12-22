from pico2d import *
import game_framework
import math
import random
import json

JSON_FILENAME = 'GameData.json'
JSON_DATA = None

jsonFile = open(JSON_FILENAME, "r")
JSON_DATA = json.load(jsonFile)
jsonFile.close()

PIXEL_PER_METER = JSON_DATA['PIXEL_PER_METER']

mx, my = 0, 0
ui, hero = None, None
camX = 0 #27000
isClicked = False
isRightClicked = False

enemies = []

isFreeze = False
unfrozenObject = None

class UI:
    def __init__(self):
        self.font = load_font('Resources/CFMarieEve.ttf', JSON_DATA['UI']['fontSize'])
        self.numFont = load_font('Resources/ConsolaMalgun.ttf', JSON_DATA['UI']['numFontSize'])

        self.menu_image = load_image('Resources/Menu_Image.png')
        self.status_image = load_image('Resources/Status_Image_empty.png')
        self.status_inner_image = load_image('Resources/Status_Image_inner.png')
        self.red_image = load_image('Resources/red.png')
        self.black_image = load_image('Resources/black.png')
        self.yellow_image = load_image('Resources/yellow.png')
        self.blue_image = load_image('Resources/BG_Blue2.png')
        self.BGNames = ['Resources/BG_Blue.png', 'Resources/BG_Blue2.png', 'Resources/BG_Brown.png', 'Resources/BG_Orange.png', 'Resources/BG_Purple.png', 'Resources/BG_Silk.png', 'Resources/BG_Sky.png']
        self.BGImages = []
        for i in range(len(self.BGNames)):
            self.BGImages.append(load_image(self.BGNames[i]))
        self.nowBGIdx = random.randint(0, len(self.BGImages) - 1)
        self.pattern_image = load_image('Resources/pattern_3_40_600.png')
        self.ground_image = load_image('Resources/ground_40x2.png')
        self.mapBox = load_image('Resources/whiteBox.png')

    def draw(self):
        global mx, my, hero, enemies
        self.BGImages[self.nowBGIdx].draw(JSON_DATA['UI']['BGX'], JSON_DATA['UI']['BGY'], JSON_DATA['UI']['BGW'], JSON_DATA['UI']['BGH'])
        for j in range(int(800/JSON_DATA['UI']['patternW'] + 1)):
            self.pattern_image.draw(j * JSON_DATA['UI']['patternW'] + JSON_DATA['UI']['patternOffsetX'] - camX % JSON_DATA['UI']['patternW'], JSON_DATA['UI']['patternY'])
        self.ground_image.draw(JSON_DATA['UI']['groundImageX'], JSON_DATA['UI']['groundImageY'], JSON_DATA['UI']['groundImageW'], JSON_DATA['UI']['groundImageH'])
        self.menu_image.draw(JSON_DATA['UI']['menuImageX'], JSON_DATA['UI']['menuImageY'], JSON_DATA['UI']['menuImageW'], JSON_DATA['UI']['menuImageH'])
        self.status_image.draw(JSON_DATA['UI']['statusImageX'], JSON_DATA['UI']['statusImageY'], JSON_DATA['UI']['statusImageW'], JSON_DATA['UI']['statusImageH'])
        self.status_inner_image.draw(JSON_DATA['UI']['statusInnerImageX'], JSON_DATA['UI']['statusInnerImageY'])
        self.black_image.draw(JSON_DATA['UI']['HPBarImageX'], JSON_DATA['UI']['HPBarImageY'], JSON_DATA['UI']['HPBarImageW'], JSON_DATA['UI']['HPBarImageH'])
        self.black_image.draw(JSON_DATA['UI']['EXPBarImageX'], JSON_DATA['UI']['EXPBarImageY'], JSON_DATA['UI']['EXPBarImageW'], JSON_DATA['UI']['EXPBarImageH'])
        self.black_image.draw(JSON_DATA['UI']['blackMapBarImageX'], JSON_DATA['UI']['blackMapBarImageY'], JSON_DATA['UI']['blackMapBarImageW'], JSON_DATA['UI']['blackMapBarImageH'])
        if hero.direction == "RIGHT":
            hero.image.clip_draw(hero.runFrame * JSON_DATA['Hero']['imageWGap'], JSON_DATA['Hero']['imageRightStartY'], JSON_DATA['Hero']['imageW'], JSON_DATA['Hero']['imageH'], JSON_DATA['UI']['heroImageX'], JSON_DATA['UI']['heroImageY'], JSON_DATA['UI']['heroImageY'], JSON_DATA['UI']['heroImageH'])
        else:
            hero.image.clip_draw(hero.runFrame * JSON_DATA['Hero']['imageWGap'], JSON_DATA['Hero']['imageLeftStartY'], JSON_DATA['Hero']['imageW'], JSON_DATA['Hero']['imageH'], JSON_DATA['UI']['heroImageX'], JSON_DATA['UI']['heroImageY'], JSON_DATA['UI']['heroImageY'], JSON_DATA['UI']['heroImageH'])

        self.red_image.draw(JSON_DATA['UI']['HPBarImageX'] - (hero.fullHP - hero.HP), JSON_DATA['UI']['HPBarImageY'], JSON_DATA['UI']['HPBarImageW'] / hero.fullHP * hero.HP, JSON_DATA['UI']['HPBarImageH'])
        self.blue_image.draw(JSON_DATA['UI']['EXPBarImageX'] - (hero.fullEXP - hero.EXP), JSON_DATA['UI']['EXPBarImageY'], JSON_DATA['UI']['EXPBarImageW'] / hero.fullEXP * hero.EXP, JSON_DATA['UI']['EXPBarImageH'])
    
        self.font.draw(JSON_DATA['UI']['HPX'], JSON_DATA['UI']['HPY'], "HP", (0xFF, 0xFF, 0xFF))
        self.numFont.draw(JSON_DATA['UI']['HPValueX'], JSON_DATA['UI']['HPValueY'], "%d/%d" % (hero.HP, hero.fullHP), (0xFF, 0xFF, 0xFF))
        self.font.draw(JSON_DATA['UI']['EXPX'], JSON_DATA['UI']['EXPY'], "EXP", (0xFF, 0xFF, 0xFF))
        self.numFont.draw(JSON_DATA['UI']['EXPValueX'], JSON_DATA['UI']['EXPValueY'], "%d/%d" % (hero.EXP, hero.fullEXP), (0xFF, 0xFF, 0xFF))

        for e in enemies:
            if not e.state == "DIE":
                self.red_image.draw(JSON_DATA['UI']['mapObjectOffsetX'] + JSON_DATA['UI']['blackMapBarImageW'] / JSON_DATA['maxCamX'] * e.x, JSON_DATA['UI']['blackMapBarImageY'] - JSON_DATA['UI']['blackMapBarImageH'] / 2 + JSON_DATA['UI']['mapBoxY'] / JSON_DATA['groundH'] * (e.y - JSON_DATA['groundY']), JSON_DATA['UI']['mapObjectW'], JSON_DATA['UI']['mapObjectH'])

        self.yellow_image.draw(JSON_DATA['UI']['mapObjectOffsetX'] + JSON_DATA['UI']['blackMapBarImageW'] / JSON_DATA['maxCamX'] * hero.x , JSON_DATA['UI']['blackMapBarImageY'] - JSON_DATA['UI']['blackMapBarImageH'] / 2 + JSON_DATA['UI']['mapBoxY'] / JSON_DATA['groundH'] * (hero.y - JSON_DATA['groundY']), JSON_DATA['UI']['mapObjectW'], JSON_DATA['UI']['mapObjectH'])

        self.mapBox.draw(JSON_DATA['UI']['mapBoxX'] + JSON_DATA['UI']['blackMapBarImageW'] / JSON_DATA['maxCamX'] * camX,  JSON_DATA['UI']['mapBoxY'], JSON_DATA['UI']['mapBoxW'], JSON_DATA['UI']['mapBoxH'])
pass

class Hero:
    RUN_SPEED_KMPH = JSON_DATA['Hero']['RUN_SPEED_KMPH']
    RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000. / 60.
    RUN_SPEED_MPS = RUN_SPEED_MPM / 60.
    RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

    RUN_TIME_PER_ACTION = JSON_DATA['Hero']['RUN_TIME_PER_ACTION']
    RUN_ACTION_PER_TIME = 1.0 / RUN_TIME_PER_ACTION
    RUN_FRAMES_PER_ACTION = JSON_DATA['Hero']['RUN_FRAMES_PER_ACTION']

    ATTACK_DELAY = JSON_DATA['Hero']['ATTACK_DELAY']
    ATTACK_DURATION = JSON_DATA['Hero']['ATTACK_DURATION']

    def __init__(self):
        self.x, self.y = JSON_DATA['Hero']['x'], JSON_DATA['Hero']['y']
        self.image = load_image('Resources/character.png')
        self.runFrame = 0
        self.runTotalFrame = 0.0
        self.direction = JSON_DATA['Hero']['direction']
        self.state = JSON_DATA['Hero']['state']
        self.isAttacking = False
        self.isGuarding = False
        self.attackFrame = 0.0
        #self.attackAnimation = [load_image('Resources/attack1.png'), load_image('Resources/attack2.png'),load_image('Resources/attack3.png'),load_image('Resources/attack4.png'),load_image('Resources/attack5.png')]
        self.attackImage = {"RIGHT":load_image('Resources/attack_right.png'), "LEFT":load_image('Resources/attack_left.png')}
        self.guardImage = load_image('Resources/guard.png')

        self.fullHP = JSON_DATA['Hero']['fullHP']
        self.HP = JSON_DATA['Hero']['HP']
        self.fullEXP = JSON_DATA['Hero']['fullEXP']
        self.EXP = JSON_DATA['Hero']['EXP']

    def update(self, time):
        global camX, isClicked, isRightClicked

        if isFreeze:
            return


        if not self.isGuarding or self.isAttacking:
            self.attackFrame += time

        if isRightClicked == True:
            self.isGuarding = True
        else:
            self.isGuarding = False

        if self.isGuarding == False:
            self.runTotalFrame += Hero.RUN_FRAMES_PER_ACTION * Hero.RUN_ACTION_PER_TIME * time
            self.runFrame = int(self.runTotalFrame) % Hero.RUN_FRAMES_PER_ACTION
            if isClicked:
                if self.direction == "LEFT":
                    self.direction = "RIGHT"
                else:
                    self.direction = "LEFT"
                isClicked = False

            if self.direction == "RIGHT":
                self.x += JSON_DATA['Hero']['moveSpeedRight'] * time
            else:
                self.x += JSON_DATA['Hero']['moveSpeedLeft'] * time

        camX += JSON_DATA['Hero']['camSpeed'] * time

        if camX >= JSON_DATA['maxCamX'] - JSON_DATA['Hero']['camLastLimitMax']:
            camX = JSON_DATA['maxCamX'] - JSON_DATA['Hero']['camLastLimitMax']

        if self.x - camX > JSON_DATA['Hero']['camLimitMax']:
            if camX >= JSON_DATA['maxCamX'] - JSON_DATA['Hero']['camLastLimitMax']:
               # print(ok)
                if self.x > JSON_DATA['maxCamX'] - JSON_DATA['Hero']['camLastLimitMin'] - JSON_DATA['Hero']['w'] / 2:
                    self.x = JSON_DATA['maxCamX'] - JSON_DATA['Hero']['camLastLimitMin'] - JSON_DATA['Hero']['w'] / 2
            else:
                camX += (self.x - camX - JSON_DATA['Hero']['camLimitMax']) / JSON_DATA['Hero']['camLimitSpeedRate']
                self.x = camX + JSON_DATA['Hero']['camLimitMax']
        elif self.x - camX < JSON_DATA['Hero']['camLimitMin']:
            self.x = camX + JSON_DATA['Hero']['camLimitMin']

        if self.isAttacking == False and self.attackFrame >= Hero.ATTACK_DELAY:
            self.attackFrame -= Hero.ATTACK_DELAY
            self.isAttacking = True

        if self.isAttacking == True and self.attackFrame > Hero.ATTACK_DURATION:
            self.attackFrame -= Hero.ATTACK_DURATION
            self.isAttacking = False

        if self.isAttacking == True:
            # attack Monster
            pass


    def draw(self):
        global mx, my, camX
        if self.direction == "RIGHT":
            self.image.clip_draw(self.runFrame * JSON_DATA['Hero']['imageWGap'], JSON_DATA['Hero']['imageRightStartY'], JSON_DATA['Hero']['imageW'], JSON_DATA['Hero']['imageH'], self.x - camX, self.y, JSON_DATA['Hero']['w'], JSON_DATA['Hero']['h'])
        else:
            self.image.clip_draw(self.runFrame * JSON_DATA['Hero']['imageWGap'], JSON_DATA['Hero']['imageLeftStartY'], JSON_DATA['Hero']['imageW'], JSON_DATA['Hero']['imageH'], self.x - camX, self.y, JSON_DATA['Hero']['w'], JSON_DATA['Hero']['h'])

        if self.isAttacking == True:
            self.attackImage[self.direction].draw(self.x - camX, self.y, JSON_DATA['Hero']['attackW'], JSON_DATA['Hero']['attackH'])

        if self.isGuarding == True:
            self.guardImage.draw(self.x - camX, self.y)

            print(camX)

    def get_bb(self):
        return [self.x - JSON_DATA['Hero']['w'] / 2 - camX, self.y - JSON_DATA['Hero']['h'] / 2, self.x + JSON_DATA['Hero']['w']/2 - camX, self.y + JSON_DATA['Hero']['h'] /2 ]

    def get_attack_bb(self):
        return [self.x - JSON_DATA['Hero']['w'] / 2 - camX - (JSON_DATA['Hero']['attackOffsetX'] if self.direction == "LEFT" else 0), self.y - JSON_DATA['Hero']['h'] / 2, self.x + JSON_DATA['Hero']['w']/2 - camX + (JSON_DATA['Hero']['attackOffsetX'] if self.direction == "RIGHT" else 0), self.y + JSON_DATA['Hero']['h'] /2 +JSON_DATA['Hero']['attackOffsetY']]

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw_attack_bb(self):
        draw_rectangle(*self.get_attack_bb())
pass

class Enemy:
    RUN_SPEED_KMPH = JSON_DATA['Enemy']['RUN_SPEED_KMPH']
    RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000. / 60.
    RUN_SPEED_MPS = RUN_SPEED_MPM / 60.
    RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

    RUN_TIME_PER_ACTION = JSON_DATA['Enemy']['RUN_TIME_PER_ACTION']
    RUN_ACTION_PER_TIME = 1.0 / RUN_TIME_PER_ACTION
    RUN_FRAMES_PER_ACTION = JSON_DATA['Enemy']['RUN_FRAMES_PER_ACTION']

    def __init__(self):
        self.w = JSON_DATA['Enemy']['w']
        self.h = JSON_DATA['Enemy']['h']
        self.x = random.randint(JSON_DATA['Enemy']['xRandMin'], JSON_DATA['maxCamX'] - JSON_DATA['Enemy']['xRandMin'])
        self.y = JSON_DATA['groundY'] + self.h / 2

        self.runFrame = 0
        self.runTotalFrame = 0.0
        self.direction = JSON_DATA['Enemy']['direction']
        self.state = JSON_DATA['Enemy']['state']
        self.image = None
        self.dyingJumpPower = JSON_DATA['Enemy']['dyingJumpPower']

        self.imageName = ""
        pass

    def update(self, frame_time):
        global isFreeze, unfrozenObject
        if isFreeze and not self == unfrozenObject:
            return

        if self.state == "RUNNING":
            self.runTotalFrame += Enemy.RUN_FRAMES_PER_ACTION * Enemy.RUN_ACTION_PER_TIME * frame_time
            self.runFrame = int(self.runTotalFrame) % Enemy.RUN_FRAMES_PER_ACTION
            if self.direction == "LEFT":
                self.x -= Enemy.RUN_SPEED_PPS * frame_time
            else:
                self.x += Enemy.RUN_SPEED_PPS * frame_time
        elif self.state == "DYING":
            self.y += self.dyingJumpPower * frame_time
            self.dyingJumpPower -= frame_time * JSON_DATA['Enemy']['dyingjumpPowerWeight']
            if(self.y < JSON_DATA['Enemy']['dyingLimit'] ):
                isFreeze = False
                self.state = "DIE"
                del(self.image)


        pass

    def draw(self):
        if self.image and not self.state == "DIE":
            self.image.clip_draw(self.runFrame * JSON_DATA['Enemy']['imageWGap'] , JSON_DATA['Enemy']['imageLeftStartingY'] if self.direction == "LEFT" else JSON_DATA['Enemy']['imageRightStartingY'], JSON_DATA['Enemy']['imageW'], JSON_DATA['Enemy']['imageH'], self.x - camX, self.y, JSON_DATA['Enemy']['w'], JSON_DATA['Enemy']['h'])
        pass

    def die(self):
        global unfrozenObject
        self.state = "DYING"
        self.image = load_image(self.imageName)
        self.image.opacify(JSON_DATA['Enemy']['dyingOpacify'])
        unfrozenObject = self

    def get_bb(self):
        return [self.x - self.w / 2 - camX, self.y - self.h /2 , self.x + self.w /2 - camX, self.y + self.h/2]

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    pass

class EnemyFlower(Enemy):
    image = None # load_image("Resources/Enemy_Flower.png")
    def __init__(self):
        Enemy.__init__(self)
        if EnemyFlower.image == None:
            EnemyFlower.image = load_image("Resources/Enemy_Flower.png")
        self.image = EnemyFlower.image
        self.imageName = "Resources/Enemy_Flower.png"
        pass
    pass

class EnemyFrog(Enemy):
    image = None # load_image("Resources/Enemy_Flower.png")
    def __init__(self):
        Enemy.__init__(self)
        #print(EnemyFrog.image)
        if EnemyFrog.image == None:
            EnemyFrog.image = load_image("Resources/Enemy_Frog.png")
        self.image = EnemyFrog.image
        self.imageName = "Resources/Enemy_Frog.png"
        pass
    pass

def enter():
    global ui, hero, enemies
    ui = UI()
    hero = Hero()

    for i in range(JSON_DATA['enemyCount']):
        if(random.randint(0, 1)):
            enemies.append(EnemyFlower())
        else:
            enemies.append(EnemyFrog())
    pass

def exit():
    pass

def pause():
    pass

def resume():
    pass

def isCollision(rectA, rectB):
    if rectB[2] < rectA[0] or rectA[1] > rectB[3] or rectA[2] < rectB[0] or rectB[1] > rectA[3]:
        return False
    return True

def handle_events(frame_time):
    global mx, my, isClicked, isRightClicked
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, 599 - event.y
            #print(mx, my)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == 1:
                isClicked = True
            elif event.button == 3:
                isRightClicked = True
            mx, my = event.x, 599 - event.y
            print(mx, my)
        elif event.type == SDL_MOUSEBUTTONUP:
            #print(event.button)
            if event.button == 3:
                isRightClicked = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                isClicked = True
            elif event.key == SDLK_RETURN:
                isRightClicked = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RETURN:
                isRightClicked = False

def update(frame_time):
    global hero, enemies, isFreeze
    hero.update(frame_time)

    if hero.isAttacking:
        for e in enemies:
            if e.state == "RUNNING" and isCollision(hero.get_attack_bb(), e.get_bb()):
                isFreeze = True
                e.die()
                break

    for e in enemies:
        e.update(frame_time)


def draw():
    global ui, hero, enemies
    clear_canvas()

    ui.draw()

    for e in enemies:
        e.draw()
       # e.draw_bb()
    hero.draw()
    #hero.draw_bb()
    #if hero.isAttacking:
    #    hero.draw_attack_bb()



    update_canvas()

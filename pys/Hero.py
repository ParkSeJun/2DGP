from pico2d import *

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

    def update(self, time):
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
                self.x += 5 * time * 60
            else:
                self.x -= 2 * time * 60

        camX += 1.5 * time * 60

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
import pygame
import tools
import Constants

class BatEnemy:
    mainSurface = None

    initX = 0
    initY = 0

    xPos = 0
    yPos = 0
    movementHeight = 0

    width = 75
    height = 40

    enemyRect = None
    topRect = None

    goingDown = True
    goingUp = False

    mainAnimation = None
    image = None
    animationCount = 0

    dead = False
    deadRunOnce = True
    deathCount = 0
    deathImage = None

    delete = False

    tag = "batEnemy"

    def __init__(self,surface : pygame.Surface,x : int, y : int, movementRange: int):
        self.mainSurface = surface

        self.initX = x
        self.initY = y

        self.xPos = x
        self.yPos = y

        self.movementHeight = movementRange

        self.setRects()

        self.mainAnimation = Constants.Animations.BatEnemy.mainAnimation


    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)
        self.topRect = pygame.Rect(self.xPos-6,self.yPos,self.width,28)

    def control(self,platforms,bullets : list,character):
        if not self.dead:
            if self.goingUp:
                self.yPos-=4
            elif self.goingDown:
                self.yPos += 4

            self.setRects()

            if self.yPos < self.initY - self.movementHeight:
                self.goingUp = False
                self.goingDown = True

            if self.yPos > self.initY+self.movementHeight:
                self.goingDown = False
                self.goingUp = True

            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos,bullet.yPos):
                    self.dead = True
                    bullet.destroy = True
        else:
            if self.deadRunOnce:
                self.deathImage = self.mainAnimation[0]
                self.deadRunOnce = False
                self.enemyRect = pygame.Rect(0,0,0,0)

            self.image = pygame.transform.rotate(self.deathImage,self.deathCount * 8)
            self.yPos += 3

            self.deathCount += 1
            if self.deathCount >= 120:
                self.delete = True

    def display(self):
        if not self.dead:
            if self.animationCount >= len(self.mainAnimation):
                self.animationCount = 0

            self.image = self.mainAnimation[self.animationCount]
            self.animationCount+=1


        self.mainSurface.blit(self.image,(self.xPos,self.yPos))
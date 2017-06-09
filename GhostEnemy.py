import pygame
import Constants

class GhostEnemy:
    mainSurface = None

    xPos = 0
    yPos = 0
    speed = 0

    width = 50
    height = 50

    dead = False
    deadRunOnce = True
    deathCount = 0
    deathImage = None

    delete = False

    goingRight = False
    goingLeft = False\


    enemyRect = None
    rightEnemyRect = None
    leftEnemyRect = None
    topEnemyRect = None
    bottomEnemyRect = None

    tag = "ghostEnemy"

    movingAnimation = []
    animationCount = 0
    image = None

    def __init__(self, surface: pygame.Surface, x, y, speed=4):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.setRects()

        self.movingAnimation = Constants.Animations.GhostEnemy.movingAnimation

    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topEnemyRect = pygame.Rect(self.xPos, self.yPos, self.width, 10)
        self.leftEnemyRect = pygame.Rect(self.xPos, self.yPos, 10, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 10, self.yPos, 10, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    def control(self, platforms, bullets, character):
        if not self.dead:
            if not character.yPos <= self.yPos + self.height / 2 <= character.yPos + character.characterHeight:
                if character.yPos < self.yPos + self.height / 2:
                    self.yPos -= self.speed
                elif character.yPos > self.yPos + self.height / 2:
                    self.yPos += self.speed

            if not character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth:
                if character.xPos > self.xPos + self.width / 2:
                    self.xPos += self.speed
                    self.goingRight = True
                    self.goingLeft = False
                elif character.xPos < self.xPos + self.width / 2:
                    self.xPos -= self.speed
                    self.goingLeft = True
                    self.goingRight = False

            self.setRects()

            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):
                    self.dead = True
                    bullet.destroy = True
        else:
            if self.deadRunOnce:
                self.deathImage = self.movingAnimation[0]
                self.deadRunOnce = False
                self.enemyRect = pygame.Rect(0,0,0,0)

            self.image = pygame.transform.rotate(self.deathImage,self.deathCount * 8)
            self.yPos += 3

            self.deathCount += 1
            if self.deathCount >= 120:
                self.delete = True

    def animationControl(self):
        if self.animationCount >= len(self.movingAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.1

        self.image = self.movingAnimation[int(self.animationCount)]

    def display(self):
        if not self.dead:
            self.animationControl()


        if self.image is not None:
            if self.goingLeft:
                self.mainSurface.blit(self.image, (
                self.xPos, self.yPos + 3))  # Add 3 because the image normally is off the ground a littlea
            else:
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos, self.yPos + 3))
        else:
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)

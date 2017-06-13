import pygame

import Constants
import FireBall
import tools


class ZombieEnemy:
    mainSurface = None

    xPos = 0
    yPos = 0
    speed = 0

    width = 150
    height = 240

    dead = False
    deadRunOnce = True
    deathCount = 0
    delete = False

    goingLeft = True
    goingRight = False
    goingDown = True

    leftColliding = False
    rightColliding = False

    enemyRect = None
    rightEnemyRect = None
    leftEnemyRect = None
    topEnemyRect = None
    bottomEnemyRect = None

    tag = "zombieBoss"

    movingAnimation = []
    animationCount = 0
    image = None

    currentAnimation = []

    health = 3

    shootCount = 0
    shootCountLimit = 120

    facingLeft = True
    facingRight = False

    def __init__(self, surface: pygame.Surface, x, y, speed=4, health=10):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.setRects()
        self.health = health

        self.movingAnimation = tools.scaleImages(Constants.Animations.ZombieEnemy.movingAnimation, 3)

        self.currentAnimation = self.movingAnimation

    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos + 30, self.yPos + 10, self.width - 60, self.height - 10)
        self.topEnemyRect = pygame.Rect(self.xPos, self.yPos, self.width, 10)
        self.leftEnemyRect = pygame.Rect(self.xPos - 20, self.yPos, 30, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 20, self.yPos, 30, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    def control(self, platforms, bullets, character):
        if not self.dead:
            if self.health <= 0:
                self.dead = True

            if not (character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth):
                if character.xPos >= self.xPos + self.width / 2:
                    self.facingRight = True
                    self.facingLeft = False
                elif character.xPos <= self.xPos + self.width / 2:
                    self.facingLeft = True
                    self.facingRight = False

            if self.collidingBottom(platforms):
                self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
                self.goingDown = False
                if self.getCollidingBottomRect(platforms).tag == "deathPlatform":
                    self.dead = True
                if not (character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth):
                    if character.xPos > self.xPos:
                        self.goingRight = True
                        self.goingLeft = False
                    elif character.xPos < self.xPos:
                        self.goingLeft = True
                        self.goingRight = False

                else:
                    self.goingLeft = False
                    self.goingRight = False
            else:
                self.goingLeft = False
                self.goingRight = False
                self.goingDown = True

            if self.goingRight:
                if not self.collidingRight(platforms):
                    self.xPos += self.speed

            if self.goingLeft:
                if not self.collidingLeft(platforms):
                    self.xPos -= self.speed

            if self.goingDown:
                self.yPos += self.speed

            self.setRects()
        else:
            if self.deadRunOnce:
                self.image = pygame.transform.scale(self.movingAnimation[0], (self.movingAnimation[0].get_width(), 15))
                self.yPos = self.yPos + self.height
                self.deadRunOnce = False
                self.enemyRect = pygame.Rect(0, 0, 0, 0)
            self.deathCount += 1
            if self.deathCount >= 60:
                self.delete = True

        if self.shootCount >= self.shootCountLimit:
            self.shootCount = 0
            if self.facingRight:
                bullets.append(
                    FireBall.FireBall(self.mainSurface, self.xPos + self.width - 30, self.yPos + 85, hurtPlayer=True,
                                      startRight=True, speed=11))
            elif self.facingLeft:
                bullets.append(
                    FireBall.FireBall(self.mainSurface, self.xPos + 30, self.yPos + 85, hurtPlayer=True,
                                      startRight=False, speed=11))
        self.shootCount += 1


    def animationControl(self):
        if self.animationCount >= len(self.currentAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.3

        self.image = self.currentAnimation[int(self.animationCount)]

    def display(self):
        if not self.dead:
            self.animationControl()

        if self.image is not None:
            if self.facingLeft:
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos - 30, self.yPos - 60))
            else:
                self.mainSurface.blit(self.image, (
                    self.xPos - 30, self.yPos - 60))  # -5 and -18 to align the image properly
        else:
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)


    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 700 < self.xPos:
                if platform.checkLeftCollide(self.rightEnemyRect):
                    self.rightColliding = True
                    return True
        self.rightColliding = False
        return False

    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:
                if platform.checkRightCollide(self.leftEnemyRect):
                    self.leftColliding = True
                    return True
        self.leftColliding = False
        return False

    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 700 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkBottomCollide(self.topEnemyRect):
                    return True
        return False

    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomEnemyRect):
                    return True
        return False

    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomEnemyRect):
                    return platform
        return None

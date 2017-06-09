import pygame
import Bullet
import math
import Constants
import FireBall

class ShooterEnemy:
    mainSurface = None

    xPos = 0
    yPos = 0

    fallSpeed = 5

    enemyRect = None
    bottomEnemyRect = None
    topEnemyRect = None

    width = 60
    height = 80

    goingDown = True

    dead = False
    deadRunOnce = True
    deathCount = 0

    delete = False

    tag = "shooterEnemy"

    shootCount = 0
    shootTimerLimit = 150

    shootBalls = False

    image = None
    currentAnimation = None
    animationCount = 0

    animationSwitchCount = 31

    idleAnimation = None
    shootingAnimation = None

    def __init__(self, surface: pygame.Surface, x: int, y: int,fallSpeed:int = 5,shootBalls = False):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y

        self.fallSpeed = fallSpeed

        self.shootBalls = shootBalls

        self.setRects()

        self.shootingAnimation = Constants.Animations.ShooterEnemy.shootingAnimation
        self.idleAnimation = Constants.Animations.ShooterEnemy.idleAnimation


    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 20, self.width, 20)
        self.topEnemyRect = pygame.Rect(self.xPos,self.yPos,self.width,20)

    def control(self, platforms, bullets, character):
        if not self.dead:
            if not self.collidingBottom(platforms):
                self.goingDown = True

            if self.goingDown:
                self.yPos += self.fallSpeed
                if self.collidingBottom(platforms):
                    self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
                    self.goingDown = False

            self.shootCount += 1
            if self.shootCount >= self.shootTimerLimit:
                if character.xPos + character.characterWidth/2 < self.xPos:
                    if self.shootBalls:
                        bullets.append(FireBall.FireBall(self.mainSurface,self.xPos-20,self.yPos+10,fallingVelocity=10,startRight=False,hurtPlayer=True,speed=7))
                    else:
                        xDiff = character.xPos+character.characterWidth/2 - self.xPos
                        yDiff = character.yPos+character.characterHeight/2 - self.yPos

                        angle = math.degrees(math.atan2(yDiff, xDiff))
                        bullets.append(Bullet.Bullet(self.mainSurface, self.xPos-20, self.yPos, angle, image=Constants.Images.Bullet.bulletImage,
                                                 defaultImageAngle=-90, speed = 1.5,hurtPlayer = True))
                    self.animationSwitchCount = 0
                self.shootCount = 0


            self.animationSwitchCount += 1
            if ((self.shootCount >= (2/3) * self.shootTimerLimit) and character.xPos < self.xPos) or self.animationSwitchCount < 30:
                self.currentAnimation = self.shootingAnimation
            else:
                self.currentAnimation = self.idleAnimation
            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos,bullet.yPos):
                    self.dead = True
                    bullet.destroy = True
            self.setRects()
        else:
            if self.deadRunOnce:
                self.image = pygame.transform.scale(self.currentAnimation[0], (self.currentAnimation[0].get_width(), 25))
                self.yPos = self.yPos + self.height - 25
                self.deadRunOnce = False
                self.enemyRect = pygame.Rect(0,0,0,0)
            self.deathCount += 1
            if self.deathCount >= 60:
                self.delete = True

    def animationControl(self):
        self.animationCount += 1

        if self.animationCount >= len(self.currentAnimation):
            self.animationCount = 0

        self.image = self.currentAnimation[self.animationCount]


    def display(self):
        if not self.dead:
            self.animationControl()

        if self.image is not None:
            self.mainSurface.blit(self.image,(self.xPos,self.yPos))
        else:
            pygame.draw.rect(self.mainSurface,(255,0,0),self.enemyRect,0)
            print("lol")

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

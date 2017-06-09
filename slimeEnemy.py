import pygame
import tools
import Constants

class SlimeEnemy:
    mainSurface = None

    xPos = 0
    yPos = 0
    speed = 0

    width = 45
    height = 45

    dead = False
    deathCount = 0
    deadRunOnce = True

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

    tag = "slimeEnemy"

    movingAnimation = []
    animationCount = 0
    image = None

    delete = False

    def __init__(self, surface: pygame.Surface, x, y, speed=4):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.movingAnimation = Constants.Animations.SlimeEnemy.movingAnimation
        self.setRects()

    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topEnemyRect = pygame.Rect(self.xPos-12, self.yPos, self.width+24, 15) # Large top collison size to make enemy easy to kill
        self.leftEnemyRect = pygame.Rect(self.xPos, self.yPos, 10, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 10, self.yPos, 10, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    def control(self, platforms, bullets, character):
        if not self.dead:
            if self.collidingBottom(platforms):
                self.goingDown = False
                if self.goingLeft:
                    if self.collidingLeft(platforms):
                        self.goingRight = True
                        self.goingLeft = False
                    else:
                        self.xPos -= self.speed
                elif self.goingRight:
                    if self.collidingRight(platforms):
                        self.goingLeft = True
                        self.goingRight = False
                    else:
                        self.xPos += self.speed
            else:
                self.goingDown = True

            if self.goingDown:
                self.yPos += self.speed * 2

            self.setRects()

            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):
                    self.dead = True
                    bullet.destroy = True
        else:
            if self.deadRunOnce:
                self.image = pygame.transform.scale(self.movingAnimation[0], (self.movingAnimation[0].get_width(), 15))
                self.yPos = self.yPos + self.height - 15
                self.deadRunOnce = False
                self.enemyRect = pygame.Rect(0,0,0,0)
            self.deathCount += 1
            if self.deathCount >= 60:
                self.delete = True


    def animationControl(self):
        if self.animationCount >= len(self.movingAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.3

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


    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:
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
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkBottomCollide(self.topEnemyRect):
                    return True
        return False

    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomEnemyRect):
                    return True
        return False

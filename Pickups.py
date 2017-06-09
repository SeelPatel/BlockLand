import pygame
import Constants

class HealthPickup:
    mainSurface = None

    image = None
    goingDown = False

    xPos = 0
    yPos = 0

    width = 40
    height = 40

    tag = "health"

    mainRect = None

    picked = False

    def __init__(self,mainSurface : pygame.Surface,x: int,y : int):
        self.mainSurface = mainSurface
        self.xPos = x
        self.yPos = y

        self.image = pygame.transform.scale(Constants.Images.Heart.mainHeart,(self.width,self.height))

        self.setRects()

    def setRects(self):
        self.mainRect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)

    def control(self,platforms : list):
        if self.collidingBottom(platforms):
            self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
            self.goingDown = False
        else:
            self.goingDown = True

        if self.goingDown:
            self.yPos += 3

        self.setRects()

    def display(self):
        self.mainSurface.blit(self.image,(self.xPos,self.yPos))


    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):
                    return True
        return False

    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):
                    return platform
        return None


class FireBallPickup:
    mainSurface = None

    image = None
    goingDown = False

    xPos = 0
    yPos = 0

    width = 40
    height = 40

    tag = "fireball"

    mainRect = None

    picked = False

    def __init__(self,mainSurface : pygame.Surface,x: int,y : int):
        self.mainSurface = mainSurface
        self.xPos = x
        self.yPos = y

        self.image = pygame.transform.scale(Constants.Images.Bullet.fireBallImage,(self.width,self.height))

        self.setRects()

    def setRects(self):
        self.mainRect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)

    def control(self,platforms : list):
        if self.collidingBottom(platforms):
            self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
            self.goingDown = False
        else:
            self.goingDown = True

        if self.goingDown:
            self.yPos += 3

        self.setRects()

    def display(self):
        self.mainSurface.blit(self.image,(self.xPos,self.yPos))


    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):
                    return True
        return False

    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):
                    return platform
        return None

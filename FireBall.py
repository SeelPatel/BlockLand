import pygame

import Constants

class FireBall:
    mainSurface = None
    xPos = 0
    yPos = 0

    bounceCount = 0
    bounceMax = 15

    destroy = False

    width = 30
    height = 30

    mainRect = None
    bottomRect = None
    topRect = None
    rightRect = None
    leftRect = None

    image = None

    speed = 0

    fallingVelocity = 0

    goingRight = True
    goingLeft = True
    goingUp = False
    goingDown = True

    tag = "fireBall"

    hurtPlayer = False

    def __init__(self, surface: pygame.Surface, x, y, image : pygame.image =None, speed = 15,startRight = True,fallingVelocity=5
                 ,hurtPlayer = False):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y

        self.speed = speed

        if image == None:
            self.image = Constants.Images.Bullet.fireBallImage
        else:
            self.image = image

        self.setRects()

        self.goingRight = startRight
        self.goingLeft = not startRight

        self.hurtPlayer = hurtPlayer

        self.fallingVelocity = fallingVelocity

    def setRects(self):
        self.mainRect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)
        self.topRect = pygame.Rect(self.xPos + 5, self.yPos, self.width - 10, 15)
        self.bottomRect = pygame.Rect(self.xPos + 5, self.yPos + self.height / 2, self.width - 10, 15)
        self.leftRect = pygame.Rect(self.xPos, self.yPos + 5, 15, self.height - 10)
        self.rightRect = pygame.Rect(self.xPos + self.width / 2, self.yPos + 5, 15, self.height - 10)


    def control(self, platforms: list):
        if not self.destroy:
            if self.goingRight:
                if self.collidingRight(platforms):
                    self.goingRight = False
                    self.goingLeft = True
                    self.bounceCount += 1

                self.xPos += self.speed

            elif self.goingLeft:
                if self.collidingLeft(platforms):
                    self.goingLeft = False
                    self.goingRight = True
                    self.bounceCount += 1

                self.xPos -= self.speed

            if self.goingDown:
                if self.collidingBottom(platforms):
                    self.goingDown = False
                    self.goingUp = True
                    self.bounceCount += 1
                    if self.getCollidingBottomRect(platforms).tag == "deathPlatform":
                        self.destroy = True
                else:
                    self.fallingVelocity += 0.50
                    self.yPos += self.fallingVelocity

            elif self.goingUp:
                if self.fallingVelocity <= 0 or self.collidingTop(platforms):
                    self.goingDown = True
                    self.goingUp = False
                    self.fallingVelocity = 0
                    self.bounceCount += 1
                else:
                    self.fallingVelocity -= 0.50
                    self.yPos-= self.fallingVelocity

            if self.bounceCount > self.bounceMax:
                self.destroy = True

            self.setRects()


    def display(self):
        if self.image is not None:
            self.mainSurface.blit(self.image,(self.xPos,self.yPos))
        else:
            pygame.draw.circle(self.mainSurface, (255, 0, 0), [int(self.xPos + self.width/2), int(self.yPos+ self.height/2)], 15, 0)

    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:
                if platform.checkLeftCollide(self.rightRect) and platform.tag != "specSurface":
                    self.rightColliding = True
                    return True
        self.rightColliding = False
        return False

    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:
                if platform.checkRightCollide(self.leftRect) and platform.tag != "specSurface":
                    self.leftColliding = True
                    return True
        self.leftColliding = False
        return False

    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkBottomCollide(self.topRect) and platform.tag != "specSurface":
                    return True
        return False

    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomRect) and platform.tag != "specSurface":
                    return True
        return False

    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomRect) and platform.tag != "specSurface":
                    return platform
        return None
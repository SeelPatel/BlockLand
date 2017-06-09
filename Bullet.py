import pygame
import RectPlatform
import math


class Bullet:
    mainSurface = None
    xPos = 0
    yPos = 0
    angle = 0

    tickCount = 0

    destroy = False

    width = 10

    image = None
    defaultImageAngle = 0

    speed = 0

    tag = "bullet"

    hurtPlayer = False

    def __init__(self, surface: pygame.Surface, x, y, angle, image : pygame.image =None, defaultImageAngle=0, speed = 10,hurtPlayer=False):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.angle = angle

        self.speed = speed

        self.hurtPlayer = hurtPlayer

        self.image = image
        self.defaultImageAngle = defaultImageAngle

    def control(self, platforms: list):
        for x in range(25):
            self.xPos += (1- 1/self.speed) * math.cos(math.radians(self.angle))
            self.yPos += (1- 1/self.speed) * math.sin(math.radians(self.angle))
            for platform in platforms:
                if platform.fullRect.collidepoint(self.xPos, self.yPos):
                    self.destroy = True

        self.tickCount += 1
        if self.tickCount >= 900:  # keep bullets for 15 seconds
            self.destroy = True

    def display(self):

        if self.image is not None:
            rotatedImage = pygame.transform.rotate(self.image, self.defaultImageAngle + -self.angle)
            self.mainSurface.blit(rotatedImage,
                                  (self.xPos - rotatedImage.get_width() / 2, self.yPos - rotatedImage.get_height() / 2))

        else:
            pygame.draw.circle(self.mainSurface, (255, 0, 255), [int(self.xPos), int(self.yPos)], 5, 0)
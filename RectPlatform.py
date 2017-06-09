import pygame
from pygame.rect import Rect


class RectPlatform:
    tag = ""  # If tag is health then hitting this drops health
    droppedAlready = False

    originalImage = None
    color = None

    img = None
    xPos = 0
    yPos = 0
    width = 1
    height = 1

    mainSurface = None

    collideTopRect = None
    collideBottomRect = None
    collideLeftRect = None
    collideRightRect = None
    fullRect = None

    debug = False

    def __init__(self, surface: pygame.Surface, x, y, width, height, tag: str = "platform", image: pygame.image = None,
                 color: tuple = (255, 0, 0)):
        self.tag = tag
        self.xPos = x
        self.yPos = y
        self.width = width
        self.height = height
        self.mainSurface = surface
        self.color = color
        self.originalImage = image
        self.changeImageSize()

        self.setRects()

    def setRects(self):
        self.collideTopRect = Rect(self.xPos+5, self.yPos, self.width-10, 30)
        self.collideBottomRect = Rect(self.xPos+5, self.yPos + self.height - 20, self.width-10, 20)

        self.collideLeftRect = Rect(self.xPos, self.yPos + 10, 30, self.height-10)
        self.collideRightRect = Rect(self.xPos + self.width - 30, self.yPos + 10, 30, self.height - 10)

        self.fullRect = Rect(self.xPos, self.yPos, self.width, self.height)

    def display(self, surface=None):
        if surface == None:
            blitSurface = self.mainSurface
        else:
            blitSurface = surface
        if self.img != None:
            blitSurface.blit(pygame.transform.smoothscale(self.img, (self.width, self.height)),
                             (self.xPos, self.yPos))
        if self.debug:
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideTopRect, 1)
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideBottomRect, 1)
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideLeftRect, 1)
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideRightRect, 1)

    def setPos(self, x, y):
        self.xPos = x
        self.yPos = y
        self.setRects()

    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.changeImageSize()
        self.setRects()

    def changeImageSize(self):
        if self.originalImage != None:
            self.img = pygame.transform.smoothscale(self.originalImage, (self.width, self.height))

    def checkTopCollide(self, rect: Rect):
        if self.collideTopRect.colliderect(rect):
            return True
        return False

    def checkLeftCollide(self, rect: Rect):
        if self.collideLeftRect.colliderect(rect):
            return True
        return False

    def checkRightCollide(self, rect: Rect):
        if self.collideRightRect.colliderect(rect):
            return True
        return False

    def checkBottomCollide(self, rect: Rect):
        if self.collideBottomRect.colliderect(rect):
            return True
        return False

    def getY(self):
        return self.yPos

    def getX(self):
        return self.xPos

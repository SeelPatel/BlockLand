import pygame
import Character

class Background:
    character = None
    xPos = 0
    yPos = 0

    mainSurface = None

    background = None
    midground = None
    foreground = None

    backgroundSurface = None
    midgroundSurface = None
    foregroundSurface = None

    background = None
    midground = None
    foreground = None

    midCount = 0
    foreCount = 0

    clouds = None

    graveScene = False

    def __init__(self,surface : pygame.Surface,character : Character,x : int,y : int,graveScene=False):
        self.character = character
        self.xPos = x
        self.yPos = y

        self.mainSurface = surface
        self.graveScene = graveScene

        if not graveScene:
            self.background = pygame.image.load("sprites/background/background.png").convert()
            self.midground = pygame.image.load("sprites/background/backMountains.png")
            self.foreground = pygame.image.load("sprites/background/treeLine.png")
        else:
            self.background = pygame.image.load("sprites/background/graveBackground.png").convert()
            self.midground = pygame.image.load("sprites/background/graveMidground.png")
            self.foreground = pygame.image.load("sprites/background/graveForeground.png")

        self.initSurfaces()

    def initSurfaces(self):
        self.backgroundSurface = pygame.Surface(
            (self.background.get_width() * 2, self.background.get_height()))
        self.backgroundSurface.blit(self.background, (0, 0))
        self.backgroundSurface.blit(self.background, (self.background.get_width(), 0))

        self.midgroundSurface = pygame.Surface((self.midground.get_width() * 2, self.midground.get_height()),
                                               pygame.SRCALPHA)
        self.midgroundSurface.blit(self.midground, (0, 0))
        self.midgroundSurface.blit(self.midground, (self.midground.get_width(), 0))


        self.foregroundSurface = pygame.Surface(
            (self.foreground.get_width() * 2, self.foreground.get_height()),
            pygame.SRCALPHA)
        self.foregroundSurface.blit(self.foreground, (0, 0))
        self.foregroundSurface.blit(self.foreground, (self.foreground.get_width(), 0))

    def control(self,x ,y):
        self.xPos = x
        self.yPos = y

        if not (self.character.goingRight and self.character.goingLeft):
            if self.character.goingRight and not self.character.rightColliding:
                self.foreCount += 5
                self.midCount += 2.5
                if self.foreCount >= 1000:
                    self.foreCount = 0
                if self.midCount >= 1000:
                    self.midCount = 0

            if self.character.goingLeft and not self.character.leftColliding:
                self.foreCount = self.foreCount - self.character.currentSpeed/2
                self.midCount = self.midCount - self.character.currentSpeed/4
                if self.foreCount < 0:
                    self.foreCount = 1000
                if self.midCount < 0:
                    self.midCount = 1000

    def display(self):
        if self.graveScene:
            self.mainSurface.blit(self.background,(self.xPos,self.yPos))
        else:
            self.mainSurface.blit(self.background, (self.xPos, self.yPos))
        self.mainSurface.blit(self.midgroundSurface.subsurface([self.midCount,0,1000,700]), (self.xPos, self.yPos))
        self.mainSurface.blit(self.foregroundSurface.subsurface([self.foreCount,0,1000,700]), (self.xPos, self.yPos))

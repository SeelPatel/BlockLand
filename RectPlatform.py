import pygame
from pygame.rect import Rect


class RectPlatform:
    # If tag is a powerup, this indicates which one it should drop,
    # Also indicates whether a ball should bounce of the surface or not
    tag = ""

    droppedAlready = False  # if the platform has pwoerup this indicates if its already dropped

    # The original image before scaling to fit
    originalImage = None
    # The color to display if an image is not provided
    color = None

    # Image to blit on the gamesurface
    img = None

    # position of the platform
    xPos = 0
    yPos = 0

    # size dimensions of the platform
    width = 1
    height = 1

    # surface that the plaform should be displayed on
    mainSurface = None

    # colliders used for objects to detect collisions with the platform
    collideTopRect = None
    collideBottomRect = None
    collideLeftRect = None
    collideRightRect = None
    fullRect = None  # used main more bullets to check if they should be destroy

    debug = False  # Game displays the colliders above if this is true

    # initialize the platform
    def __init__(self, surface: pygame.Surface, x, y, width, height, tag: str = "platform", image: pygame.image = None,
                 color: tuple = (255, 0, 0)):
        # set some variables that were inputted
        self.tag = tag
        self.xPos = x
        self.yPos = y
        self.width = width
        self.height = height
        self.mainSurface = surface
        self.color = color
        self.originalImage = image

        self.changeImageSize()  # change the image size to match the size of the platform

        self.setRects()  # set the colliders of the platforms based on the fed positional/dimensional arguments

    # Used to set the colliders of the platform
    def setRects(self):
        # for top and bottom collisions
        self.collideTopRect = Rect(self.xPos + 5, self.yPos, self.width - 10, 30)
        self.collideBottomRect = Rect(self.xPos + 5, self.yPos + self.height - 20, self.width - 10, 20)

        # for side collisions
        self.collideLeftRect = Rect(self.xPos, self.yPos + 10, 30, self.height - 10)
        self.collideRightRect = Rect(self.xPos + self.width - 30, self.yPos + 10, 30, self.height - 10)

        # used mainly for bullet collisions
        self.fullRect = Rect(self.xPos, self.yPos, self.width, self.height)

    # display the platform on the surface it was initialized with or a second provided surface
    def display(self, surface=None):  # if you don't want to display on the gameSurface, use the surface arguement
        if surface == None:
            blitSurface = self.mainSurface  # set gameSurface as the blitsurface if not new surface provided
        else:
            blitSurface = surface  # If new surface is provided change the blitSurface to the new surface
        if self.img != None:
            blitSurface.blit(self.img, (self.xPos, self.yPos))  # if an image was provided, display it
        if self.debug:  # display the colliders if the debug variable is set true
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideTopRect, 1)
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideBottomRect, 1)
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideLeftRect, 1)
            pygame.draw.rect(blitSurface, (0, 255, 0), self.collideRightRect, 1)

    # used to change position of the surface
    def setPos(self, x, y):
        # set position
        self.xPos = x
        self.yPos = y
        # reset colliders
        self.setRects()

    # used to change the size of the surface
    def setSize(self, width, height):
        # change the dimensions
        self.width = width
        self.height = height
        # rescale the image to fit the new dimensions
        self.changeImageSize()
        # reset the colliders
        self.setRects()

    # used to scale the image to fit the platform
    def changeImageSize(self):
        # if an orignal image exists, scale the image to display using it
        if self.originalImage is not None:
            self.img = pygame.transform.smoothscale(self.originalImage, (self.width, self.height))

    # Used to check top collision
    def checkTopCollide(self, rect: Rect):
        if self.collideTopRect.colliderect(rect):  # check collision with inputted rect using top collider
            return True
        return False

    # Used to check left collision
    def checkLeftCollide(self, rect: Rect):
        if self.collideLeftRect.colliderect(rect):  # check collision with inputted rect using left collider
            return True
        return False

    # Used to check right collision
    def checkRightCollide(self, rect: Rect):
        if self.collideRightRect.colliderect(rect):  # check collision with inputted rect using right collider
            return True
        return False

        # Used to check bottom collision

    def checkBottomCollide(self, rect: Rect):
        if self.collideBottomRect.colliderect(rect):  # check collision with inputted rect using bottom collider
            return True
        return False

import pygame

import Character

"""
This background uses the parallax effect to create a
surface that has a 3d effect. This is done by moving the foreground
and midground elements at different speeds.
"""


class Background:
    character = None  # Used to check if character is moving

    # X and Y Position to blit surface on
    xPos = 0
    yPos = 0

    # The surface to display the background on
    mainSurface = None

    # The background portion of the surface
    background = None

    # The midground portion of the surface
    midground = None

    # The foreground portion of the surface
    foreground = None

    # Surfaces to scroll through for backgrounds
    backgroundSurface = None
    midgroundSurface = None
    foregroundSurface = None

    # X Position for scrolling through surfaces
    midCount = 0
    foreCount = 0

    graveScene = False  # Indicates whether to use the grave level images

    # initialize background variables
    def __init__(self, surface: pygame.Surface, character: Character, x: int, y: int, graveScene=False):
        # Set some of the attributes from the variables passed in
        # Purpose of these variables is listed above
        self.character = character
        self.xPos = x
        self.yPos = y
        self.mainSurface = surface
        self.graveScene = graveScene

        # set surfaces based on which level the player is on
        if not graveScene:
            self.background = pygame.image.load("sprites/background/background.png").convert()
            self.midground = pygame.image.load("sprites/background/backMountains.png")
            self.foreground = pygame.image.load("sprites/background/treeLine.png")
        else:
            self.background = pygame.image.load("sprites/background/graveBackground.png").convert()
            self.midground = pygame.image.load("sprites/background/graveMidground.png")
            self.foreground = pygame.image.load("sprites/background/graveForeground.png")

        # Initialize surfaces to scroll through for background
        self.initSurfaces()

    # initialize surfaces
    def initSurfaces(self):
        # Create and fill background surface for scrolling
        self.backgroundSurface = pygame.Surface(
            (self.background.get_width() * 2, self.background.get_height()))
        self.backgroundSurface.blit(self.background, (0, 0))
        self.backgroundSurface.blit(self.background, (self.background.get_width(), 0))

        # Create and fill midground surface for scrolling
        self.midgroundSurface = pygame.Surface((self.midground.get_width() * 2, self.midground.get_height()),
                                               pygame.SRCALPHA)
        self.midgroundSurface.blit(self.midground, (0, 0))
        self.midgroundSurface.blit(self.midground, (self.midground.get_width(), 0))

        # Create and fill foreground surface for scrolling
        self.foregroundSurface = pygame.Surface(
            (self.foreground.get_width() * 2, self.foreground.get_height()),
            pygame.SRCALPHA)
        self.foregroundSurface.blit(self.foreground, (0, 0))
        self.foregroundSurface.blit(self.foreground, (self.foreground.get_width(), 0))

    # control the background
    def control(self, x, y):
        # Move the position to display background at
        self.xPos = x
        self.yPos = y

        # If the character is not going left and right (player pressing A and D)
        if not (self.character.goingRight and self.character.goingLeft):
            # Scroll background left if character moving right
            if self.character.goingRight and not self.character.rightColliding:
                # Change scroll position for surfaces
                self.foreCount += self.character.currentSpeed / 2
                self.midCount += self.character.currentSpeed / 4
                # Reset scroll count at specific points
                if self.foreCount >= 1000:
                    self.foreCount = 0
                if self.midCount >= 1000:
                    self.midCount = 0

            # Scroll background right if character moving right
            if self.character.goingLeft and not self.character.leftColliding:
                # Change scroll position for surfaces
                self.foreCount -= self.character.currentSpeed / 2
                self.midCount -= self.character.currentSpeed / 4
                # Reset scroll count at specific points
                if self.foreCount < 0:
                    self.foreCount = 1000
                if self.midCount < 0:
                    self.midCount = 1000

    # display the background
    def display(self):
        # Display background section
        self.mainSurface.blit(self.background, (self.xPos, self.yPos))

        # Display midground and foreground based on scroll values
        self.mainSurface.blit(self.midgroundSurface.subsurface([self.midCount, 0, 1000, 700]), (self.xPos, self.yPos))
        self.mainSurface.blit(self.foregroundSurface.subsurface([self.foreCount, 0, 1000, 700]), (self.xPos, self.yPos))

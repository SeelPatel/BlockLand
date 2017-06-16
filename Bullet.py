import math

import pygame


class Bullet:
    mainSurface = None  # Surface to put bullet on
    # Position for bullet
    xPos = 0
    yPos = 0

    # Angle at which bullet is shot
    angle = 0

    # Used to determine when to delete bullet if it doesnt hit anything
    tickCount = 0

    # if true, delete from bullet list
    destroy = False

    # Image for bullet
    image = None
    # Image angle to rotate image by default to get proper orientation
    defaultImageAngle = 0

    # Speed to move the bullet
    speed = 0

    width = 10  # used to determine if bullet is on screen

    # Tag to control bullet based on interactions
    tag = "bullet"

    # Determine whether the bullet hurts the player
    hurtPlayer = False

    # initialize bullet
    def __init__(self, surface: pygame.Surface, x, y, angle, image: pygame.image = None, defaultImageAngle=0, speed=10,
                 hurtPlayer=False):
        # Set some of the attributes from the variables passed in
        # Purpose of these variables is listed above
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.angle = angle

        self.speed = speed

        self.hurtPlayer = hurtPlayer

        self.image = image
        self.defaultImageAngle = defaultImageAngle

    # control the bullet
    def control(self, platforms: list):
        # Move bullet incrementally 25 times and check if it hit a plaform
        for x in range(25):
            """
            calculate and add to position based on angle
            I do this by getting the trigonometric components from the angle
            """
            self.xPos += (1 - 1 / self.speed) * math.cos(math.radians(self.angle))
            self.yPos += (1 - 1 / self.speed) * math.sin(math.radians(self.angle))
            # Destroy bullet if it collides with a platform
            for platform in platforms:
                # Use collidepoint to check collision with platform
                if platform.fullRect.collidepoint(self.xPos, self.yPos):
                    self.destroy = True

        # if bullet exists for too long then destroy it
        self.tickCount += 1
        if self.tickCount >= 900:  # keep bullets for 15 seconds
            self.destroy = True

    # display the bullet
    def display(self):
        # if image is provided
        if self.image is not None:
            # Rotate the image based on the angle the bullet is shot at and the default image angle
            rotatedImage = pygame.transform.rotate(self.image, self.defaultImageAngle + -self.angle)
            self.mainSurface.blit(rotatedImage,
                                  (self.xPos - rotatedImage.get_width() / 2, self.yPos - rotatedImage.get_height() / 2))
        else:  # if image not provided draw circle
            pygame.draw.circle(self.mainSurface, (255, 0, 255), [int(self.xPos), int(self.yPos)], 5, 0)

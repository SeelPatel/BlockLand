import pygame

import Constants


class HealthPickup:
    # surface to display on
    mainSurface = None

    # image to display
    image = None

    # variable for movement control
    goingDown = False

    # Position of the pickup
    xPos = 0
    yPos = 0

    # size of the pickup
    width = 40
    height = 40

    # Tag of pickup for player interaction
    tag = "health"

    # Rect for player collisions
    mainRect = None

    # Varible to indicate deletion and decide if the pickup has been picked
    picked = False

    # initialize the pickup
    def __init__(self, mainSurface: pygame.Surface, x: int, y: int):
        # set some variables
        self.mainSurface = mainSurface
        self.xPos = x
        self.yPos = y

        # get image from constants
        self.image = pygame.transform.scale(Constants.Images.Heart.mainHeart, (self.width, self.height))

        # set colliders from initial position
        self.setRects()

    # Set colliders for interaction
    def setRects(self):
        self.mainRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)

    # Control the movement of the pickup
    def control(self, platforms: list):
        # if the pickup hits a platform
        if self.collidingBottom(platforms):
            # set the pickup right on top of the platform
            self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
            self.goingDown = False  # stop it from falling
        else:
            self.goingDown = True  # if not colliding make it fall

        if self.goingDown:  # if falling add to the y Position to move it
            self.yPos += 3

        self.setRects()  # Set colliders from new positions

    # display pickup
    def display(self):  # display the pickup to the screen
        self.mainSurface.blit(self.image, (self.xPos, self.yPos))

    # check if the pickup hits the floor
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            # check if the pickup is in range
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):  # check for the collision
                    return True  # return true if colliding
        return False  # false if not colliding

    # get the rect that the pickup is hitting
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            # check if the pickup is in range
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):  # check if colliding
                    return platform  # return the platform that the pickups is collding with
        return None


class FireBallPickup:
    # surface to display on
    mainSurface = None

    # image to display
    image = None

    # variable for movement control
    goingDown = False

    # Position of the pickup
    xPos = 0
    yPos = 0

    # size of the pickup
    width = 40
    height = 40

    # Tag of pickup for player interaction
    tag = "fireball"

    # Rect for player collisions
    mainRect = None

    # Varible to indicate deletion and decide if the pickup has been picked
    picked = False

    # initialize the pickup
    def __init__(self, mainSurface: pygame.Surface, x: int, y: int):
        # set some variables
        self.mainSurface = mainSurface
        self.xPos = x
        self.yPos = y

        # get image from constants
        self.image = pygame.transform.scale(Constants.Images.Bullet.fireBallImage, (self.width, self.height))

        # set colliders from initial position
        self.setRects()

    # Set colliders for interaction
    def setRects(self):
        self.mainRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)

    # Control the movement of the pickup
    def control(self, platforms: list):
        # if the pickup hits a platform
        if self.collidingBottom(platforms):
            # set the pickup right on top of the platform
            self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
            self.goingDown = False  # stop it from falling
        else:
            self.goingDown = True  # if not colliding make it fall

        if self.goingDown:  # if falling add to the y Position to move it
            self.yPos += 3

        self.setRects()  # Set colliders from new positions

    # display pickup
    def display(self):  # display the pickup to the screen
        self.mainSurface.blit(self.image, (self.xPos, self.yPos))

    # check if the pickup hits the floor
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            # check if the pickup is in range
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):  # check for the collision
                    return True  # return true if colliding
        return False  # false if not colliding

    # get the rect that the pickup is hitting
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            # check if the pickup is in range
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.mainRect):  # check if colliding
                    return platform  # return the platform that the pickups is collding with
        return None

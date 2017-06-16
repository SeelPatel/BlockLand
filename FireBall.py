import pygame

import Constants


class FireBall:
    # surface to display on
    mainSurface = None

    # Position of ball
    xPos = 0
    yPos = 0

    # used to count number of bounces
    bounceCount = 0
    bounceMax = 15  # max amount of bounces

    # used to set ball for deletion
    destroy = False

    # dimensions of the ball
    width = 30
    height = 30

    # colliders for the ball
    mainRect = None
    bottomRect = None
    topRect = None
    rightRect = None
    leftRect = None

    # image for the ball
    image = None

    # speed of the ball
    speed = 0

    # the velocity of the ball
    fallingVelocity = 0

    # the moving directions of the ball
    goingRight = True
    goingLeft = True
    goingUp = False
    goingDown = True

    # tag for ball interaction with other game objects
    tag = "fireBall"

    # indicates whether ball hurts player
    hurtPlayer = False

    # initialize balls
    def __init__(self, surface: pygame.Surface, x, y, image: pygame.image = None, speed=15, startRight=True,
                 fallingVelocity=5
                 , hurtPlayer=False):
        # setup some variables
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y

        self.speed = speed

        # set images based on provided input
        if image == None:
            self.image = Constants.Images.Bullet.fireBallImage
        else:
            self.image = image

        # set colliders for ball
        self.setRects()

        # set starting direction
        self.goingRight = startRight
        self.goingLeft = not startRight

        self.hurtPlayer = hurtPlayer

        # set initial velocity
        self.fallingVelocity = fallingVelocity

    # set colliders
    def setRects(self):
        self.mainRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)

        self.topRect = pygame.Rect(self.xPos + 5, self.yPos, self.width - 10, 15)
        self.bottomRect = pygame.Rect(self.xPos + 5, self.yPos + self.height / 2, self.width - 10, 15)
        self.leftRect = pygame.Rect(self.xPos, self.yPos + 5, 15, self.height - 10)
        self.rightRect = pygame.Rect(self.xPos + self.width / 2, self.yPos + 5, 15, self.height - 10)

    # control ball
    def control(self, platforms: list):
        # if the ball is not set for deletion
        if not self.destroy:
            # if the ball is going right
            if self.goingRight:
                if self.collidingRight(platforms):
                    self.goingRight = False
                    self.goingLeft = True
                    self.bounceCount += 1

                self.xPos += self.speed
            # if the ball is going left
            elif self.goingLeft:
                if self.collidingLeft(platforms):
                    self.goingLeft = False
                    self.goingRight = True
                    self.bounceCount += 1

                self.xPos -= self.speed

            # if the ball is going down
            if self.goingDown:
                # switch to going up if ball hits platform
                if self.collidingBottom(platforms):
                    self.goingDown = False
                    self.goingUp = True
                    self.bounceCount += 1
                    # if ball hits the death platform ( falls of the map ), delete it
                    if self.getCollidingBottomRect(platforms).tag == "deathPlatform":
                        self.destroy = True
                else:
                    # accelerate ball while falling, by adding to velocity
                    self.fallingVelocity += 0.50
                    self.yPos += self.fallingVelocity  # add velocity to position to move ball

            # if the ball is going up
            elif self.goingUp:
                # switch direction if ball hits platform
                # or if the velocity reaches 0 due to acceleration
                if self.fallingVelocity <= 0 or self.collidingTop(platforms):
                    self.goingDown = True
                    self.goingUp = False
                    # reset velocity
                    self.fallingVelocity = 0
                    self.bounceCount += 1  # add to bounce count
                else:
                    # ball decelerates while going up
                    self.fallingVelocity -= 0.50  # removing from velocity while going up
                    self.yPos -= self.fallingVelocity  # adding the velocity to position to move it

            # destroy ball if it bounces to much
            if self.bounceCount > self.bounceMax:
                self.destroy = True

            # set colliders based on new position
            self.setRects()

    # display ball
    def display(self):
        if self.image is not None:
            # display ball picture if the image exists
            self.mainSurface.blit(self.image, (self.xPos, self.yPos))
        else:  # display circle for ball if image does not exist
            pygame.draw.circle(self.mainSurface, (255, 0, 0),
                               [int(self.xPos + self.width / 2), int(self.yPos + self.height / 2)], 15, 0)

    # check right collisions
    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:  # check if platform in range
                # check collision and return true if collding and not a special surface
                if platform.checkLeftCollide(self.rightRect) and platform.tag != "specSurface":
                    return True
        return False

    # check left collisions
    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:  # check if platform in range
                # check collision and return true if collding and not a special surface
                if platform.checkRightCollide(self.leftRect) and platform.tag != "specSurface":
                    return True
        return False

    # check top collisions
    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # check if platform in range
                # check collision and return true if collding and not a special surface
                if platform.checkBottomCollide(self.topRect) and platform.tag != "specSurface":
                    return True
        return False

    # check bottom collisions
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # check if platform in range
                # check collision and return true if collding and not a special surface
                if platform.checkTopCollide(self.bottomRect) and platform.tag != "specSurface":
                    return True
        return False

    # get the platform the ball collided with at the bottom
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # check if platform in range
                # check collision and return platform if collding and not a special surface
                if platform.checkTopCollide(self.bottomRect) and platform.tag != "specSurface":
                    return platform
        return None

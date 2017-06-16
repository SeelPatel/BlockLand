import pygame

import Constants


# slime enemy stays between two platforms and switches direction if it hits one
class SlimeEnemy:
    # the surface the enemy should be displayed on
    mainSurface = None

    # position of the enemy ( top left )
    xPos = 0
    yPos = 0

    # speed the enemy is set to move at
    speed = 0

    # dimensions of the enemy
    width = 45
    height = 45

    # variables for enemy death
    dead = False  # indicates if its dead
    deathCount = 0  # used to indicate when to mark for deletion
    deadRunOnce = True  # used to run some code only once on death

    # indicates current movement directions
    goingLeft = True
    goingRight = False
    goingDown = True

    # indicates if its colliding in either direction
    leftColliding = False
    rightColliding = False

    # colliders for player interactions
    enemyRect = None  # used for bullets

    # for environment collisions
    rightEnemyRect = None
    leftEnemyRect = None

    # for death and player interactions
    topEnemyRect = None

    # for collision with floor
    bottomEnemyRect = None

    # tag for player interactions
    tag = "slimeEnemy"

    # main animation of enemy
    movingAnimation = []
    animationCount = 0  # count to iterate through animation
    image = None  # image to display to gamesurface

    delete = False  # used to mark enemy for deletion

    # initialize the enemy
    def __init__(self, surface: pygame.Surface, x, y, speed=4):
        # set some variables for inputted arguments
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed

        # get the animation from constants
        self.movingAnimation = Constants.Animations.SlimeEnemy.movingAnimation

        # set the colliders based on initial position
        self.setRects()

    # set the enemy colliders
    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topEnemyRect = pygame.Rect(self.xPos - 12, self.yPos, self.width + 24,
                                        15)  # Large top collison size to make enemy easy to kill
        self.leftEnemyRect = pygame.Rect(self.xPos, self.yPos, 10, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 10, self.yPos, 10, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    # control the enemy
    def control(self, platforms, bullets, character):
        if not self.dead:  # if the enemy isnt dead
            if self.collidingBottom(platforms):  # if the character is on a platform
                self.goingDown = False  # dont allow it to go down
                if self.goingLeft:  # if the enemy is going left
                    if self.collidingLeft(platforms):  # if it hits a platform to the left
                        # switch the movement direction
                        self.goingRight = True
                        self.goingLeft = False
                    else:
                        # if not hittiing an object, move the enemy left
                        self.xPos -= self.speed

                elif self.goingRight:  # if the enemy is going right
                    if self.collidingRight(platforms):  # if it hits a platform to the right
                        # switch movement direction
                        self.goingLeft = True
                        self.goingRight = False
                    else:
                        # if not hitting a platform, move the enemy right
                        self.xPos += self.speed
            else:
                # if the enemy is not on top of a platform, set it as falling
                self.goingDown = True

            # if the enemy is falling
            if self.goingDown:
                # make the enemy go down
                self.yPos += self.speed * 2

            # set the colliders based on the new positions
            self.setRects()

            # check for bulelt collision
            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):  # if bullet hits enemy
                    self.dead = True  # kill the enemy
                    bullet.destroy = True  # set bullet for deletion
        else:  # if the enemy is dead
            if self.deadRunOnce:  # run once on death
                # set death image and scale it to give squished appearence
                self.image = pygame.transform.scale(self.movingAnimation[0], (self.movingAnimation[0].get_width(), 15))
                self.yPos = self.yPos + self.height - 15  # set y position base on squished appearence
                self.deadRunOnce = False  # make sure this runs once
                self.enemyRect = pygame.Rect(0, 0, 0, 0)  # avoid any character collisions

            self.deathCount += 1  # add to death count to determine deletion time
            if self.deathCount >= 60:  # if the enemy has been dead for 60 ticks
                self.delete = True  # set it for deletion

    # control the animations of the character
    def animationControl(self):
        # if the animation is finished,reset it
        if self.animationCount >= len(self.movingAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.3  # add 0.3 to progess animation slower

        # set the image based on current position within animation
        self.image = self.movingAnimation[int(self.animationCount)]

    # display the enemy
    def display(self):
        # if not dead then control the animation
        if not self.dead:
            self.animationControl()

        # if an image is provided
        if self.image is not None:
            if self.goingLeft:  # if going left, display image
                self.mainSurface.blit(self.image, (
                    self.xPos, self.yPos + 3))  # Add 3 because the image normally is off the ground a little
            else:  # if going right then flip and display the image
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos, self.yPos + 3))
        else:
            # if no image is provided draw a rectangle
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)

    # check collision to the right
    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:  # Check if the enemy is in range
                if platform.checkLeftCollide(self.rightEnemyRect):  # check collision
                    self.rightColliding = True  # set collding right as true
                    return True  # return true if colliding right
        # return and set as false if not collding
        self.rightColliding = False
        return False

    # check collision to the left
    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:  # Check if the enemy is in range
                if platform.checkRightCollide(self.leftEnemyRect):  # check collision
                    # set true and return true if collding left
                    self.leftColliding = True
                    return True
        # set false and return false if collding left
        self.leftColliding = False
        return False

    # check collision at the bottom
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # Check if the enemy is in range
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return True  # return true if collding
        return False  # return false if colliding

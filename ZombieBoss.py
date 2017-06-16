import pygame

import Constants
import FireBall
import tools


class ZombieEnemy:
    # surface to display the enemy on
    mainSurface = None

    # position of enemy ( top left )
    xPos = 0
    yPos = 0

    # speed of enemy
    speed = 0

    # dimensions of the enemy
    width = 150
    height = 240

    # variables for character death
    dead = False  # indicates if dead
    deadRunOnce = True  # used to run code once on death
    deathCount = 0  # used to delete enemy if its dead for too long
    delete = False  # used to mark enemy for deletion
    deathImage = None  # image to display after death
    deathY = 0  # holds Y position after death

    # indicate movement direction
    goingLeft = True
    goingRight = False
    goingDown = True

    # indicates if the enemy is colliding
    leftColliding = False
    rightColliding = False

    # colliders for the enemy
    enemyRect = None  # used for character interaction
    # used for side collisions
    rightEnemyRect = None
    leftEnemyRect = None
    # used for taking damage
    topEnemyRect = None
    # used to collide on floor
    bottomEnemyRect = None

    # tag for character interactions
    tag = "zombieBoss"

    # animation for movement
    movingAnimation = []
    animationCount = 0  # user to iterate through animations
    image = None  # Used to store image to display

    # used to store current animation
    currentAnimation = []

    # used to store player health
    health = 10

    # shoot count used to determine when the zombie should shoot
    shootCount = 0
    shootCountLimit = 180  # if shoot count reaches 180 ticks, shoot

    # Used to indicate the direction the enemy is facing
    facingLeft = True
    facingRight = False

    # initialize the enemy
    def __init__(self, surface: pygame.Surface, x, y, speed=4, health=10):
        # set some variables from the inputted variables
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.setRects()
        self.health = health

        # get and scale the animation from constants
        self.movingAnimation = tools.scaleImages(Constants.Animations.ZombieEnemy.movingAnimation, 3)

        # Set the animaton as the moving animation
        self.currentAnimation = self.movingAnimation

    # set the colliders for the enemy
    def setRects(self):
        # for character interactions
        self.enemyRect = pygame.Rect(self.xPos + 30, self.yPos + 10, self.width - 60, self.height - 10)
        self.topEnemyRect = pygame.Rect(self.xPos, self.yPos, self.width, 10)
        # for environment interactions
        self.leftEnemyRect = pygame.Rect(self.xPos - 20, self.yPos, 30, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 20, self.yPos, 30, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    # control the enemy
    def control(self, platforms, bullets, character):
        if not self.dead:  # if enemy is not dead
            # kill enemy if health is gone
            if self.health <= 0:
                self.dead = True

            # if the enemy is not inside the character area
            if not (character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth):
                if character.xPos >= self.xPos + self.width / 2:  # If the character is to the right of the enemy
                    # make character face right
                    self.facingRight = True
                    self.facingLeft = False
                elif character.xPos <= self.xPos + self.width / 2:  # If the character is to the left of the enemy
                    # make character face left
                    self.facingLeft = True
                    self.facingRight = False

            # If the enemy is colliding with the floor
            if self.collidingBottom(platforms):
                # set the enemy position above the platform
                self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
                # stop the enemy from going down
                self.goingDown = False
                # if the character fell of the map, kill it
                if self.getCollidingBottomRect(platforms).tag == "deathPlatform":
                    self.dead = True

                # if the enemy is not inside the character area
                if not (character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth):
                    # if the character is to the right of the enemy
                    if character.xPos > self.xPos:
                        # make the enemy go right
                        self.goingRight = True
                        self.goingLeft = False
                    # if the character is to the left of the enemy
                    elif character.xPos < self.xPos:
                        # make the enemy go left
                        self.goingLeft = True
                        self.goingRight = False
                else:
                    # if the enemy is inside the character area stop movement
                    self.goingLeft = False
                    self.goingRight = False
            else:
                # if the enemy is not on the floor, stop movement, and make enemy fall
                self.goingLeft = False
                self.goingRight = False
                self.goingDown = True

            # if the character is going right
            if self.goingRight:
                if not self.collidingRight(platforms):  # if the character is not colliding to the right
                    self.xPos += self.speed  # move the enemy right

            # if the character is going left
            if self.goingLeft:
                if not self.collidingLeft(platforms):  # if the character is not colliding to the left
                    self.xPos -= self.speed  # move the enemy left

            # if the character is going down
            if self.goingDown:
                self.yPos += self.speed  # move the enemy down

            # if the shoot count reaches the limit
            if self.shootCount >= self.shootCountLimit:
                self.shootCount = 0  # reset the limit
                if self.facingRight:  # if facing right, shoot a ball to the right
                    bullets.append(
                        FireBall.FireBall(self.mainSurface, self.xPos + self.width - 30, self.yPos + 85,
                                          hurtPlayer=True,
                                          startRight=True, speed=11))
                elif self.facingLeft:  # if facing left, shoot a ball to the left
                    bullets.append(
                        FireBall.FireBall(self.mainSurface, self.xPos + 30, self.yPos + 85, hurtPlayer=True,
                                          startRight=False, speed=11))
            self.shootCount += 1  # add to the count to count ticks

            self.setRects()  # set the colliders based on new position
        else:  # if enemy is dead
            if self.deadRunOnce:  # run once on death
                self.deathImage = self.movingAnimation[0]  # set the death image
                self.deathY = self.yPos  # set the starting death Y
                self.deadRunOnce = False  # make sure this runs once only
                self.enemyRect = pygame.Rect(0, 0, 0, 0)  # Make sure no more player damage interactions

            self.deathCount += 1  # add to deathcount
            # rotate and set image based on deathcount
            self.image = pygame.transform.rotate(self.deathImage, self.deathCount * 3 // 2)
            # set Y position based on deathcount
            self.yPos = self.deathY + self.deathCount * 3 // 2

            # mark for deletion after 60 ticks of death
            if self.deathCount >= 60:
                self.delete = True

    # control animations
    def animationControl(self):
        # reset animation after it end of list is reached
        if self.animationCount >= len(self.currentAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.3  # add to count to further animation (adding 0.3 slows animation)
        # set image to display
        self.image = self.currentAnimation[int(self.animationCount)]

    # display enemy
    def display(self):
        if not self.dead:  # control animations if not dead
            self.animationControl()
        # if an image is provided
        if self.image is not None:
            if self.facingLeft:  # if facing left display flipped image
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos - 30, self.yPos - 60))
            else:  # if facing right display normal image
                self.mainSurface.blit(self.image, (
                    self.xPos - 30, self.yPos - 60))  # -30 and -60 to align the image properly
        else:  # if no image provided draw a rectangle
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)

    # check collision to the right
    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 700 < self.xPos:  # check if enemy is in range of platform
                if platform.checkLeftCollide(self.rightEnemyRect):  # check collision
                    # return and set true if colliding
                    self.rightColliding = True
                    return True
        # otherwise set and return false
        self.rightColliding = False
        return False

    # check collision to the left
    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:  # check if enemy is in range of platform
                if platform.checkRightCollide(self.leftEnemyRect):  # check collision
                    # return and set true if colliding
                    self.leftColliding = True
                    return True
        # otherwise set and return false
        self.leftColliding = False
        return False

    # check bottom collision
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # check if enemy is in range of platform
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return True  # return true if colliding
        #otherwise return false
        return False

    # get platform that is colliding on the bottom
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # check if enemy is in range of platform
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return platform  # return colliding platform
        # otherwise return nothing
        return None

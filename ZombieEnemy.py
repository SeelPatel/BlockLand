import pygame

import Constants


class ZombieEnemy:
    # surface to display the enemy on
    mainSurface = None

    # position of enemy ( top left )
    xPos = 0
    yPos = 0

    # speed of enemy
    speed = 0

    # dimensions of the enemy
    width = 50
    height = 80

    # variables for character death
    dead = False  # indicates if dead
    deadRunOnce = True  # used to run code once on death
    deathCount = 0  # used to delete enemy if its dead for too long
    delete = False  # used to mark enemy for deletion

    # indicate movement direction
    goingLeft = True
    goingRight = False
    goingDown = True

    # variables for jumping
    jumping = False  # indicates if enemy is jumping
    jumpHeight = 0  # counts current height of enemy when jumping
    maxJumpHeight = 200  # the max height the enemy can jump
    jumpTimer = 0  # times the jump
    jumpTimerMax = 150  # the max ticks the enemy can jump

    jumpingToReachPlayer = False  # indicates if the enemy is jumping to reach player
    reachPlayerJumpTimer = 0  # timer to count that jump

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

    # tag for player interactions
    tag = "zombieEnemy"

    # animation lists
    jumpingAnimation = []
    movingAnimation = []
    # used to iterate through animation
    animationCount = 0
    # image to display
    image = None

    # the current animation of the enemy
    currentAnimation = []

    # the health of the enemy
    health = 3

    # indicates which direction the enemy is facing
    facingLeft = True
    facingRight = False

    # initialize the enemy
    def __init__(self, surface: pygame.Surface, x, y, speed=6, health=3):
        # set some variables from inputs
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.setRects()  # set colliders with new values
        self.health = health

        # get animations from constants
        self.movingAnimation = Constants.Animations.ZombieEnemy.movingAnimation
        self.jumpingAnimation = Constants.Animations.ZombieEnemy.jumpingAnimation

        # set starting animation
        self.currentAnimation = self.movingAnimation

    # used to set colliders of enemy
    def setRects(self):
        # for character and environment interactions
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topEnemyRect = pygame.Rect(self.xPos, self.yPos, self.width, 10)
        # for environment interactions
        self.leftEnemyRect = pygame.Rect(self.xPos, self.yPos, 10, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 10, self.yPos, 10, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    # Used to control the enemy
    def control(self, platforms, bullets, character):
        if not self.dead:  # if enemy is not dead
            if self.health <= 0:  # kill enemy if no health
                self.dead = True

            # if the player is to the right of the enemy
            if character.xPos >= self.xPos:
                # set the enemy facing right
                self.facingRight = True
                self.facingLeft = False
            # if the player is to the left of the enemy
            elif character.xPos <= self.xPos:
                # set the enemy facing left
                self.facingLeft = True
                self.facingRight = False

            # if the enemy is on the floor and not jumping
            if self.collidingBottom(platforms) and not self.jumping:
                # set the y position to above the platform its on
                self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
                # stop the enemy from going down
                self.goingDown = False
                # if the enemy falls of the map, kill it
                if self.getCollidingBottomRect(platforms).tag == "deathPlatform":
                    self.dead = True
                # if the enemy is not within x area of the character
                if not (character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth):
                    if character.xPos > self.xPos:  # if the character is to the right of the enemy
                        # set enemy as going right
                        self.goingRight = True
                        self.goingLeft = False
                    elif character.xPos < self.xPos:  # if the character is to the left of the enemy
                        # set enemy as going left
                        self.goingLeft = True
                        self.goingRight = False
                    # set the reach player timer to 0, so the enemy doesnt jump at character
                    self.reachPlayerJumpTimer = 0
                else:
                    # if the enemy within the x area of the character
                    # stop it from moving sideways
                    self.goingLeft = False
                    self.goingRight = False
                    # add to the reach player jump timer
                    self.reachPlayerJumpTimer += 1

                    # if the player is below the enemy and the reach player jump timer is greater than 20
                    if character.yPos < self.yPos and self.reachPlayerJumpTimer >= 20:
                        # jump to reach player
                        self.jumping = True
                        self.jumpHeight = 0  # reset jump height counter
                        self.jumpingToReachPlayer = True  # indicate that enemy is jumping to reach player

            else:  # if the enemy is not on the floor
                if not self.jumping:  # if not jumping, make enemy drop
                    self.goingDown = True
                self.goingLeft = False  # stop enemy from moving left or right
                self.goingRight = False

            # if enemy is set going right
            if self.goingRight:
                if self.collidingRight(platforms):  # if it collides into a platform to the right
                    if self.jumpTimer >= self.jumpTimerMax:  # if it hasnt jumped recently
                        # make the enemy jump
                        self.jumping = True
                        self.jumpHeight = 0  # reset count for how high enemy has jumped
                        self.jumpTimer = 0  # reset timer to decide when to jump again
                else:
                    self.xPos += self.speed  # if not colliding on the right, move the enemy to the right

            # if the enemy is st going left
            if self.goingLeft:
                if self.collidingLeft(platforms):  # if it collides to the left
                    if self.jumpTimer >= self.jumpTimerMax:  # if it hasnt jumped recently
                        # make the enemy jump
                        self.jumping = True
                        self.jumpHeight = 0  # reset count for how high enemy has jumped
                        self.jumpTimer = 0  # reset timer to decide when to jump again
                else:
                    self.xPos -= self.speed  # if not colliding on the right, move the enemy to the right

            # if the enemy is not jumping and is falling
            if self.goingDown and not self.jumping:
                self.yPos += self.speed * 1.5  # move the enemy down

            # if the enemy is jumping
            if self.jumping:
                # set the animation to the jumping animation
                self.currentAnimation = self.jumpingAnimation

                # Move the enemy up
                self.yPos -= self.speed * 1.5
                # make sure its not going down
                self.goingDown = False
                # add to the jump height
                self.jumpHeight += self.speed * 1.5

                if not self.jumpingToReachPlayer:  # if jumping normally
                    # if the enemy stops collding left or right stop jumping ( this lets enemy climb objects )
                    # if the enemy reaches a max jump height, stop it from jumping
                    if (not self.collidingRight(platforms) and (not self.collidingLeft(platforms)) or (
                                self.jumpHeight >= self.maxJumpHeight)):
                        self.jumping = False

                # if the enemy is jumping to reach the plyaer
                # and it hits a platform or reaches a jump height limit
                # stop it from jumping
                if (self.jumpingToReachPlayer and self.jumpHeight >= self.maxJumpHeight) or (
                        self.collidingTop(platforms)):
                    self.reachPlayerJumpTimer = 0  # reset timer to determine when to jump at player again
                    self.jumping = False  # make the enemy stop jumping
                    self.jumpingToReachPlayer = False  # reset this to false

            else:
                # if the enemy is not jumping, play the moving animation
                self.currentAnimation = self.movingAnimation

            # check bullet collisions
            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):  # if a bullet hits the enemy
                    self.health -= 1  # take away health
                    bullet.destroy = True  # destroy the bullets

            self.jumpTimer += 1  # add to jump timer, to decide when to jump again

            # set the colliders based on the new position
            self.setRects()
        else:
            if self.deadRunOnce:  # run once when enemy dies
                # set the death image and scale it to seem squished
                self.image = pygame.transform.scale(self.movingAnimation[0], (self.movingAnimation[0].get_width(), 15))
                # set the enemy position based on squished appearance
                self.yPos += self.height
                self.deadRunOnce = False  # make sure this runs once
                # Makes sure there are no character interactions
                self.enemyRect = pygame.Rect(0, 0, 0, 0)
                self.topEnemyRect = pygame.Rect(0, 0, 0, 0)
            self.deathCount += 1  # add to death count
            # if the enemy has been dead for 60 ticks, mark it for deletion
            if self.deathCount >= 60:
                self.delete = True

    # control animations of the enemy
    def animationControl(self):
        # Reset animation if it ends
        if self.animationCount >= len(self.currentAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.3  # add to count to iterate through animation ( 0.3 for slow animation )

        # set image from current animation
        self.image = self.currentAnimation[int(self.animationCount)]

    # display the character
    def display(self):
        # if not dead then control the animation
        if not self.dead:
            self.animationControl()

        # if an image is provided
        if self.image is not None:
            if self.facingLeft:  # if facing left, display the flipped image
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos - 5, self.yPos - 18))

            else:  # if facing right, display the normal image
                self.mainSurface.blit(self.image, (
                    self.xPos - 5, self.yPos - 18))  # -5 and -18 to align the image properly
        else:
            # if no image is not provided, draw a rectangle
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)

    # check right collision
    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:  # if the enemy is in range
                if platform.checkLeftCollide(self.rightEnemyRect):  # check collision
                    # set and return true if colliding
                    self.rightColliding = True
                    return True
        # otherwise set and return false
        self.rightColliding = False
        return False

    # check left collision
    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:  # if the enemy is in range
                if platform.checkRightCollide(self.leftEnemyRect):  # check collision
                    # set and return true if colliding
                    self.leftColliding = True
                    return True
        # otherwise set and return false
        self.leftColliding = False
        return False

    # check top collision
    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if the enemy is in range
                if platform.checkBottomCollide(self.topEnemyRect):  # check collision
                    return True  # return true if colliding
        return False  # return false otherwise

    # check bottom collision
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if the enemy is in range
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return True  # return true if colliding
        return False  # otherwise return false

    # get the platform that is being colldided with on the bottom
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if the enemy is in range
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return platform  # return platform that is being collided with
        return None  # otherwise return none

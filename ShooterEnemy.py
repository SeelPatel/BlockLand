import math

import pygame

import Bullet
import Constants
import FireBall


class ShooterEnemy:
    # the surface to display the enemy on
    mainSurface = None

    # the position of the enemy( top left )
    xPos = 0
    yPos = 0

    # The falling speed of the enemy
    fallSpeed = 5

    # the necessary colliders for the enemy
    enemyRect = None  # For bullets and player hit
    bottomEnemyRect = None  # for hitting the floor
    topEnemyRect = None  # for player interaction and death

    # size of the enemy
    width = 60
    height = 80

    # indicates movement direction
    goingDown = True

    # variables for death
    dead = False  # indicates the enemy is dead
    deadRunOnce = True  # used to run some code once on enemy death
    deathCount = 0  # count used to mark enemy for deletion after 60 ticks

    # used to mark enemy for deletion from the enemy list
    delete = False

    # tag used to control player interactions
    tag = "shooterEnemy"

    # used to time how often the enemy shoots at player
    shootCount = 0
    shootTimerLimit = 150  # the enemy shoots once every 150 ticks

    shootBalls = False  # checks if the enemy should shoot balls or bullets

    image = None  # the image of the enemy to display
    currentAnimation = None  # the current animation of the enemy
    animationCount = 0  # used to iterate through animation

    animationSwitchCount = 31  # indicates how much time passes before animation switches

    idleAnimation = None  # animation when idle
    shootingAnimation = None  # animation when shooting

    # used to initialize the enemy
    def __init__(self, surface: pygame.Surface, x: int, y: int, fallSpeed: int = 5, shootBalls=False):
        # set some variables from inputted values
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y

        self.fallSpeed = fallSpeed

        self.shootBalls = shootBalls

        # set the colliders based on the new position provided
        self.setRects()

        # get the animations from the constants files
        self.shootingAnimation = Constants.Animations.ShooterEnemy.shootingAnimation
        self.idleAnimation = Constants.Animations.ShooterEnemy.idleAnimation

    # set the colliders for the enemy
    def setRects(self):
        # used for character and bullet interaction
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        # used for floor collision
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 20, self.width, 20)
        # used for character interaction and death
        self.topEnemyRect = pygame.Rect(self.xPos, self.yPos, self.width, 20)

    # used to control the enemy movement
    def control(self, platforms, bullets, character):
        if not self.dead:  # If the enemy is not dead
            if not self.collidingBottom(platforms):  # if the enemy is not on the floor, set it as falling
                self.goingDown = True

            # if the enemy is going down
            if self.goingDown:
                self.yPos += self.fallSpeed  # move the enemy down
                if self.collidingBottom(platforms):  # if it hits a platform
                    # set it atop the platform
                    self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
                    # stop it from going down
                    self.goingDown = False
            # add to shootcount to determine if it should shoot
            self.shootCount += 1
            # if the shoot count exceed the timer limit, shoot projectiles
            if self.shootCount >= self.shootTimerLimit:
                # only shoot if the character is to the left of the enemy
                if character.xPos + character.characterWidth / 2 < self.xPos:
                    if self.shootBalls:  # if enemy was told to shoot balls, shoot a ball to the left
                        bullets.append(
                            FireBall.FireBall(self.mainSurface, self.xPos - 20, self.yPos + 10, fallingVelocity=10,
                                              startRight=False, hurtPlayer=True, speed=7))
                    else:
                        # if the enemy was told to shoot bullets
                        # get the distance in both axis from enemy to character
                        xDiff = character.xPos + character.characterWidth / 2 - self.xPos
                        yDiff = character.yPos + character.characterHeight / 2 - self.yPos

                        # use trig to get the angle between the player and the enemy
                        angle = math.degrees(math.atan2(yDiff, xDiff))
                        # shoot a bullet towards the player at the angle calculated above
                        bullets.append(Bullet.Bullet(self.mainSurface, self.xPos - 20, self.yPos, angle,
                                                     image=Constants.Images.Bullet.bulletImage,
                                                     defaultImageAngle=-90, speed=1.5, hurtPlayer=True))
                    # reset the animation count,
                    self.animationSwitchCount = 0
                # reset the timer to decide when to shoot
                self.shootCount = 0

            # add to the animation switch count
            self.animationSwitchCount += 1
            # if the enemy is getting ready to shoot and the player is to the left,
            # or for 30 seconds after the enemy shoots
            # set the animation to the shooting animation
            if ((self.shootCount >= (2 / 3) * self.shootTimerLimit)
                and character.xPos < self.xPos) or self.animationSwitchCount < 30:
                self.currentAnimation = self.shootingAnimation
            else:
                # if none of the above is true, set it to the idle animation
                self.currentAnimation = self.idleAnimation

            # control the bullet interactions
            for bullet in bullets:  # for all the bullets
                if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):  # check collision with collider
                    self.dead = True  # set to dead if hit
                    bullet.destroy = True  # mark bullet for destruction

            self.setRects()  # set the colliders based on any changed positions

        else:  # if the enemy is dead
            if self.deadRunOnce:
                # set the death image and scale down the height, to indicate that it got squished
                self.image = pygame.transform.scale(self.currentAnimation[0],
                                                    (self.currentAnimation[0].get_width(), 25))
                # set the y Position based on squished image
                self.yPos = self.yPos + self.height - 25
                # Let this code run only once
                self.deadRunOnce = False
                # make sure no further collisions can occur after enemy is dead
                self.enemyRect = pygame.Rect(0, 0, 0, 0)

            self.deathCount += 1  # add to deathcount
            # if the death lasts for 60 ticks, mark enemy for deletion
            if self.deathCount >= 60:
                self.delete = True

    # control the animation
    def animationControl(self):
        self.animationCount += 1  # progress through the current animation

        # if outside length of animation, reset it
        if self.animationCount >= len(self.currentAnimation):
            self.animationCount = 0

        # set the image of the enemy based on the current animation
        self.image = self.currentAnimation[self.animationCount]

    # display the enemy
    def display(self):
        # control animation if the enemy isnt dead
        if not self.dead:
            self.animationControl()
        # if there is an image provided, display it
        if self.image is not None:
            self.mainSurface.blit(self.image, (self.xPos, self.yPos))
        else:  # otherwise display a rectangle
            pygame.draw.rect(self.mainSurface, (255, 0, 0), self.enemyRect, 0)

    # check bottom collisions
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if the enemy is in range
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return True  # return true if colliding
        return False  # otherwise false

    # get platform enemy is colliding with on the bottom
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if the enemy is in range
                if platform.checkTopCollide(self.bottomEnemyRect):  # check collision
                    return platform  # return platform that the enemy is colliding on
        return None  # otherwise return none

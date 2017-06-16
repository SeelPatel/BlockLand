import pygame

import Constants


class GhostEnemy:
    # surface to displau enemy
    mainSurface = None

    # position of enemy
    xPos = 0
    yPos = 0

    # speed of enemy
    speed = 0

    # dimensions of enemy
    width = 50
    height = 50

    # variables for enemy death
    dead = False  # if enemy is dead
    deadRunOnce = True  # run once when enemy dies
    deathCount = 0  # counter for deletion
    deathImage = None  # image for death

    # used to mark for deletion
    delete = False

    # used to indicate movement direction
    goingRight = False
    goingLeft = False

    # colliders for the enemy
    enemyRect = None
    topEnemyRect = None

    # tag for interactions with other game objects
    tag = "ghostEnemy"

    # main animation
    movingAnimation = []
    animationCount = 0  # animation position indicator
    image = None  # Image to display to game surface

    # initialize the enemy
    def __init__(self, surface: pygame.Surface, x, y, speed=4):
        # Intialize some variables for the enemy
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.setRects()  # Set the colliders for the enemy

        # Get animations from the constants file
        self.movingAnimation = Constants.Animations.GhostEnemy.movingAnimation

    # Set the colliders
    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topEnemyRect = pygame.Rect(self.xPos - 20, self.yPos, self.width + 40, 25)

    # Function to control the enemy
    def control(self, platforms, bullets, character):
        # Do normal controls if the enemy is not dead
        if not self.dead:
            # if the enemy is not within the y range of the character
            if not character.yPos <= self.yPos + self.height / 2 <= character.yPos + character.characterHeight:
                if character.yPos < self.yPos + self.height / 2:  # if the character is below the enemy
                    self.yPos -= self.speed  # make the enemy going down
                elif character.yPos > self.yPos + self.height / 2:  # if the character is above the enemy
                    self.yPos += self.speed  # make the enemy go up

            # if the enemy is not within the x range of the character
            if not character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth:
                if character.xPos > self.xPos + self.width / 2:  # if the character is to the right of the enemy
                    self.xPos += self.speed  # make the enemy go right
                    # set directions
                    self.goingRight = True
                    self.goingLeft = False
                elif character.xPos < self.xPos + self.width / 2:  # if the character is to the left of the enemy
                    self.xPos -= self.speed  # make the enemy go left
                    # set directions
                    self.goingLeft = True
                    self.goingRight = False
            # Set the colliders for the enemy
            self.setRects()

            # ghosts dont get hit by fireballs
        else:
            if self.deadRunOnce:  # run once when character dies
                self.deathImage = self.movingAnimation[0]  # set the death image
                self.deadRunOnce = False  # make sure this only runs once
                self.enemyRect = pygame.Rect(0, 0, 0, 0)  # prevent further collisions after death

            # rotate image of enemy while it falls through the map
            self.image = pygame.transform.rotate(self.deathImage, self.deathCount * 8)
            self.yPos += 3  # make enemy fall through the map

            # add to death count
            self.deathCount += 1

            # if the character has been dead for 120 ticks, set it for deletion
            if self.deathCount >= 120:
                self.delete = True

    # Control the animation of the enemy
    def animationControl(self):
        if self.animationCount >= len(self.movingAnimation) - 1:  # reset animation if it surpasses animation length
            self.animationCount = 0
        else:
            self.animationCount += 0.1  # add 0.1 to animation to switch image every 10 ticks

        # get the current image from the animation
        self.image = self.movingAnimation[int(self.animationCount)]

    # Display the enemy
    def display(self):
        if not self.dead:  # control animation if the enemy is not dead
            self.animationControl()

        if self.image is not None:  # if the image exists
            # Display enemy based off of the direction the enemy is facing
            if self.goingLeft:
                self.mainSurface.blit(self.image, (
                    self.xPos, self.yPos + 3))  # Add 3 because the image normally is off the ground a littlea
            else:
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos, self.yPos + 3))
        else:  # draw a rectangle if there is not image
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)

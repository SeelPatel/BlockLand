import pygame

import Constants  # used to get animations and images


class BatEnemy:
    mainSurface = None

    # Used to check how far enemy has moved
    initX = 0
    initY = 0

    # Position of enemy on gameSurface
    xPos = 0
    yPos = 0
    # Movement range of enemy
    movementHeight = 0

    # Width and height of enemies, to create Rects for collision
    width = 75
    height = 40

    # Rects for oollision
    enemyRect = None
    topRect = None  # Used to determine if head is jumped on

    # Determine if enemy is moving up or down
    goingDown = True
    goingUp = False

    # Variables for animation and current image from animations
    mainAnimation = None
    image = None
    animationCount = 0

    # Variables for character death
    dead = False  # if character is dead
    deadRunOnce = True  # Used to run some code only once on character death
    deathCount = 0  # Count up to deleting enemy
    deathImage = None  # Image to display for death animation

    delete = False  # Enemy is deleted from list if this is true

    tag = "batEnemy"  # Enemy tag for character interactions

    # initialize enemy
    def __init__(self, surface: pygame.Surface, x: int, y: int, movementRange: int):
        # Set some of the attributes from the variables passed in
        # Purpose of these variables is listed above
        self.mainSurface = surface

        self.xPos = x
        self.yPos = y

        self.initX = x
        self.initY = y

        self.movementHeight = movementRange

        self.setRects()  # Set the Rects based on the starting X and Y

        # Get animation from constants file
        self.mainAnimation = Constants.Animations.BatEnemy.mainAnimation

    # set colliders
    def setRects(self):
        # Set rects based on position and size
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topRect = pygame.Rect(self.xPos - 6, self.yPos, self.width, 28)

    # control enemy
    def control(self, platforms, bullets: list, character):
        # Some imports are unused
        # This is because all enemies must have same control inputs
        # This is for simplicity in enemy control function

        if not self.dead:  # Do if character not dead
            # Move character
            if self.goingUp:
                self.yPos -= 4
            elif self.goingDown:
                self.yPos += 4

            # Set Rects based on new position
            self.setRects()

            # If the character moves out of movement range, flip the movement direction
            if self.yPos < self.initY - self.movementHeight:
                self.goingUp = False
                self.goingDown = True

            if self.yPos > self.initY + self.movementHeight:
                self.goingDown = False
                self.goingUp = True

            # If a bullet hits the enemy, kill it
            for bullet in bullets:
                if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):
                    self.dead = True
                    bullet.destroy = True
        else:  # Do if character is dead
            if self.deadRunOnce:  # Run once if enemy dies
                self.deathImage = self.mainAnimation[0]  # Set death image
                self.deadRunOnce = False  # dont run again
                self.enemyRect = pygame.Rect(0, 0, 0, 0)  # make sure no player collsion

            # Rotate enemy as it falls down through map after dieing
            self.image = pygame.transform.rotate(self.deathImage, self.deathCount * 8)
            self.yPos += 3

            self.deathCount += 1  # add to ticks

            # Set enemy ready for delete after 120 ticks
            if self.deathCount >= 120:
                self.delete = True

    # display enemy
    def display(self):
        # Animate character if the enemy is not dead
        if not self.dead:
            if self.animationCount >= len(self.mainAnimation):
                self.animationCount = 0

            self.image = self.mainAnimation[self.animationCount]
            self.animationCount += 1

        # Display the current image for the character
        self.mainSurface.blit(self.image, (self.xPos, self.yPos))

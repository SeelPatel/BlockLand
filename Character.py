import random

import pygame

import Constants
import FireBall
import GhostEnemy
import Pickups


class Character:
    # character health
    health = 3

    # Surface to display the character on
    mainSurface = None

    # Position of the character
    xPos = 0
    yPos = 0

    # If the character can jump from its current position
    canJump = False

    # Direction in which character is travelling
    goingUp = False
    goingDown = True
    goingRight = False
    goingLeft = False

    # The jump height of the character
    jumpHeight = 400

    # count to the length of time for which the character goes up
    jumpCount = 0

    # Acceleration for character movement
    jumpAcceleration = 0
    fallAcceleration = 0
    movingAcceleration = 0

    # Amount of ticks it takes for character to start running full speed
    movingAccelerationTime = 160  # 60 = 1 second

    # Main Rect for the
    charRect = None

    # character width and height
    characterWidth = 0
    characterHeight = 0

    # Rects for platform collison
    topCharRect = None
    bottomCharRect = None
    rightCharRect = None
    leftCharRect = None

    # Variables to determine if character is collding
    rightColliding = False
    leftColliding = False

    # image to display to gameSurface
    image = None

    # Max speed of character
    speed = 0

    # Speed when accelerating
    currentSpeed = 0

    # Animation Lists
    idleAnimation = []
    runningAnimation = []
    currentAnimation = []
    jumpingAnimation = []
    fallingAnimation = []

    # Animation count to determine position in animation lists
    animationCount = 0

    # Flip image if facing left
    facingLeft = False

    # Animation list to show dust when accelerating
    # It creates an effect as if his feet are slipping
    runningDustAnimation = []
    showRunningDust = False  # Show running dust if true
    runningDustCount = 0  # count for position in runningDust animation
    dustImage = None  # Image of dust to display

    debug = False  # Display colliders if true

    # Taking not damage if damage is already taken recently
    invinciblePeriodCount = 0  # Count for invincibility period
    takeNoDamage = False  # Take damage or not
    healthFlickerBool = True  # Used to flicker health if invincible
    healthFlickerTimer = 0  # Timer for health flicker
    invinciblePeriodLimit = 120  # How many ticks the invincibility period lasts for

    dead = False  # indicates if character is dead

    # Image for the health heart
    healthImage = None
    # Get image for the balls that the player shoots
    ballImage = pygame.transform.scale(Constants.Images.Bullet.fireBallImage, (50, 50))

    # Amount of balls the player has
    ballCount = 1

    # Indicates if level is passed
    moveToNextLevel = False

    # Used to set Rects for collision and interaction
    def setRects(self):
        # Set rect for enemy and bullet collision
        self.charRect = pygame.Rect(self.xPos, self.yPos, self.characterWidth, self.characterHeight)

        # Set rects for platform collisions
        self.topCharRect = pygame.Rect(self.xPos, self.yPos, self.characterWidth, 10)
        self.bottomCharRect = pygame.Rect(self.xPos, self.yPos + self.characterHeight - 10, self.characterWidth, 10)
        self.rightCharRect = pygame.Rect(self.xPos + self.characterWidth - 15, self.yPos, 15, self.characterHeight)
        self.leftCharRect = pygame.Rect(self.xPos, self.yPos, 15, self.characterHeight)

    # Used to set some variables and initialize some things
    def __init__(self, surface: pygame.Surface, startPos=(0, 0), image: pygame.image = None, width=30, height=50,
                 speed=13):
        # Set some of the attributes from the variables passed in
        # Purpose of these variables is listed above
        self.mainSurface = surface
        self.xPos = startPos[0]
        self.yPos = startPos[1]
        self.characterHeight = height
        self.characterWidth = width

        self.speed = speed

        self.setRects()  # set the rects based on starting position

        self.runningAnimation = Constants.Animations.Character.runningAnimation
        self.idleAnimation = Constants.Animations.Character.idleAnimation
        self.runningDustAnimation = Constants.Animations.Character.runningDustAnimation
        self.jumpingAnimation = Constants.Animations.Character.jumpingAnimation
        self.fallingAnimation = Constants.Animations.Character.fallingAnimation

        self.currentAnimation = self.idleAnimation  # set staring animation

        self.healthImage = Constants.Images.Heart.mainHeart

    # Control the animations of the character
    def animationControl(self):
        # Default animation
        self.currentAnimation = self.idleAnimation

        # This switches if any condition below is true

        # if going left or right, and not falling or jumping, set to moving animation
        if (self.goingRight or self.goingLeft) and not (self.goingDown or self.goingUp):
            self.currentAnimation = self.runningAnimation

        # If the character is going up, then play a jumping animation
        if self.goingUp:
            self.currentAnimation = self.jumpingAnimation
        # If the character is going down, then play a falling animation
        elif self.goingDown and not self.goingUp:
            self.currentAnimation = self.fallingAnimation
        # if the character is going left and right at once
        # this means the player is pressing A and D at the same time
        elif self.goingRight and self.goingLeft:
            self.currentAnimation = self.idleAnimation

        # Change direction character is facing
        # Used to flip image based on direction
        if self.goingLeft:
            self.facingLeft = True
        if self.goingRight:
            self.facingLeft = False

        # add to animation count
        self.animationCount += 1
        # if the point in animation is greater than the size of the animation list
        if self.animationCount >= len(self.currentAnimation):
            self.animationCount = 0
        else:
            # Set the image and flip it based on the direction the character is facing
            if self.goingLeft or self.facingLeft:
                self.image = pygame.transform.flip(self.currentAnimation[self.animationCount], True, False)
            else:
                self.image = self.currentAnimation[self.animationCount]

        # Check if the player is on ground, moving in one direction, and accelerating to decide
        if self.showRunningDust and (self.goingRight or self.goingLeft) and not self.goingDown and not (
                    self.goingLeft and self.goingRight):
            if self.runningDustCount >= len(self.runningDustAnimation):  # Reset animation if done
                self.runningDustCount = 0
            self.dustImage = self.runningDustAnimation[self.runningDustCount]  # Set the dust image to be displayed
            self.runningDustCount += 1  # Progress the animation
        else:
            self.runningDustCount = 0  # Make sure animation starts at beginning
            self.dustImage = None  # Make sure no image will be displayed

    # Function to display health of the player to the screen
    def displayHealth(self, surface: pygame.Surface):
        if not self.takeNoDamage:  # If the user is not invincible
            # Spread health hearts out based on amount of health
            for h in range(self.health):  # makes it able to draw any amount of health
                surface.blit(self.healthImage, (5 * h + self.healthImage.get_width() * h, 0))  # Draw health

        else:  # if the user is invincible (after taking damage)
            if self.healthFlickerTimer >= 15:  # flicker health every 15 seconds
                self.healthFlickerBool = not self.healthFlickerBool
                self.healthFlickerTimer = 0

            # Display the health if the health is supposed to appear
            if self.healthFlickerBool:
                for h in range(self.health):
                    surface.blit(self.healthImage, (5 * h + self.healthImage.get_width() * h, 0))
            self.healthFlickerTimer += 1

    # Function to display the amount of balls
    def displayBalls(self, surface: pygame.Surface):  # display amount of balls the player has
        for h in range(self.ballCount):  # Allows program to display as many balls as user has
            surface.blit(self.ballImage,  # display balls at top left
                         (5 * h + self.ballImage.get_width() * h, self.healthImage.get_height() + 10))

    # Function to display the character on the screen
    def display(self):
        self.animationControl()  # Control the animation

        # Blit the character image on the screen
        self.mainSurface.blit(self.image, (self.xPos, self.yPos))

        # Display the dust if accelerating and the dustImage varible has an image
        if self.showRunningDust and self.dustImage is not None:
            if not self.facingLeft:  # Display the dust to the right if going left
                self.mainSurface.blit(self.dustImage, (
                    self.xPos - self.dustImage.get_width(),
                    self.yPos + self.characterHeight - self.dustImage.get_height()))
            else:  # otherwise display the dust on the left
                self.mainSurface.blit(pygame.transform.flip(self.dustImage, True, False), (
                    self.xPos + self.characterWidth, self.yPos + self.characterHeight - self.dustImage.get_height()))

        # if debug variable is true, display the colliders for the character
        if self.debug:
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.topCharRect, 1)
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.bottomCharRect, 1)
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.leftCharRect, 1)
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.rightCharRect, 1)
            if self.takeNoDamage:  # Display square to indicate invincibility period
                pygame.draw.rect(self.mainSurface, (0, 0, 255), [self.xPos, self.yPos, 20, 20], 0)

    # Control the character based on user inputs
    def playerControl(self, events: list, bullets: list):
        # Take in game events and bullets to control game actions
        for e in events:
            if e.type == pygame.KEYDOWN:  # If the player presses keys
                if e.key == pygame.K_SPACE:  # jump
                    if self.canJump:  # if the player can jump
                        self.goingUp = True  # make player go up
                        self.goingDown = False  # make player stop going done
                        self.jumpCount = 0  # start count for jump to stop at certain height
                        self.canJump = False  # Set player inable to jump again until landing

                elif e.key == pygame.K_d:  # go right
                    self.goingRight = True  # set the character going right

                elif e.key == pygame.K_a:  # go left
                    self.goingLeft = True  # set character going left

                elif e.key == pygame.K_m:  # shoot bullets
                    if self.ballCount > 0:  # If the player has bullets left
                        self.ballCount -= 1  # remove a bullet
                        # Shoot bullet left if facing left and right if facing right
                        if self.facingLeft:
                            bullets.append(FireBall.FireBall(self.mainSurface, self.xPos, self.yPos, startRight=False))
                        else:
                            bullets.append(FireBall.FireBall(self.mainSurface, self.xPos, self.yPos))

            if e.type == pygame.KEYUP:  # if the players lets a button up
                if e.key == pygame.K_d:  # right
                    self.goingRight = False  # Stop the character from going right
                if e.key == pygame.K_a:  # left
                    self.goingLeft = False  # Stop the character from going left

    # function to move character
    def moveCharacter(self, platforms: list, enemies: list, pickups: list, bullets: list):
        # Take in game elements to control player based off of them

        # jumping code
        if self.goingUp:  # if the character is set as going up
            # Slow player down with acceleration while changing the height of the character
            self.yPos -= self.speed - self.speed * self.jumpAcceleration
            self.jumpCount += 1  # add to this control when player falls back down
            self.jumpAcceleration += 0.02  # Add to acceleration to slow the player more as he ascends
            # if the player should fall back down, stop him from jumping
            if self.jumpCount >= self.jumpHeight // self.speed:
                self.goingUp = False
                self.goingDown = True
            if self.collidingTop(platforms):  # if the player hits something above while jumping, drop back down
                self.goingUp = False
                self.goingDown = True

                collidingPlatform = self.getCollidingTopRect(platforms)  # get the platform the character hit on top
                # Check if the character hit a powerup plaform
                if collidingPlatform.tag == "health" and not collidingPlatform.droppedAlready:
                    # calculate middle of crate
                    x = collidingPlatform.xPos + ((collidingPlatform.width - Pickups.HealthPickup.width) / 2)
                    y = collidingPlatform.yPos - Pickups.HealthPickup.height - 50
                    # add a health pickup
                    pickups.append(Pickups.HealthPickup(self.mainSurface, x, y))
                    collidingPlatform.droppedAlready = True  # dont let object drop more than once
                if collidingPlatform.tag == "fireball" and not collidingPlatform.droppedAlready:
                    # calculate middle of crate
                    x = collidingPlatform.xPos + ((collidingPlatform.width - Pickups.FireBallPickup.width) / 2)
                    y = collidingPlatform.yPos - Pickups.FireBallPickup.height - 50
                    # add a ball refill powerup
                    pickups.append(Pickups.FireBallPickup(self.mainSurface, x, y))
                    collidingPlatform.droppedAlready = True  # Dont let object drop more than once
        else:
            self.jumpAcceleration = 0  # if the character is not jumping, reset acceleration

        # If the character is falling
        if self.goingDown and not self.goingUp:
            # Speed player up with acceleration while changing the height of the character
            self.yPos += self.speed + self.speed * self.fallAcceleration
            # Add to character falling acceleration
            self.fallAcceleration += 0.02
            # if the character hits ground, stop it from falling
            if self.collidingBottom(platforms):
                self.goingDown = False  # stop from falling
                collidingObject = self.getCollidingBottomRect(platforms)  # get platform
                self.yPos = collidingObject.yPos - self.characterHeight + 1  # set character atop the platform

                if collidingObject.tag == "deathPlatform":  # Kill player if he falls off map
                    self.dead = True
        else:
            self.fallAcceleration = 0  # if the character is not falling, reset acceleration

        if self.goingUp:  # set going down false if player is jumping
            self.goingDown = False

        # going right code
        if self.goingRight:
            if self.collidingRight(platforms):  # if the character is colliding to the right
                platform = self.getCollidingRightRect(platforms)  # get platform
                if platform.tag == "endGame":  # if player hits end game block, then let player win
                    self.moveToNextLevel = True
                self.xPos = platform.xPos - self.characterWidth + 1  # set player pos to left of plaform
            else:
                if not self.goingDown:  # If the character is not going down, add to acceleration
                    # add speed based on time to accelerate
                    self.movingAcceleration += self.speed / self.movingAccelerationTime
                # set speed limited by preset speed
                self.currentSpeed = min(self.speed / 2 + self.movingAcceleration, self.speed)
                # add current speed to character position to move character
                if not (self.goingRight and self.goingLeft):
                    self.xPos += self.currentSpeed
            # determine if character is accelerating and show dust if it is
            if self.movingAcceleration < self.speed / 2:
                self.showRunningDust = True
            else:
                self.showRunningDust = False

        if self.goingLeft:
            if self.collidingLeft(platforms):  # if the character is colliding to the left
                platform = self.getCollidingLeftRect(platforms)  # get platform
                self.xPos = platform.xPos + platform.width - 1  # set player pos to right of plaform
            else:  # if not colliding
                if not self.goingDown:  # accelerate if not falling
                    self.movingAcceleration += self.speed / self.movingAccelerationTime
                # add to speed limited by pre determined speed
                self.currentSpeed = min(self.speed / 2 + self.movingAcceleration, self.speed)
                if not (self.goingRight and self.goingLeft):
                    # add current speed to character position to move character
                    self.xPos -= self.currentSpeed
            # determine if character is accelerating and show dust if it is
            if self.movingAcceleration < self.speed / 2:
                self.showRunningDust = True
            else:
                self.showRunningDust = False

        # reset speed and acceleration if player not moving or going both directions
        if not self.goingLeft and not self.goingRight:
            self.movingAcceleration = 0
            self.currentSpeed = 0
        if self.goingRight and self.goingLeft:
            self.movingAcceleration = 0
            self.currentSpeed = 0

        # set player able to jump if character is on platform
        if self.collidingBottom(platforms):
            self.canJump = True
        else:  # otherwise dont let player jump and drop player
            self.goingDown = True
            self.canJump = False

        # Health control
        if self.takeNoDamage:  # if invincible add to count
            self.invinciblePeriodCount += 1

        # if count reaches the limit, remove invincibility
        if self.invinciblePeriodCount > self.invinciblePeriodLimit:
            self.takeNoDamage = False

        # if player has no health, player is dead
        if self.health <= 0:
            self.dead = True

        # ENEMY COLLISION
        self.interactWithEnemies(enemies)  # Control enemy interactions
        self.interactWithBulletsAndPickups(bullets, pickups)  # control bullet and pickups interactions

        self.setRects()  # set the colliders of the character

    # control interactions with bullets and pickups
    def interactWithBulletsAndPickups(self, bullets: list, pickups: list):
        # Use the inputted bullet list
        for bullet in bullets:
            # if the bullet should hurt player and it isnt already destroyed
            if bullet.hurtPlayer and not bullet.destroy:
                if bullet.tag == "bullet":  # if the bullet type is bullet
                    if self.charRect.collidepoint(bullet.xPos, bullet.yPos):  # check collisoin
                        # take damage and destroy bullet
                        self.takeDamage(1)
                        bullet.destroy = True
                if bullet.tag == "fireBall":  # if the bullet type is fireball
                    if self.charRect.colliderect(bullet.mainRect):  # check collision
                        # take damage and destroy bullet
                        self.takeDamage(1)
                        bullet.destroy = True

        # Control Pickups
        # Use inputted pickups lists
        for pickup in pickups:
            if self.charRect.colliderect(pickup.mainRect):
                # if pickup is picked up, set it as picked up, which sets them for deletion
                if pickup.tag == "health":
                    pickup.picked = True
                    self.health += 1  # reset health
                if pickup.tag == "fireball":
                    pickup.picked = True
                    self.ballCount = 3  # fill balls

    # control enemy interactions
    def interactWithEnemies(self, enemies: list):
        for enemy in enemies:
            if not enemy.dead:  # if enemy is not dead
                if enemy.tag == "batEnemy":
                    # if player is going down and hitting the top of the enemy
                    if self.bottomCharRect.colliderect(enemy.topRect) and self.goingDown and not self.goingUp:
                        # kill enemy
                        enemy.dead = True
                        # Make enemy jump
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                        # Make character invincible for 20 ticks
                        self.takeDamage(0, 20)
                    elif self.topCharRect.colliderect(enemy.enemyRect):
                        # make player fall if character hits bottom of enemy while jumping
                        self.goingUp = False
                        self.goingDown = True
                        self.takeDamage(1)  # take damage
                    elif self.charRect.colliderect(enemy.enemyRect):
                        self.takeDamage(1)  # if the player runs into enemy take damage

                elif enemy.tag == "slimeEnemy":
                    # if player is going down and hitting the top of the enemy
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        # kill enemy
                        enemy.dead = True
                        # Make enemy jump
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                        # Make character invincible for 20 ticks
                        self.takeDamage(0, 20)
                    elif self.charRect.colliderect(enemy.enemyRect):
                        self.takeDamage(1)  # if the player runs into enemy take damage

                elif enemy.tag == "zombieEnemy":
                    # if player is going down and hitting the top of the enemy
                    if self.bottomCharRect.colliderect(
                            enemy.topEnemyRect) and self.goingDown and not self.goingUp and not enemy.jumping:
                        # hurt enemy
                        enemy.health -= 1
                        # Make enemy jump
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                        # Make character invincible for 20 ticks
                        self.takeDamage(0, 20)
                    elif enemy.jumping and enemy.enemyRect.colliderect(self.charRect):
                        self.takeDamage(1)  # if character jumps up and hits player take damage
                    elif enemy.enemyRect.colliderect(self.charRect):
                        self.takeDamage(1)  # if the player runs into enemy take damage

                elif enemy.tag == "ghostEnemy":
                    # if player is going down and hitting the top of the enemy
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        # kill enemy
                        enemy.dead = True
                        # Make enemy jump
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                        # Make character invincible for 40 ticks
                        self.takeDamage(0, 40)
                    elif enemy.enemyRect.colliderect(self.charRect):
                        self.takeDamage(1)  # if the player runs into enemy take damage

                elif enemy.tag == "shooterEnemy":
                    # if player is going down and hitting the top of the enemy
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        # kill enemy
                        enemy.dead = True
                        # Make enemy jump
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                        # Make character invincible for 20 ticks
                        self.takeDamage(0, 20)
                    elif enemy.enemyRect.colliderect(self.charRect):
                        self.takeDamage(1)  # Take damage if character runs into enemy

                elif enemy.tag == "zombieBoss":
                    # if player is going down and hitting the top of the enemy
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        # kill enemy
                        enemy.health -= 1
                        # Make enemy jump
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                        # Make character invincible for 40 ticks
                        self.takeDamage(0, 40)
                        if random.randint(0, 1) == 0:  # spawn ghost at right if 0 is generated
                            self.spawnGhost(self.mainSurface, enemies, self.xPos + 500,
                                            enemy.yPos + 50)
                        else:  # spawn ghost at left if 0 is not generated
                            self.spawnGhost(self.mainSurface, enemies, self.xPos - 500,
                                            enemy.yPos + 50)
                    elif self.charRect.colliderect(enemy.enemyRect):
                        self.takeDamage(1)  # if the player runs into enemy take damage

    # spawn ghost at position provided
    def spawnGhost(self, surface, enemies: list, x, y):
        enemies.append(GhostEnemy.GhostEnemy(surface, x, y, speed=6))

    # function to take damage
    def takeDamage(self, amount: int, periodStart: int = 0):
        if not self.takeNoDamage:  # if not invincible
            # Make character invincible
            self.invinciblePeriodCount = periodStart
            self.takeNoDamage = True
            # remove health
            self.health -= amount
            return True  # return true if character could take damage
        return False  # false if character cant take damage and is invincible

    # check if collding right
    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:  # if the character is in range
                if platform.checkLeftCollide(self.rightCharRect):  # check collision
                    self.rightColliding = True
                    return True  # return true if colllding
        self.rightColliding = False
        return False  # return false if not colliding

    # check if colliding left
    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:  # if the character in in range
                if platform.checkRightCollide(self.leftCharRect):  # check collison
                    self.leftColliding = True  # return true if collidng
                    return True
        self.leftColliding = False
        return False  # return false otherwise

    # check if collding top
    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if character is in range
                if platform.checkBottomCollide(self.topCharRect):  # check collision
                    return True  # return true if colliding
        return False  # other wise false

    # check if colliding bottom
    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if character is in range
                if platform.checkTopCollide(self.bottomCharRect):  # check collision
                    return True  # return true if colliding
        return False

    # get colliding platform
    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if character is in range
                if platform.checkTopCollide(self.bottomCharRect):  # check collision
                    return platform  # return colliding platform
        return None

    # get colliding platform
    def getCollidingTopRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if character is in range
                if platform.checkBottomCollide(self.topCharRect):  # check collision
                    return platform  # return colliding platform
        return None

    # get colliding platform
    def getCollidingRightRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if character is in range
                if platform.checkLeftCollide(self.rightCharRect):  # check collision
                    return platform  # return colliding platform
        return None

    # get colliding platform
    def getCollidingLeftRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:  # if character is in range
                if platform.checkRightCollide(self.leftCharRect):  # check collision
                    return platform  # return colliding platform
        return None

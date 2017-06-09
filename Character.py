import pygame
import os
import tools
import FireBall
import Pickups

import Constants

class Character:
    health = 3

    mainSurface = None
    xPos = 0
    yPos = 0

    canJump = False

    goingUp = False
    goingDown = True

    goingRight = False
    goingLeft = False

    jumpHeight = 400
    jumpCount = 0

    jumpAcceleration = 0
    fallAcceleration = 0
    movingAcceleration = 0

    movingAccelerationTime = 160  # 60 = 1 second

    charRect = None

    characterWidth = 30
    characterHeight = 50

    topCharRect = None
    bottomCharRect = None
    rightCharRect = None
    leftCharRect = None

    rightColliding = False
    leftColliding = False

    originalImage = None

    image = None

    speed = 0
    currentSpeed = 0

    idleAnimation = []
    runningAnimation = []
    currentAnimation = []
    jumpingAnimation = []
    fallingAnimation = []
    animationCount = 0
    facingLeft = False

    runningDustAnimation = []
    showRunningDust = False
    runningDustCount = 0
    dustImage = None

    debug = False

    invinciblePeriodCount = 0
    takeNoDamage = False
    healthFlickerBool = True
    healthFlickerTimer = 0
    invinciblePeriodLimit = 120
    dead = False

    healthImage = None
    ballImage = pygame.transform.scale(Constants.Images.Bullet.fireBallImage,(50,50))

    ballCount = 1

    moveToNextLevel = False

    def setRects(self):
        self.charRect = pygame.Rect(self.xPos, self.yPos, self.characterWidth, self.characterHeight)
        self.topCharRect = pygame.Rect(self.xPos, self.yPos, self.characterWidth, 10)
        self.bottomCharRect = pygame.Rect(self.xPos, self.yPos + self.characterHeight - 10, self.characterWidth, 10)

        self.rightCharRect = pygame.Rect(self.xPos + self.characterWidth - 15, self.yPos, 15, self.characterHeight)
        self.leftCharRect = pygame.Rect(self.xPos, self.yPos, 15, self.characterHeight)

    def __init__(self, surface: pygame.Surface, startPos=(0, 0), image: pygame.image = None, width=30, height=50,
                 speed=13):
        self.mainSurface = surface
        self.xPos = startPos[0]
        self.yPos = startPos[1]
        self.characterHeight = height
        self.characterWidth = width

        self.speed = speed

        self.originalImage = image
        self.changeImageSize()

        self.setRects()

        self.runningAnimation = Constants.Animations.Character.runningAnimation
        self.idleAnimation = Constants.Animations.Character.idleAnimation
        self.runningDustAnimation = Constants.Animations.Character.runningDustAnimation
        self.jumpingAnimation = Constants.Animations.Character.jumpingAnimation
        self.fallingAnimation = Constants.Animations.Character.fallingAnimation

        self.currentAnimation = self.idleAnimation

        self.healthImage = Constants.Images.Heart.mainHeart

    def changeImageSize(self):
        if self.originalImage != None:
            self.image = pygame.transform.smoothscale(self.originalImage, (self.characterWidth, self.characterHeight))
        else:
            self.image = None

    def animationControl(self):
        if (self.goingRight or self.goingLeft) and not (self.goingDown or self.goingUp):
            self.currentAnimation = self.runningAnimation
            if self.goingLeft:
                self.facingLeft = True
            if self.goingRight:
                self.facingLeft = False
        else:
            self.currentAnimation = self.idleAnimation

        if self.goingUp:
            self.currentAnimation = self.jumpingAnimation
            if self.goingLeft:
                self.facingLeft = True
            if self.goingRight:
                self.facingLeft = False

        elif self.goingDown and not self.goingUp:
            self.currentAnimation = self.fallingAnimation
            if self.goingLeft:
                self.facingLeft = True
            if self.goingRight:
                self.facingLeft = False

        elif not self.goingLeft and not self.goingRight:
            self.currentAnimation = self.idleAnimation

        elif self.goingRight and self.goingLeft:
            self.currentAnimation = self.idleAnimation

        self.animationCount += 1
        if self.animationCount >= len(self.currentAnimation):
            self.animationCount = 0
        else:
            if self.goingLeft or self.facingLeft:
                self.image = pygame.transform.flip(self.currentAnimation[self.animationCount], True, False)
            else:
                self.image = self.currentAnimation[self.animationCount]

        if self.showRunningDust and (self.goingRight or self.goingLeft) and not self.goingDown and not (
                    self.goingLeft and self.goingRight):
            if self.runningDustCount >= len(self.runningDustAnimation):
                self.runningDustCount = 0
            self.dustImage = self.runningDustAnimation[self.runningDustCount]
            self.runningDustCount += 1
        else:
            self.runningDustCount = 0
            self.dustImage = None

    def displayHealth(self,surface : pygame.Surface):
        if not self.takeNoDamage:
            for h in range(self.health):
                surface.blit(self.healthImage,(5 * h + self.healthImage.get_width() * h, 0))
        else:
            if self.healthFlickerTimer >= 15:
                self.healthFlickerBool = not self.healthFlickerBool
                self.healthFlickerTimer = 0

            if self.healthFlickerBool:
                for h in range(self.health):
                    surface.blit(self.healthImage, (5 * h + self.healthImage.get_width() * h, 0))
            self.healthFlickerTimer += 1

    def displayBalls(self, surface : pygame.Surface):
        for h in range(self.ballCount):
            surface.blit(self.ballImage,
                         (5 * h + self.ballImage.get_width() * h, self.healthImage.get_height()+10))


    def display(self):
        self.animationControl()

        self.mainSurface.blit(self.image, (self.xPos, self.yPos))

        if self.showRunningDust and self.dustImage != None:
            if not self.facingLeft:
                self.mainSurface.blit(self.dustImage, (
                    self.xPos - self.dustImage.get_width(),
                    self.yPos + self.characterHeight - self.dustImage.get_height()))
            else:
                self.mainSurface.blit(pygame.transform.flip(self.dustImage, True, False), (
                    self.xPos + self.characterWidth, self.yPos + self.characterHeight - self.dustImage.get_height()))

        if self.debug:
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.topCharRect, 1)
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.bottomCharRect, 1)
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.leftCharRect, 1)
            pygame.draw.rect(self.mainSurface, (0, 255, 0), self.rightCharRect, 1)
            if self.takeNoDamage:
                pygame.draw.rect(self.mainSurface, (0, 0, 255), [self.xPos, self.yPos, 20, 20], 0)

    def playerControl(self, events: list,bullets : list):
        self.setRects()
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.canJump:
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False

                if e.key == pygame.K_d:
                    self.goingRight = True

                if e.key == pygame.K_a:
                    self.goingLeft = True

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_d:
                    self.goingRight = False
                if e.key == pygame.K_a:
                    self.goingLeft = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    if self.ballCount > 0:
                        self.ballCount -= 1
                        if self.facingLeft:
                            bullets.append(FireBall.FireBall(self.mainSurface, self.xPos, self.yPos, startRight=False))
                        else:
                            bullets.append(FireBall.FireBall(self.mainSurface, self.xPos, self.yPos))

    def moveCharacter(self, platforms: list, enemies: list, pickups : list,bullets : list):
        # jumping code
        if self.goingUp:
            self.yPos -= self.speed - self.speed * self.jumpAcceleration
            self.jumpCount += 1
            self.jumpAcceleration += 0.02
            if self.jumpCount >= self.jumpHeight // self.speed:
                self.goingUp = False
                self.goingDown = True
            if self.collidingTop(platforms):
                self.goingUp = False
                self.goingDown = True

                collidingPlatform = self.getCollidingTopRect(platforms)
                if collidingPlatform.tag == "health" and not collidingPlatform.droppedAlready:
                    x = collidingPlatform.xPos + ((collidingPlatform.width - Pickups.HealthPickup.width)/2)
                    y = collidingPlatform.yPos - Pickups.HealthPickup.height - 50
                    pickups.append(Pickups.HealthPickup(self.mainSurface,x,y))
                    collidingPlatform.droppedAlready = True
                if collidingPlatform.tag == "fireball" and not collidingPlatform.droppedAlready:
                    x = collidingPlatform.xPos + ((collidingPlatform.width - Pickups.FireBallPickup.width)/2)
                    y = collidingPlatform.yPos - Pickups.FireBallPickup.height - 50
                    pickups.append(Pickups.FireBallPickup(self.mainSurface,x,y))
                    collidingPlatform.droppedAlready = True
        else:
            self.jumpAcceleration = 0

        if self.goingDown and not self.goingUp:
            self.yPos += self.speed + self.speed * self.fallAcceleration
            self.fallAcceleration += 0.02
            if self.collidingBottom(platforms):
                self.goingDown = False
                # self.yPos -= self.speed * 2 - int(self.speed / 2)
                colldingObject = self.getCollidingBottomRect(platforms)
                self.yPos = colldingObject.yPos - self.characterHeight + 1

                if colldingObject.tag == "deathPlatform": #Kill player if he falls off map
                    self.dead = True
        else:
            self.fallAcceleration = 0

        if self.goingUp:
            self.goingDown = False

        # going right code
        if self.goingRight:
            if self.collidingRight(platforms):
                platform = self.getCollidingRightRect(platforms)
                if platform.tag == "endGame":
                    self.moveToNextLevel = True

                self.xPos = platform.xPos - self.characterWidth+1
            else:
                if not self.goingDown:
                    self.movingAcceleration += self.speed / self.movingAccelerationTime
                self.currentSpeed = min(self.speed / 2 + self.movingAcceleration, self.speed)
                if not(self.goingRight and self.goingLeft):
                    self.xPos += self.currentSpeed

            if self.movingAcceleration < self.speed / 2:
                self.showRunningDust = True
            else:
                self.showRunningDust = False

        if self.goingLeft:
            if self.collidingLeft(platforms):
                platform = self.getCollidingLeftRect(platforms)
                self.xPos = platform.xPos + platform.width-1
            else:
                if not self.goingDown:
                    self.movingAcceleration += self.speed / self.movingAccelerationTime
                self.currentSpeed = min(self.speed / 2 + self.movingAcceleration, self.speed)
                if not (self.goingRight and self.goingLeft):
                    self.xPos -= self.currentSpeed

            if self.movingAcceleration < self.speed / 2:
                self.showRunningDust = True
            else:
                self.showRunningDust = False

        if not self.goingLeft and not self.goingRight:
            self.movingAcceleration = 0
            self.currentSpeed = 0

        if self.goingRight and self.goingLeft:
            self.movingAcceleration = 0
            self.currentSpeed = 0

        if self.collidingBottom(platforms):
            self.canJump = True
        else:
            self.goingDown = True
            self.canJump = False
        # HEalth control
        if self.takeNoDamage:
            self.invinciblePeriodCount += 1

        if self.invinciblePeriodCount > self.invinciblePeriodLimit:
            self.takeNoDamage = False

        if self.health <= 0:
            self.dead = True

        # ENEMY COLLISION

        for enemy in enemies:
            if not enemy.dead:
                if enemy.tag == "batEnemy":
                    if self.bottomCharRect.colliderect(enemy.topRect) and self.goingDown and not self.goingUp:
                        enemy.dead = True
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                    elif self.topCharRect.colliderect(enemy.enemyRect):
                        self.goingUp = False
                        self.goingDown = True
                        self.takeDamage(1)
                    elif self.charRect.colliderect(enemy.enemyRect):
                        self.takeDamage(1)

                elif enemy.tag == "slimeEnemy":
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        enemy.dead = True
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                    elif self.charRect.colliderect(enemy.enemyRect):
                        self.takeDamage(1)
                elif enemy.tag == "zombieEnemy":
                    if self.bottomCharRect.colliderect(
                            enemy.topEnemyRect) and self.goingDown and not self.goingUp and not enemy.jumping:
                        enemy.health -= 1
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                    elif enemy.jumping and enemy.enemyRect.colliderect(self.charRect):
                        if self.takeDamage(1):
                            self.xPos -= 100
                elif enemy.tag == "ghostEnemy":
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        enemy.dead = True
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                    elif enemy.enemyRect.colliderect(self.charRect):
                        if self.takeDamage(1):
                            self.xPos -= 100
                elif enemy.tag == "shooterEnemy":
                    if self.bottomCharRect.colliderect(enemy.topEnemyRect) and self.goingDown and not self.goingUp:
                        enemy.dead = True
                        self.goingUp = True
                        self.goingDown = False
                        self.jumpCount = 0
                        self.canJump = False
                    elif enemy.enemyRect.colliderect(self.charRect):
                        if self.takeDamage(1):
                            self.xPos -= 100

        for bullet in bullets:
            if bullet.hurtPlayer and not bullet.destroy:
                if bullet.tag == "bullet":
                    if self.charRect.collidepoint(bullet.xPos,bullet.yPos):
                        self.takeDamage(1)
                        bullet.destroy = True
                if bullet.tag == "fireBall":
                    if self.charRect.colliderect(bullet.mainRect):
                        self.takeDamage(1)
                        bullet.destroy = True


        #Control Pickups
        for pickup in pickups:
            if self.charRect.colliderect(pickup.mainRect):
                if pickup.tag == "health":
                    pickup.picked = True
                    self.health +=1
                if pickup.tag == "fireball":
                    pickup.picked = True
                    self.ballCount = 3

    def takeDamage(self, amount: int):
        if not self.takeNoDamage:
            self.invinciblePeriodCount = 0
            self.takeNoDamage = True
            self.health -= amount
            return True
        return False

    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:
                if platform.checkLeftCollide(self.rightCharRect):
                    self.rightColliding = True
                    return True
        self.rightColliding = False
        return False

    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:
                if platform.checkRightCollide(self.leftCharRect):
                    self.leftColliding = True
                    return True
        self.leftColliding = False
        return False

    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkBottomCollide(self.topCharRect):
                    return True
        return False

    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomCharRect):
                    return True
        return False

    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomCharRect):
                    return platform
        return None

    def getCollidingTopRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkBottomCollide(self.topCharRect):
                    return platform
        return None

    def getCollidingRightRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkLeftCollide(self.rightCharRect):
                    return platform
        return None

    def getCollidingLeftRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkRightCollide(self.leftCharRect):
                    return platform
        return None

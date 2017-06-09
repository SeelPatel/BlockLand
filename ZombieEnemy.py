import pygame
import tools
import Constants


class ZombieEnemy:
    mainSurface = None

    xPos = 0
    yPos = 0
    speed = 0

    width = 50
    height = 80

    dead = False
    deadRunOnce = True
    deathCount = 0
    delete = False

    goingLeft = True
    goingRight = False
    goingDown = False

    jumping = False
    jumpHeight = 0
    maxJumpHeight = 200

    jumpTimer = 0
    jumpTimerMax = 150

    jumpingToReachPlayer = False
    reachPlayerJumpTimer = 0

    leftColliding = False
    rightColliding = False

    enemyRect = None
    rightEnemyRect = None
    leftEnemyRect = None
    topEnemyRect = None
    bottomEnemyRect = None

    tag = "zombieEnemy"

    jumpingAnimation = []
    movingAnimation = []
    animationCount = 0
    image = None

    currentAnimation = []

    health = 3

    facingLeft = True
    facingRight = False

    def __init__(self, surface: pygame.Surface, x, y, speed=6, health=3):
        self.mainSurface = surface
        self.xPos = x
        self.yPos = y
        self.speed = speed
        self.setRects()
        self.health = health

        self.movingAnimation = Constants.Animations.ZombieEnemy.movingAnimation
        self.jumpingAnimation = Constants.Animations.ZombieEnemy.jumpingAnimation

        self.currentAnimation = self.movingAnimation

    def setRects(self):
        self.enemyRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.topEnemyRect = pygame.Rect(self.xPos, self.yPos, self.width, 10)
        self.leftEnemyRect = pygame.Rect(self.xPos, self.yPos, 10, self.height)
        self.rightEnemyRect = pygame.Rect(self.xPos + self.width - 10, self.yPos, 10, self.height)
        self.bottomEnemyRect = pygame.Rect(self.xPos, self.yPos + self.height - 10, self.width, 10)

    def control(self, platforms, bullets, character):
        if not self.dead:

            if self.health <= 0:
                self.dead = True

            if character.xPos >= self.xPos:
                self.facingRight = True
                self.facingLeft = False
            elif character.xPos <= self.xPos:
                self.facingLeft = True
                self.facingRight = False

            if self.collidingBottom(platforms) and not self.jumping:
                self.yPos = self.getCollidingBottomRect(platforms).yPos - self.height + 1
                self.goingDown = False
                if self.getCollidingBottomRect(platforms).tag == "deathPlatform":
                    self.dead = True
                if not (character.xPos <= self.xPos + self.width / 2 <= character.xPos + character.characterWidth):
                    if character.xPos > self.xPos:
                        self.goingRight = True
                        self.goingLeft = False
                    elif character.xPos < self.xPos:
                        self.goingLeft = True
                        self.goingRight = False

                    self.reachPlayerJumpTimer = 0
                else:
                    self.goingLeft = False
                    self.goingRight = False
                    self.reachPlayerJumpTimer += 1
                    if character.yPos < self.yPos - 50 and self.reachPlayerJumpTimer >= 20:
                        self.jumping = True
                        self.jumpHeight = 0
                        self.jumpingToReachPlayer = True

            else:
                if not self.jumping:
                    self.goingDown = True
                self.goingLeft = False
                self.goingRight = False

            if self.goingRight:
                if self.collidingRight(platforms):
                    if self.jumpTimer >= self.jumpTimerMax:
                        self.jumping = True
                        self.jumpHeight = 0
                        self.jumpTimer = 0
                else:
                    self.xPos += self.speed

            if self.goingLeft:
                if self.collidingLeft(platforms):
                    if self.jumpTimer >= self.jumpTimerMax:
                        self.jumping = True
                        self.jumpHeight = 0
                        self.jumpTimer = 0
                else:
                    self.xPos -= self.speed

            if self.goingDown and not self.jumping:
                self.yPos += self.speed * 1.5

            if self.jumping:
                self.currentAnimation = self.jumpingAnimation

                self.yPos -= self.speed * 1.5
                self.goingDown = False
                self.jumpHeight += self.speed * 2
                if not self.jumpingToReachPlayer:
                    if (not self.collidingRight(platforms) and (not self.collidingLeft(platforms)) or (
                                self.jumpHeight >= self.maxJumpHeight)):
                        self.jumping = False

                if (self.jumpingToReachPlayer and self.jumpHeight >= self.maxJumpHeight) or (self.collidingTop(platforms)):
                    self.reachPlayerJumpTimer = 0
                    self.jumping = False
                    self.jumpingToReachPlayer = False

            else:
                self.currentAnimation = self.movingAnimation

            self.setRects()
        else:
            if self.deadRunOnce:
                self.image = pygame.transform.scale(self.movingAnimation[0], (self.movingAnimation[0].get_width(), 15))
                self.yPos = self.yPos + self.height
                self.deadRunOnce = False
                self.enemyRect = pygame.Rect(0,0,0,0)
            self.deathCount += 1
            if self.deathCount >= 60:
                self.delete = True

        for bullet in bullets:
            if self.enemyRect.collidepoint(bullet.xPos, bullet.yPos):
                self.health -= 1
                bullet.destroy = True

        self.jumpTimer += 1

    def animationControl(self):
        if self.animationCount >= len(self.currentAnimation) - 1:
            self.animationCount = 0
        else:
            self.animationCount += 0.3

        self.image = self.currentAnimation[int(self.animationCount)]

    def display(self):
        if not self.dead:
            self.animationControl()

        if self.image is not None:
            if self.facingLeft:
                self.mainSurface.blit(pygame.transform.flip(self.image, True, False), (self.xPos-5, self.yPos -18))
            else:
                self.mainSurface.blit(self.image, (
                    self.xPos-5, self.yPos -18))  # -5 and -18 to align the image properly
        else:
            pygame.draw.rect(self.mainSurface, (255, 0, 0), [self.xPos, self.yPos, self.width, self.height], 0)

    def collidingRight(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 < self.xPos:
                if platform.checkLeftCollide(self.rightEnemyRect):
                    self.rightColliding = True
                    return True
        self.rightColliding = False
        return False

    def collidingLeft(self, platforms: list):
        for platform in platforms:
            if platform.xPos + platform.width + 100 > self.xPos:
                if platform.checkRightCollide(self.leftEnemyRect):
                    self.leftColliding = True
                    return True
        self.leftColliding = False
        return False

    def collidingTop(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkBottomCollide(self.topEnemyRect):
                    return True
        return False

    def collidingBottom(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomEnemyRect):
                    return True
        return False

    def getCollidingBottomRect(self, platforms: list):
        for platform in platforms:
            if platform.xPos - 100 <= self.xPos <= platform.xPos + platform.width + 100:
                if platform.checkTopCollide(self.bottomEnemyRect):
                    return platform
        return None

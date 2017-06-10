import copy

import pygame

import GhostEnemy
import RectPlatform
import ShooterEnemy
import ZombieEnemy
import batEnemy
import slimeEnemy
import tools

pygame.display.init()
pygame.display.set_mode((1, 1))


# Surfaces that will be reused for each level
gameSurface = pygame.Surface((15000, 5000), pygame.DOUBLEBUF)
gameSurface.set_alpha(None)

platformSurface = pygame.Surface((15000, 5000), pygame.SRCALPHA)


class Animations:
    class Character:
        runningAnimation = tools.loadAnimation("charRunning", "sprites/character/running", 1, 27)
        idleAnimation = tools.loadAnimation("charIdle", "sprites/character/idle", 1, 22)
        runningDustAnimation = tools.loadAnimation("dirtTrail", "sprites/character/dirt_trail", 1, 20)
        jumpingAnimation = tools.loadAnimation("jumping", "sprites/character/jumping", 1, 3)
        fallingAnimation = tools.loadAnimation("falling", "sprites/character/falling", 1, 3)

        runningAnimation = tools.scaleImages(runningAnimation, 0.5)
        idleAnimation = tools.scaleImages(idleAnimation, 0.5)
        runningDustAnimation = tools.scaleImages(runningDustAnimation, 0.5)
        jumpingAnimation = tools.scaleImages(jumpingAnimation, 0.5)
        fallingAnimation = tools.scaleImages(fallingAnimation, 0.5)

    class SlimeEnemy:
        movingAnimation = tools.loadAnimation("greenSlime", "sprites/enemies/slime", 1, 10)
        movingAnimation = tools.scaleImages(movingAnimation, 1.5)

    class BatEnemy:
        mainAnimation = tools.loadAnimation("batEnemy", "sprites/enemies/batEnemy", 1, 9)
        mainAnimation = tools.scaleImages(mainAnimation, 0.3)

    class GhostEnemy:
        movingAnimation = tools.loadAnimation("ghost", "sprites/enemies/ghostEnemy", 1, 5)

    class ZombieEnemy:
        movingAnimation = tools.loadAnimation("Walk", "sprites/enemies/zombie/moving", 1, 10)
        movingAnimation = tools.scaleImages(movingAnimation, 0.2)

        jumpingAnimation = tools.loadAnimation("Jump", "sprites/enemies/zombie/jump", 1, 3)
        jumpingAnimation = tools.scaleImages(jumpingAnimation, 0.2)

    class ShooterEnemy:
        idleAnimation = tools.loadAnimation("idle","sprites/enemies/shooterEnemy",1,3)
        shootingAnimation = tools.loadAnimation("shooting","sprites/enemies/shooterEnemy",1,3)


class Images:
    class Heart:
        mainHeart = pygame.transform.scale(pygame.image.load("sprites/healthHeart.png"), (50, 50))

    class Bullet:
        bulletImage = pygame.transform.scale(pygame.image.load("sprites/bullet1.png").convert(), (25, 35))
        bulletImage.set_colorkey((255, 255, 255))

        fireBallImage = pygame.image.load("sprites/FireBall.png").convert()
        fireBallImage.set_colorkey((255, 255, 255))



    class Tiles:
        class FloorImages:
            grassFloorImage1 = pygame.image.load("sprites/floorstuff.png").convert()
            grassFloorImage1.set_colorkey((255, 255, 255))

            glassFloorImageGrave = pygame.image.load("sprites/GraveGrass.png").convert()
            grassFloorImage1.set_colorkey((255,255,255))

            graveTree = pygame.image.load("sprites/graveTree.png")

        class Crates:
            mainCrate = pygame.image.load("sprites/crates/Crate.png").convert()
            mainCrate.set_colorkey((255, 255, 255))

            attachedCrates1 = pygame.image.load("sprites/crates/longCrate.png").convert()
            attachedCrates1.set_colorkey((255, 255, 255))

            graveCrate = pygame.image.load("sprites/crates/graveCrate.png").convert()
            graveCrate.set_colorkey((255, 255, 255))


        endGameBlock = pygame.image.load("sprites/gameEndBlock.png").convert()
        endGameBlock.set_colorkey((255,255,255))

class Levels:
    class Level1:
        # 15000 x 5000
        # starting point at 1000,2300
        enemies = []
        platforms = []
        bullets = []

        def __init__(self, surface: pygame.Surface):
            self.generateFloor(surface)
            self.createPlatformsAndEnemies(surface)
            # print("length plaforms ",len(self.platforms))
            # print("length enemies ",len(self.enemies))

        def generateFloor(self, surface: pygame.Surface):
            floorGapsList = [5, 6, 11,17,18,19,20,21,22,23,24, 25,26,27,28, 29, 34, 41, 45]

            self.platforms.append(RectPlatform.RectPlatform(surface, 744, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.grassFloorImage1))
            self.platforms.append(RectPlatform.RectPlatform(surface, 488, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.grassFloorImage1))
            # 50 iterations
            floorCount = 0
            for x in range(1000, 13100, 256):
                if floorCount not in floorGapsList:
                    self.platforms.append(RectPlatform.RectPlatform(surface, x, 2300, 256, 256,
                                                                    image=Images.Tiles.FloorImages.grassFloorImage1))
                floorCount += 1

        def enemyCopy(self):
            returnList = []
            for enemy in self.enemies:
                returnList.append(copy.copy(enemy))

            return returnList

        def createPlatformsAndEnemies(self, surface: pygame.Surface):
            # made left to right
            generateCrateGrid(surface,self.platforms,1200,2050,1,2)
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 1328, 2050, 64,64,image=Images.Tiles.Crates.mainCrate,
                                          tag="fireball"))
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 1392, 2050, 64, 64, image=Images.Tiles.Crates.mainCrate))

            #WALL TO THE LEFT (INVISIBLE)
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 900, 0, 100, 5000))

            #Wall on bottom to judge if character fell off

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 0, 3000, 150000, 100,tag="deathPlatform"))


            self.platforms.append(
                RectPlatform.RectPlatform(surface, 1296, 1800, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate, tag="health"))

            generateStaircase(self.platforms, surface, 2024, 2300,4)

            generateCrateGrid(surface,self.platforms,2664,2236,1,3)

            generateCrateGrid(surface, self.platforms, 3200, 2050, 1, 4)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 3220, 2000,shootBalls=True))

            self.enemies.append(slimeEnemy.SlimeEnemy(surface,3500,2200))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 3456, 2236, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate, tag="health"))

            generateStaircase(self.platforms, surface, 4150, 2300, 4)

            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 4800, 2200,speed=3))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 4900, 2200,speed=4))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 5000, 2200,speed=5))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 5200, 2236, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate))

            #Parkour/Obstecle Cource section
            generateCrateGrid(surface,self.platforms,5500,2050,1,4)

            self.enemies.append(ShooterEnemy.ShooterEnemy(surface,6100,2150))
            generateCrateGrid(surface, self.platforms, 6100, 2200, 1, 2)

            generateCrateGrid(surface, self.platforms, 6350, 1950, 1, 2)

            generateCrateGrid(surface, self.platforms, 6750, 1700, 1, 2)

            generateCrateGrid(surface, self.platforms, 7200, 1800, 1, 2)

            generateCrateGrid(surface, self.platforms, 7650, 1900, 1, 2)

            generateCrateGrid(surface, self.platforms, 8000, 2100, 1, 4)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface,8100,2050))

            generateCrateGrid(surface, self.platforms, 8700, 2236, 1, 2)
            self.enemies.append(slimeEnemy.SlimeEnemy(surface,8800,2180,speed=6))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface,8900,2180,speed=6))

            generateCrateGrid(surface, self.platforms, 9000, 2075, 1, 2)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface,9050,1975,shootBalls=True))
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 9128, 2075, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate, tag="health"))
            generateCrateGrid(surface, self.platforms, 9192, 2075, 1, 2)

            generateCrateGrid(surface, self.platforms, 9500, 2236, 1, 2)

            generateStaircase(self.platforms,surface,9960,2300,7)

            self.enemies.append(slimeEnemy.SlimeEnemy(surface,11000,2180,speed=6))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface,10500,2180,speed=6))

            generateCrateGrid(surface, self.platforms, 11308, 2236, 1, 2)


            generateCrateGrid(surface, self.platforms, 11900, 1900, 1, 7)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 11900, 1850, shootBalls=True))

            # INVISIBLE WALL AT RIGHT LEFT OF MAP
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 13300, 0, 100, 5000,tag="endGame"))

            # Show transition into next level theme
            for graveX in range(3):
                self.platforms.append(
                    RectPlatform.RectPlatform(surface, 13500 + graveX * 256, 2300, 256, 256,image=Images.Tiles.FloorImages.glassFloorImageGrave))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 13550, 1900, 250, 400,image=Images.Tiles.FloorImages.graveTree))

    class Level2:
        # 15000 x 5000
        # starting point at 1000,2300
        enemies = []
        platforms = []
        bullets = []

        def __init__(self, surface: pygame.Surface):
            self.generateFloor(surface)
            self.createPlatformsAndEnemies(surface)
            # print("length plaforms ", len(self.platforms))
            # print("length enemies ", len(self.enemies))

        def generateFloor(self, surface: pygame.Surface):
            floorGapsList = [4, 5, 15, 16, 23, 24, 25, 26, 27, 28]

            self.platforms.append(RectPlatform.RectPlatform(surface, 744, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.glassFloorImageGrave))
            self.platforms.append(RectPlatform.RectPlatform(surface, 488, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.glassFloorImageGrave))
            # 50 iterations
            floorCount = 0
            for x in range(1000, 14000, 256):
                if floorCount not in floorGapsList:
                    self.platforms.append(RectPlatform.RectPlatform(surface, x, 2300, 256, 256,
                                                                    image=Images.Tiles.FloorImages.glassFloorImageGrave))
                floorCount += 1

        def enemyCopy(self):
            returnList = []
            for enemy in self.enemies:
                returnList.append(copy.copy(enemy))
            return returnList

        def createPlatformsAndEnemies(self, surface: pygame.Surface):
            # made left to right
            #starts atg 1000
            # WALL TO THE LEFT (INVISIBLE)
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 900, 0, 100, 5000))

            # Wall on bottom to judge if character fell off
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 0, 3000, 150000, 100, tag="deathPlatform"))

            self.enemies.append(batEnemy.BatEnemy(surface,2224,2225,200))

            generateStaircase(self.platforms,surface,2536,2300,4,Images.Tiles.Crates.graveCrate)

            self.enemies.append(ZombieEnemy.ZombieEnemy(surface,2836,2220))

            generateReverseStaircase(self.platforms, surface, 4586,2300,4,Images.Tiles.Crates.graveCrate)
            self.enemies.append(GhostEnemy.GhostEnemy(surface,3900,2300))
            self.enemies.append(GhostEnemy.GhostEnemy(surface,4586,2300))

            self.enemies.append(batEnemy.BatEnemy(surface,5070,2200,200))

            generateCrateGrid(surface, self.platforms, 5400, 2236, 1, 1, Images.Tiles.Crates.graveCrate)

            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 5430, 2250, speed=4))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 5730, 2250, speed=5))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 6030, 2250, speed=6))

            self.enemies.append(GhostEnemy.GhostEnemy(surface, 6030, 2100, speed=5))

            generateCrateGrid(surface, self.platforms, 6400, 2236, 1, 1, Images.Tiles.Crates.graveCrate)

            generateStaircase(self.platforms, surface, 6564, 2300, 5, Images.Tiles.Crates.graveCrate)

            self.enemies.append(batEnemy.BatEnemy(surface, 6950, 1900, 200))
            self.enemies.append(batEnemy.BatEnemy(surface, 7150, 1900, 200))
            self.enemies.append(batEnemy.BatEnemy(surface, 7350, 1900, 200))
            self.enemies.append(batEnemy.BatEnemy(surface, 7550, 1900, 200))
            self.enemies.append(batEnemy.BatEnemy(surface, 7750, 1900, 200))
            self.enemies.append(batEnemy.BatEnemy(surface, 7950, 1900, 200))

            generateReverseStaircase(self.platforms, surface, 8424, 2300, 4, Images.Tiles.Crates.graveCrate)

            # INVISIBLE WALL AT RIGHT LEFT OF MAP
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 13500, 0, 100, 5000))


def generateStaircase(platforms: list, surface: pygame.Surface, x, y,rowCount : int,imageIn = Images.Tiles.Crates.mainCrate):
    for yCount in range(rowCount+1):
        xPos = x + (yCount-1) * 64
        yPos = y - yCount * 64
        generateCrateGrid(surface,platforms,xPos,yPos,yCount,1,image=imageIn)

        # platforms.append(RectPlatform.RectPlatform(surface,x + rowCount * 64,y - rowCount * 64,10,rowCount * 64,tag="specSurface")) # specSurface indicates only certain elements interact

def generateReverseStaircase(platforms: list, surface: pygame.Surface, x, y,rowCount : int,imageIn = Images.Tiles.Crates.mainCrate):
    for yCount in range(rowCount+1):
        xPos = x + rowCount * 64 - (yCount-1) * 64 - 64
        yPos = y - yCount * 64
        generateCrateGrid(surface,platforms,xPos,yPos,yCount,1,image=imageIn)

        # platforms.append(RectPlatform.RectPlatform(surface,x-10,y - rowCount * 64,10,rowCount * 64,tag="specSurface")) # specSurface indicates only certain elements interact

def generateCrateGrid(surface : pygame.Surface,platforms : list, x : int,y : int,rows :int,columns : int,image = Images.Tiles.Crates.mainCrate):
    for xCount in range(columns):
        for yCount in range(rows):
            xPos = x + 64 * xCount
            yPos = y + 64 * yCount
            platforms.append(
                RectPlatform.RectPlatform(surface, xPos, yPos, 64, 64,
                                          image=image))


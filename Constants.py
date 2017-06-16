# used to return copy of a list
import copy

import pygame

import GhostEnemy
import RectPlatform
import ShooterEnemy
import ZombieBoss
import ZombieEnemy
import batEnemy
import slimeEnemy
import tools

# Surfaces that will be reused for each level
# Surface game is played on
gameSurface = pygame.Surface((15000, 5000), pygame.DOUBLEBUF)
gameSurface.set_alpha(None)

# Surface platforms are drawn on, subsurfaces of this are taken
platformSurface = pygame.Surface((15000, 5000), pygame.SRCALPHA)


# Class to hold all animations
class Animations:
    class Character:
        # Load animations
        runningAnimation = tools.loadAnimation("charRunning", "sprites/character/running", 1, 27)
        idleAnimation = tools.loadAnimation("charIdle", "sprites/character/idle", 1, 22)
        runningDustAnimation = tools.loadAnimation("dirtTrail", "sprites/character/dirt_trail", 1, 20)
        jumpingAnimation = tools.loadAnimation("jumping", "sprites/character/jumping", 1, 3)
        fallingAnimation = tools.loadAnimation("falling", "sprites/character/falling", 1, 3)

        # Scale animations
        runningAnimation = tools.scaleImages(runningAnimation, 0.5)
        idleAnimation = tools.scaleImages(idleAnimation, 0.5)
        runningDustAnimation = tools.scaleImages(runningDustAnimation, 0.5)
        jumpingAnimation = tools.scaleImages(jumpingAnimation, 0.5)
        fallingAnimation = tools.scaleImages(fallingAnimation, 0.5)

    class SlimeEnemy:
        # Load and scale animations
        movingAnimation = tools.loadAnimation("greenSlime", "sprites/enemies/slime", 1, 10)
        movingAnimation = tools.scaleImages(movingAnimation, 1.5)

    class BatEnemy:
        # Load and scale animations
        mainAnimation = tools.loadAnimation("batEnemy", "sprites/enemies/batEnemy", 1, 9)
        mainAnimation = tools.scaleImages(mainAnimation, 0.3)

    class GhostEnemy:
        movingAnimation = tools.loadAnimation("ghost", "sprites/enemies/ghostEnemy", 1, 5)

    class ZombieEnemy:
        # Load and scale animations
        movingAnimation = tools.loadAnimation("Walk", "sprites/enemies/zombie/moving", 1, 10)
        movingAnimation = tools.scaleImages(movingAnimation, 0.2)

        jumpingAnimation = tools.loadAnimation("Jump", "sprites/enemies/zombie/jump", 1, 3)
        jumpingAnimation = tools.scaleImages(jumpingAnimation, 0.2)

    class ShooterEnemy:
        # Load and scale animations
        idleAnimation = tools.loadAnimation("idle", "sprites/enemies/shooterEnemy", 1, 3)
        shootingAnimation = tools.loadAnimation("shooting", "sprites/enemies/shooterEnemy", 1, 3)


class Images:
    class Logos:
        # load logo
        mainLogo = pygame.image.load("sprites/mainLogo.png")

    class Heart:
        # Load health image
        mainHeart = pygame.transform.scale(pygame.image.load("sprites/healthHeart.png"), (50, 50))

    class Bullet:
        # load and configure bullet images
        bulletImage = pygame.transform.scale(pygame.image.load("sprites/bullet1.png").convert(), (25, 35))
        bulletImage.set_colorkey((255, 255, 255))

        fireBallImage = pygame.image.load("sprites/FireBall.png").convert()
        fireBallImage.set_colorkey((255, 255, 255))

    class Tiles:
        class FloorImages:
            # load and configure images
            grassFloorImage1 = pygame.image.load("sprites/floorstuff.png").convert()
            grassFloorImage1.set_colorkey((255, 255, 255))

            glassFloorImageGrave = pygame.image.load("sprites/GraveGrass.png").convert()
            grassFloorImage1.set_colorkey((255, 255, 255))

            graveTree = pygame.image.load("sprites/graveTree.png")

        class Crates:
            # load and configure images
            mainCrate = pygame.image.load("sprites/crates/Crate.png").convert()
            mainCrate.set_colorkey((255, 255, 255))

            attachedCrates1 = pygame.image.load("sprites/crates/longCrate.png").convert()
            attachedCrates1.set_colorkey((255, 255, 255))

            graveCrate = pygame.image.load("sprites/crates/graveCrate.png").convert()
            graveCrate.set_colorkey((255, 255, 255))

            hitThisCrate = pygame.image.load("sprites/crates/hitThisCrate.png").convert()
            hitThisCrate.set_colorkey((255, 255, 255))

        # load and configure images
        endGameBlock = pygame.image.load("sprites/gameEndBlock.png").convert()
        endGameBlock.set_colorkey((255, 255, 255))


class Levels:
    # Generate level 1
    class Level1:
        # 15000 x 5000
        # Lists for game objects
        enemies = []
        platforms = []
        bullets = []

        # initialize level
        def __init__(self, surface: pygame.Surface):
            self.generateFloor(surface)
            self.createPlatformsAndEnemies(surface)

        # Generate floor of level
        def generateFloor(self, surface: pygame.Surface):
            # make gaps at these floor points
            floorGapsList = [5, 6, 11, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 34, 41, 45]

            # add platforms at borders of map
            self.platforms.append(RectPlatform.RectPlatform(surface, 744, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.grassFloorImage1))
            self.platforms.append(RectPlatform.RectPlatform(surface, 488, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.grassFloorImage1))
            # 50 iterations
            floorCount = 0
            # generate floor
            for x in range(1000, 13100, 256):
                # if it isnt in the gap list, add a platform
                if floorCount not in floorGapsList:
                    self.platforms.append(RectPlatform.RectPlatform(surface, x, 2300, 256, 256,
                                                                    image=Images.Tiles.FloorImages.grassFloorImage1))
                floorCount += 1

        # create copy of enemy list
        def enemyCopy(self):
            returnList = []
            # create a copy of all enemies and put them in a list
            for enemy in self.enemies:
                returnList.append(copy.copy(enemy))

            return returnList  # return list of copies

        # create platforms and enemies
        def createPlatformsAndEnemies(self, surface: pygame.Surface):
            # made left to right
            generateCrateGrid(surface, self.platforms, 1200, 2050, 1, 2)
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 1328, 2050, 64, 64, image=Images.Tiles.Crates.hitThisCrate,
                                          tag="fireball"))
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 1392, 2050, 64, 64, image=Images.Tiles.Crates.mainCrate))

            # WALL TO THE LEFT (INVISIBLE)
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 900, 0, 100, 5000))

            # Wall on bottom to judge if character fell off

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 0, 3000, 150000, 100, tag="deathPlatform"))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 1296, 1800, 64, 64,
                                          image=Images.Tiles.Crates.hitThisCrate, tag="health"))

            generateStaircase(self.platforms, surface, 2024, 2300, 4)

            generateCrateGrid(surface, self.platforms, 2664, 2236, 1, 3)

            generateCrateGrid(surface, self.platforms, 3200, 2050, 1, 4)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 3220, 2000, shootBalls=True))

            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 3500, 2200))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 3456, 2236, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate, tag="health"))

            generateStaircase(self.platforms, surface, 4150, 2300, 4)

            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 4800, 2200, speed=3))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 4900, 2200, speed=4))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 5000, 2200, speed=5))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 5200, 2236, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate))

            # Parkour/Obstecle Cource section
            generateCrateGrid(surface, self.platforms, 5500, 2050, 1, 4)

            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 6100, 2150))
            generateCrateGrid(surface, self.platforms, 6100, 2200, 1, 2)

            generateCrateGrid(surface, self.platforms, 6350, 1950, 1, 2)

            generateCrateGrid(surface, self.platforms, 6750, 1700, 1, 2)

            generateCrateGrid(surface, self.platforms, 7200, 1800, 1, 2)

            generateCrateGrid(surface, self.platforms, 7650, 1900, 1, 2)

            generateCrateGrid(surface, self.platforms, 8000, 2100, 1, 4)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 8100, 2050))

            generateCrateGrid(surface, self.platforms, 8700, 2236, 1, 2)
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 8800, 2180, speed=6))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 8900, 2180, speed=6))

            generateCrateGrid(surface, self.platforms, 9000, 2075, 1, 2)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 9050, 1975, shootBalls=True))
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 9128, 2075, 64, 64,
                                          image=Images.Tiles.Crates.mainCrate, tag="health"))
            generateCrateGrid(surface, self.platforms, 9192, 2075, 1, 2)

            generateCrateGrid(surface, self.platforms, 9500, 2236, 1, 2)

            generateStaircase(self.platforms, surface, 9960, 2300, 7)

            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 11000, 2180, speed=6))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 10500, 2180, speed=6))

            generateCrateGrid(surface, self.platforms, 11308, 2236, 1, 2)

            generateCrateGrid(surface, self.platforms, 11900, 1900, 1, 7)
            self.enemies.append(ShooterEnemy.ShooterEnemy(surface, 11900, 1850, shootBalls=True))

            # INVISIBLE WALL AT RIGHT LEFT OF MAP
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 13300, 0, 100, 5000, tag="endGame"))

            # Show transition into next level theme
            for graveX in range(3):
                self.platforms.append(
                    RectPlatform.RectPlatform(surface, 13500 + graveX * 256, 2300, 256, 256,
                                              image=Images.Tiles.FloorImages.glassFloorImageGrave))

            self.platforms.append(
                RectPlatform.RectPlatform(surface, 13550, 1900, 250, 400, image=Images.Tiles.FloorImages.graveTree))

    class Level2:
        # 15000 x 5000
        # lists for game objects
        enemies = []
        platforms = []
        bullets = []

        # initialize levels
        def __init__(self, surface: pygame.Surface):
            self.generateFloor(surface)
            self.createPlatformsAndEnemies(surface)
            # print("length plaforms ", len(self.platforms))
            # print("length enemies ", len(self.enemies))

        def generateFloor(self, surface: pygame.Surface):
            # points to create gaps in generation of floor
            floorGapsList = [4, 5, 15, 16, 23, 24, 25, 26, 27, 28]

            # add platforms to borders
            self.platforms.append(RectPlatform.RectPlatform(surface, 744, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.glassFloorImageGrave))
            self.platforms.append(RectPlatform.RectPlatform(surface, 488, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.glassFloorImageGrave))
            # 50 iterations
            floorCount = 0
            for x in range(1000, 14000, 256):
                # if it isnt in the gap list, add a platform
                if floorCount not in floorGapsList:
                    self.platforms.append(RectPlatform.RectPlatform(surface, x, 2300, 256, 256,
                                                                    image=Images.Tiles.FloorImages.glassFloorImageGrave))
                floorCount += 1

        # return copy of all enemies
        def enemyCopy(self):
            returnList = []
            # add copy of enemy to list
            for enemy in self.enemies:
                returnList.append(copy.copy(enemy))
            return returnList  # retur enemy copies

        # Generate platforms and enemies
        def createPlatformsAndEnemies(self, surface: pygame.Surface):
            # made left to right
            # starts at 1000
            # WALL TO THE LEFT (INVISIBLE)
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 900, 0, 100, 5000))

            # Wall on bottom to judge if character fell off
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 0, 3000, 150000, 100, tag="deathPlatform"))

            self.enemies.append(batEnemy.BatEnemy(surface, 2224, 2225, 200))

            generateStaircase(self.platforms, surface, 2536, 2300, 4, Images.Tiles.Crates.graveCrate)

            self.enemies.append(ZombieEnemy.ZombieEnemy(surface, 2836, 2220))

            generateReverseStaircase(self.platforms, surface, 4586, 2300, 4, Images.Tiles.Crates.graveCrate)
            self.enemies.append(GhostEnemy.GhostEnemy(surface, 3900, 2300))
            self.enemies.append(GhostEnemy.GhostEnemy(surface, 4586, 2300))

            self.enemies.append(batEnemy.BatEnemy(surface, 5070, 2200, 200))

            generateCrateGrid(surface, self.platforms, 5400, 2236, 1, 1, Images.Tiles.Crates.graveCrate)

            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 5430, 2250, speed=4))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 5730, 2250, speed=5))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 6030, 2250, speed=6))

            self.enemies.append(GhostEnemy.GhostEnemy(surface, 6030, 2100, speed=5))

            generateStaircase(self.platforms, surface, 6564, 2300, 5, Images.Tiles.Crates.graveCrate)

            self.enemies.append(batEnemy.BatEnemy(surface, 6950, 1900, 100))
            self.enemies.append(batEnemy.BatEnemy(surface, 7150, 1900, 100))
            self.enemies.append(batEnemy.BatEnemy(surface, 7350, 1900, 100))
            self.enemies.append(batEnemy.BatEnemy(surface, 7550, 1900, 100))
            self.enemies.append(batEnemy.BatEnemy(surface, 7750, 1900, 100))
            self.enemies.append(batEnemy.BatEnemy(surface, 7950, 1900, 100))

            generateReverseStaircase(self.platforms, surface, 8424, 2300, 2, Images.Tiles.Crates.graveCrate)

            self.enemies.append(ZombieEnemy.ZombieEnemy(surface, 8900, 2200))
            self.enemies.append(ZombieEnemy.ZombieEnemy(surface, 9200, 2200))
            self.enemies.append(slimeEnemy.SlimeEnemy(surface, 8600, 2200))

            generateStaircase(self.platforms, surface, 9300, 2300, 2, Images.Tiles.Crates.graveCrate)

            # INVISIBLE WALL AT RIGHT LEFT OF MAP
            self.platforms.append(
                RectPlatform.RectPlatform(surface, 9800, 0, 100, 5000, tag="endGame"))

    class Level3:
        # 15000 x 5000
        # list for game objects
        enemies = []
        platforms = []
        bullets = []

        # initialize level
        def __init__(self, surface: pygame.Surface):
            self.generateFloor(surface)
            self.createPlatformsAndEnemies(surface)

        # generate floor
        def generateFloor(self, surface: pygame.Surface):
            # floor for level borders
            self.platforms.append(RectPlatform.RectPlatform(surface, 744, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.glassFloorImageGrave))
            self.platforms.append(RectPlatform.RectPlatform(surface, 488, 2300, 256, 256,
                                                            image=Images.Tiles.FloorImages.glassFloorImageGrave))
            # generate floor
            for x in range(1000, 5000, 256):
                self.platforms.append(RectPlatform.RectPlatform(surface, x, 2300, 256, 256,
                                                                image=Images.Tiles.FloorImages.glassFloorImageGrave))

        # return copy of enemies
        def enemyCopy(self):
            returnList = []
            for enemy in self.enemies:  # copy all enemies and add them to a list
                returnList.append(copy.copy(enemy))
            return returnList  # return list of enemy copies

        # generate platforms and enemies
        def createPlatformsAndEnemies(self, surface: pygame.Surface):
            # made left to right
            generateCrateGrid(surface, self.platforms, 1200, 1340, 15, 1, image=Images.Tiles.Crates.graveCrate)
            generateCrateGrid(surface, self.platforms, 1264, 2044, 1, 1, image=Images.Tiles.Crates.graveCrate)

            generateCrateGrid(surface, self.platforms, 2700, 1340, 15, 1, image=Images.Tiles.Crates.graveCrate)
            generateCrateGrid(surface, self.platforms, 2636, 2044, 1, 1, image=Images.Tiles.Crates.graveCrate)

            # Roof
            generateCrateGrid(surface, self.platforms, 1200, 1276, 1, 25, image=Images.Tiles.Crates.graveCrate)

            # Top creates
            generateCrateGrid(surface, self.platforms, 1648, 1980, 1, 1, image=Images.Tiles.Crates.graveCrate)
            generateCrateGrid(surface, self.platforms, 1950, 1980, 1, 1, image=Images.Tiles.Crates.graveCrate)
            generateCrateGrid(surface, self.platforms, 2252, 1980, 1, 1, image=Images.Tiles.Crates.graveCrate)

            self.enemies.append(ZombieBoss.ZombieEnemy(surface, 1950, 1900, health=10))


# Generate staircase
def generateStaircase(platforms: list, surface: pygame.Surface, x, y, rowCount: int,
                      imageIn=Images.Tiles.Crates.mainCrate):
    for yCount in range(rowCount + 1):  # for row amount inputted
        xPos = x + (yCount - 1) * 64  # calculate position
        yPos = y - yCount * 64
        generateCrateGrid(surface, platforms, xPos, yPos, yCount, 1,
                          image=imageIn)  # generate crate grid for stair levels


# Generate staircase in opposite direction
def generateReverseStaircase(platforms: list, surface: pygame.Surface, x, y, rowCount: int,
                             imageIn=Images.Tiles.Crates.mainCrate):
    for yCount in range(rowCount + 1):  # for row amount input
        xPos = x + rowCount * 64 - (yCount - 1) * 64 - 64  # calculate position
        yPos = y - yCount * 64
        generateCrateGrid(surface, platforms, xPos, yPos, yCount, 1,
                          image=imageIn)  # generate crate grid for stair levels


# generate a grid of crates
def generateCrateGrid(surface: pygame.Surface, platforms: list, x: int, y: int, rows: int, columns: int,
                      image=Images.Tiles.Crates.mainCrate):
    for xCount in range(columns):  # for all columns inputted
        for yCount in range(rows):  # for all rows inputted
            xPos = x + 64 * xCount  # calculate position
            yPos = y + 64 * yCount
            platforms.append(  # add platform
                RectPlatform.RectPlatform(surface, xPos, yPos, 64, 64,
                                          image=image))

import random

from pygame import *

import Background
import Bullet
import Character
import Constants
import tools

gameSurface = Constants.gameSurface

platformSurface = Constants.platformSurface

Constants.Levels.Level3(gameSurface)

event.set_allowed(KEYDOWN | QUIT)  # Allows for more efficiant events


def checkWin(enemyList: list):
    for enemy in enemyList:
        if enemy.tag == "zombieBoss":
            return False

    return True

def start(screen):
    gameSurface.fill((0, 0, 0))

    character = Character.Character(gameSurface, startPos=(1300, 2200), width=43, height=68)
    mainClock = time.Clock()

    cameraX = character.xPos - 500
    cameraY = character.yPos - 400

    backgroundMain = Background.Background(gameSurface, character, cameraX, cameraY, graveScene=True)

    # FIX REFERENCE ISSUE

    platforms = Constants.Levels.Level3.platforms

    """
    #Return copy of enemy list because otherwise the
    reference would be to the same enemies that were killed the
    last time the level was run
    """
    enemyList = Constants.Levels.Level3.enemyCopy(Constants.Levels.Level3)
    pickupsList = []
    bullets = []

    done = False
    fpsCount = 0
    fpsTotal = 0

    bulletSpawnCount = 0
    bulletSpawnCountLimit = 100

    platformSurface.fill((0, 0, 0, 0))

    """
    Generated a Surface for all unmoving platforms
    It is faster to blit subsurfaces from this rather then
    blit surfaces in view during every iteraton
    """
    for platform in platforms:
        platform.display(surface=platformSurface)
        if platform.tag == "health" or platform.tag == "fireball":
            platform.droppedAlready = False  # Reset the platform so new list doesnt have to be generated

    while not done:
        # Set camera position
        cameraX = character.xPos - 500
        cameraY = character.yPos - 400

        # Get events, passed to character class later
        events = event.get()
        for e in events:
            if e.type == QUIT:  # Quit the level
                done = True
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:  # Open a pause menu
                    pauseAnswer = tools.pauseScreen(screen, screen)
                    if pauseAnswer == "mainMenu":
                        return "mainMenu"
                    elif pauseAnswer == "playAgain":
                        return "level3"

        # Send inputs from user to character for control
        character.playerControl(events, bullets)

        # Control character actions and movements
        character.moveCharacter(platforms, enemyList, pickupsList, bullets)

        # End game if character dies
        if character.dead:
            done = True
            pauseAnswer = tools.pauseScreen(screen, screen)
            if pauseAnswer == "playAgain" or pauseAnswer == "escape":
                return "level3"
            else:
                return "mainMenu"

        # Raining bullets generate between x 1300 - 2700 at a y 1300
        if bulletSpawnCount >= bulletSpawnCountLimit:
            bullets.append(Bullet.Bullet(gameSurface, random.randint(1300, 2600), 1400, 90,
                                         image=Constants.Images.Bullet.bulletImage,
                                         defaultImageAngle=-90, speed=1.5, hurtPlayer=True))
            bulletSpawnCount = 0
        bulletSpawnCount += 1

        # Control all game objects
        tools.controlEnemies(enemyList, platforms, character, bullets)
        tools.controlBullets(bullets, platforms)
        tools.controlPickups(pickupsList, platforms)

        #
        if checkWin(enemyList):
            pauseAnswer = tools.pauseScreen(screen, screen)
            if pauseAnswer == "mainMenu" or pauseAnswer == "escape":
                return "mainMenu"
            elif pauseAnswer == "playAgain":
                return "level3"

        # Control and display background
        backgroundMain.control(cameraX, cameraY)
        backgroundMain.display()

        # Display platforms via generated surface
        gameSurface.blit(platformSurface.subsurface(Rect(cameraX, cameraY, 1000, 700)), (cameraX, cameraY))

        # Display all game objects
        character.display()
        tools.displayEnemies(enemyList, cameraX)
        tools.displayBullets(bullets, cameraX)
        tools.displayPickups(pickupsList, cameraX)

        # Get subsurface to display
        camera = gameSurface.subsurface(Rect(cameraX, cameraY, 1000, 700))

        # Display game screen
        screen.blit(camera, (0, 0))

        # display GUI
        character.displayHealth(screen)
        character.displayBalls(screen)

        mainClock.tick(60)  # Set Frame Cap to 60
        fps = mainClock.get_fps()  # Get FPS

        display.flip()  # Update the display

        # Calculate average fps
        fpsCount += 1
        fpsTotal += fps
        averageFps = fpsTotal / fpsCount

        if character.moveToNextLevel:
            pauseAnswer = tools.pauseScreen(screen, screen)
            if pauseAnswer == "mainMenu":
                return "mainMenu"
            elif pauseAnswer == "playAgain":
                return "level3"

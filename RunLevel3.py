from pygame import *

import Background
import Character
import Constants
import tools

gameSurface = Constants.gameSurface

platformSurface = Constants.platformSurface

Constants.Levels.Level3(gameSurface)

event.set_allowed(KEYDOWN | QUIT)  # Allows for more efficiant events


def start(screen):
    gameSurface.fill((0, 0, 0))

    character = Character.Character(gameSurface, startPos=(1050, 2200), width=43, height=68)
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

        # Control all game objects
        tools.controlEnemies(enemyList, platforms, character, bullets)
        tools.controlBullets(bullets, platforms)
        tools.controlPickups(pickupsList, platforms)

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

                # print(int(character.xPos),int(character.yPos))
                # print("average fps: ", str(averageFps))
                # print(fps)
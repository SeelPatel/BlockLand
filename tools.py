import pygame


# load some button and menu images
# I did this here because Constants imports this file
# If i declared these variables in Constants, then these files would have imported eachother
# this can cause some issues
class ButtonsAndPause:
    playAgain = pygame.image.load("sprites/buttons/playAgain.png").convert()
    playAgain.set_colorkey((255, 255, 255))

    playAgainHover = pygame.image.load("sprites/buttons/playAgainHover.png").convert()
    playAgainHover.set_colorkey((255, 255, 255))

    mainMenu = pygame.image.load("sprites/buttons/mainMenu.png").convert()
    mainMenu.set_colorkey((255, 255, 255))

    mainMenuHover = pygame.image.load("sprites/buttons/mainMenuHover.png").convert()
    mainMenuHover.set_colorkey((255, 255, 255))

    nextLevel = pygame.image.load("sprites/buttons/nextLevel.png").convert()
    nextLevel.set_colorkey((255, 255, 255))

    nextLevelHover = pygame.image.load("sprites/buttons/nextLevelHover.png").convert()
    nextLevelHover.set_colorkey((255, 255, 255))

    playGame = pygame.image.load("sprites/buttons/playGame.png").convert()
    playGame.set_colorkey((255, 255, 255))

    playGameHover = pygame.image.load("sprites/buttons/playGameHover.png").convert()
    playGameHover.set_colorkey((255, 255, 255))

    aboutGame = pygame.image.load("sprites/buttons/about.png").convert()
    aboutGame.set_colorkey((255, 255, 255))

    aboutGameHover = pygame.image.load("sprites/buttons/aboutHover.png").convert()
    aboutGameHover.set_colorkey((255, 255, 255))

    level1 = pygame.image.load("sprites/buttons/level1.png").convert()
    level1.set_colorkey((255, 255, 255))
    level1Hover = pygame.image.load("sprites/buttons/level1Hover.png").convert()
    level1Hover.set_colorkey((255, 255, 255))

    level2 = pygame.image.load("sprites/buttons/level2.png").convert()
    level2.set_colorkey((255, 255, 255))
    level2Hover = pygame.image.load("sprites/buttons/level2Hover.png").convert()
    level2Hover.set_colorkey((255, 255, 255))

    level3 = pygame.image.load("sprites/buttons/level3.png").convert()
    level3.set_colorkey((255, 255, 255))
    level3Hover = pygame.image.load("sprites/buttons/level3Hover.png").convert()
    level3Hover.set_colorkey((255, 255, 255))

    backButton = pygame.image.load("sprites/buttons/back.png").convert()
    backButton.set_colorkey((255, 255, 255))

    backHoverButton = pygame.image.load("sprites/buttons/backHover.png").convert()
    backHoverButton.set_colorkey((255, 255, 255))

    controlsButton = pygame.image.load("sprites/buttons/controls.png").convert()
    controlsButton.set_colorkey((255, 255, 255))

    controlsHoverButton = pygame.image.load("sprites/buttons/controlsHover.png").convert()
    controlsHoverButton.set_colorkey((255, 255, 255))

    menuBackground = pygame.image.load("sprites/buttons/menuBackground.png").convert()
    winMenuBackground = pygame.image.load("sprites/buttons/WinningScreen.png").convert()


# import menu images
class MenuImages:
    aboutScreen = pygame.image.load("sprites/menu/aboutScreen.png").convert()
    aboutScreen.set_colorkey((255, 255, 255))

    controlsScreen = pygame.image.load("sprites/menu/controlsScreen.png").convert()
    controlsScreen.set_colorkey((255, 255, 255))


# function to load animations
def loadAnimation(fileName, directory, start, end):
    imageList = []  # list of images for animation
    for x in range(start, end + 1):  # for all images in animation
        # import and add image to list
        # loadNumberFormat formats 1 to 001 or 10 to 010
        imageList.append(pygame.image.load("%s/%s%s.png" % (directory, fileName, loadNumberFormat(x))))
    return imageList  # return list of animation


# Used to scale all images in a list
def scaleImages(imageList: list, scale):
    # inputs are the imageList and the scale ratio
    returnList = []  # list of scaled images
    for item in imageList:
        returnList.append(  # scale all images in the list and add them to the return list
            pygame.transform.smoothscale(item, (int(item.get_width() * scale), int(item.get_height() * scale))))
    return returnList  # return the list of scaled images


# Used to format the numbers for loading images
def loadNumberFormat(number: int):
    if number <= 9:  # if its 1 digit, return this type ( 1 -> 001 )
        return "00" + str(number)
    else:  # if more than 1 digits, return this type ( 10 -> 010 )
        return "0" + str(number)


# used to control enemies in all the levels
def controlEnemies(enemyList: list, platforms: list, character, bullets: list):
    enemyCount = 0  # enemy count, used to delete enemies
    for enemy in enemyList:
        if enemy.delete:  # if enemy is set for deletion
            del enemyList[enemyCount]  # delete enemy
        else:  # if not set for deletion
            if abs(enemy.xPos - character.xPos) < 1500:  # if enemy is within 1500 pixels of player
                enemy.control(platforms, bullets, character)  # control enemy
        enemyCount += 1  # add to enemy count


# used to display enemies in all the levels
def displayEnemies(enemyList: list, cameraX):
    for enemy in enemyList:
        # if the left most point or the right most point of the enemy is within the camera range
        if (cameraX <= enemy.xPos <= cameraX + 1000) or \
                (cameraX <= enemy.xPos + enemy.width <= cameraX + 1000):
            enemy.display()  # display the enemies


# used to control bullets in all the levels
def controlBullets(bullets: list, platforms: list):
    bulletCounter = 0  # used to delete bullets later
    for bullet in bullets:
        bullet.control(platforms)  # control bullets
        if bullet.destroy:
            del bullets[bulletCounter]  # if bullet is set for deletion, delete it from the list
        bulletCounter += 1  # add to the bullet counter


# used to display the bullets to the screen
def displayBullets(bullets: list, cameraX: int):
    for bullet in bullets:
        # if the left most point or the right most point of the bullet is within the camera range
        if (cameraX <= bullet.xPos <= cameraX + 1000) or \
                (cameraX <= bullet.xPos + bullet.width <= cameraX + 1000):
            bullet.display()  # display the bullet


# used to control pickups in all the levels
def controlPickups(pickupsList: list, platforms: list):
    pickupCount = 0  # used to delete pickups
    for pickup in pickupsList:
        if pickup.picked:  # if the pickup is already picked up
            del pickupsList[pickupCount]  # delete the pickup
        else:
            # if it isnt already picked up, then control the bullet
            pickup.control(platforms)
        pickupCount += 1


# used to display pickups to the screen
def displayPickups(pickupsList: list, cameraX):
    for pickup in pickupsList:
        # if the left most point or the right most point of the bullet is within the camera range
        if (cameraX <= pickup.xPos <= cameraX + 1000) or \
                (cameraX <= pickup.xPos + pickup.width <= cameraX + 1000):
            pickup.display()  # display the pickup


# display the pause screen in any level
def pauseScreen(screen: pygame.Surface, backgroundSurface: pygame.Surface, winScreen=False):
    # run pause screen while this is true
    runPause = True
    # Position the menu in the middle of the screen
    xPos = (screen.get_width() - 350) // 2
    yPos = (screen.get_height() - 400) // 2

    # The Rects for the buttons in the menu
    mainMenuRect = pygame.Rect(xPos + 75, yPos + 109, 200, 75)
    playAgainRect = pygame.Rect(xPos + 75, yPos + 218, 200, 75)

    # run menu while true
    while runPause:
        # Get the x and y position
        mx, my = pygame.mouse.get_pos()

        # indicates if mouse is over buttons
        hoveringPlayAgain = False
        hoveringMainMenu = False

        #Used to check for mouse clicks on buttons
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:  # for ball mouse clicks
                if playAgainRect.collidepoint(mx, my):  # if play again button is clicked on
                    return "playAgain"  # return playAgain to playagain
                elif mainMenuRect.collidepoint(mx, my):  # if main menu button is clicked on
                    return "mainMenu"  # return mainMenu
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "escape"  # return escape, this is handled outside this function

        # if hovering over playAgain, set it as true
        if playAgainRect.collidepoint(mx, my):
            hoveringPlayAgain = True
        # if hovering over mainMenu, set it as true
        if mainMenuRect.collidepoint(mx, my):
            hoveringMainMenu = True

        # blit the background surface that was inputted
        screen.blit(backgroundSurface, (0, 0))

        # if its the winning screen then blit the winning menu picture as the background of the menu
        # otherwise use the normal menu background
        if winScreen:
            screen.blit(ButtonsAndPause.winMenuBackground, (xPos, yPos))
        else:
            screen.blit(ButtonsAndPause.menuBackground, (xPos, yPos))

        # display hover button if hovering over main menu button
        # otherwise display the normal button
        if hoveringMainMenu:
            screen.blit(ButtonsAndPause.mainMenuHover, (xPos + 75, yPos + 109))
        else:
            screen.blit(ButtonsAndPause.mainMenu, (xPos + 75, yPos + 109))

        # display hover button if hovering over play again button
        # otherwise display the normal button
        if hoveringPlayAgain:
            screen.blit(ButtonsAndPause.playAgainHover, (xPos + 75, yPos + 218))
        else:
            screen.blit(ButtonsAndPause.playAgain, (xPos + 75, yPos + 218))

        # display the changes to the screen
        pygame.display.flip()


# Menu for the level end
def levelEndMenu(screen: pygame.Surface, backgroundSurface: pygame.Surface, level: int):
    # run menu if this is true
    runPause = True

    # Position to center menu on the screen
    xPos = (screen.get_width() - 350) // 2
    yPos = (screen.get_height() - 400) // 2

    # run the menu while true
    while runPause:
        # Get the rects to check button collision
        nextLevelRect = pygame.Rect(xPos + 75, yPos + 109, 200, 75)
        mainMenuRect = pygame.Rect(xPos + 75, yPos + 218, 200, 75)

        # Get the mouse position
        mx, my = pygame.mouse.get_pos()

        # used to indicate if player is hovering over buttons
        hoveringNextLevel = False
        hoveringMainMenu = False

        # used to check if player clicks on buttons
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if nextLevelRect.collidepoint(mx, my):  # check if the player clicked on the next level button
                    if level == 1:  # if the level is level 1
                        return "level2"  # return level 2
                    if level == 2:  # if the level is level 2
                        return "level3"  # reuturn level 3
                elif mainMenuRect.collidepoint(mx, my):  # check if main menu button clicked
                    return "mainMenu"  # return main menu
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:  # check if escape pressed
                    return "mainMenu"  # return main menu

        # check if hovering over next level button, and set variable true if hovering
        if nextLevelRect.collidepoint(mx, my):
            hoveringNextLevel = True

        # check if hovering over main menu button, and set variable true if hovering
        if mainMenuRect.collidepoint(mx, my):
            hoveringMainMenu = True

        # display the inputted background surface
        screen.blit(backgroundSurface, (0, 0))

        # display the menu background
        screen.blit(ButtonsAndPause.menuBackground, (xPos, yPos))

        # if hovering over next level button display hover image, otherwise display normal image
        if hoveringNextLevel:
            screen.blit(ButtonsAndPause.nextLevelHover, (xPos + 75, yPos + 109))
        else:
            screen.blit(ButtonsAndPause.nextLevel, (xPos + 75, yPos + 109))

        # if hovering over main menu button display hover image, otherwise display normal image
        if hoveringMainMenu:
            screen.blit(ButtonsAndPause.mainMenuHover, (xPos + 75, yPos + 218))
        else:
            screen.blit(ButtonsAndPause.mainMenu, (xPos + 75, yPos + 218))

        # display the changes to the screen
        pygame.display.flip()

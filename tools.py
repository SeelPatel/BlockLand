import pygame

pygame.display.init()
pygame.display.set_mode((0, 0))


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

    menuBackground = pygame.image.load("sprites/buttons/menuBackground.png").convert()
    winMenuBackground = pygame.image.load("sprites/buttons/WinningScreen.png").convert()

def loadAnimation(fileName, directory, start, end):
    imageList = []
    for x in range(start, end + 1):
        imageList.append(pygame.image.load("%s/%s%s.png" % (directory, fileName, loadNumberFormat(x))))
    return imageList


def scaleImages(imageList: list, scale):
    returnList = []
    for item in imageList:
        returnList.append(
            pygame.transform.smoothscale(item, (int(item.get_width() * scale), int(item.get_height() * scale))))
    return returnList

def loadNumberFormat(number: int):
    if number <= 9:
        return "00" + str(number)
    else:
        return "0" + str(number)


def controlEnemies(enemyList: list, platforms: list, character, bullets: list):
    enemyCount = 0
    for enemy in enemyList:
        if enemy.delete:
            del enemyList[enemyCount]
        else:
            if abs(enemy.xPos - character.xPos) < 1500:
                enemy.control(platforms, bullets, character)
        enemyCount += 1


def displayEnemies(enemyList: list, cameraX):
    for enemy in enemyList:
        if (cameraX <= enemy.xPos <= cameraX + 1000) or \
                (cameraX <= enemy.xPos + enemy.width <= cameraX + 1000):
            enemy.display()


def controlBullets(bullets: list, platforms: list):
    bulletCounter = 0
    for bullet in bullets:
        bullet.control(platforms)
        if bullet.destroy:
            del bullets[bulletCounter]
        bulletCounter += 1


def displayBullets(bullets: list, cameraX: int):
    for bullet in bullets:
        if (cameraX <= bullet.xPos <= cameraX + 1000) or \
                (cameraX <= bullet.xPos + bullet.width <= cameraX + 1000):
            bullet.display()


def controlPickups(pickupsList: list, platforms: list):
    pickupCount = 0
    for pickup in pickupsList:
        if pickup.picked:
            del pickupsList[pickupCount]
        else:
            pickup.control(platforms)
        pickupCount += 1


def displayPickups(pickupsList: list, cameraX):
    pickupCount = 0
    for pickup in pickupsList:
        if (cameraX <= pickup.xPos <= cameraX + 1000) or \
                (cameraX <= pickup.xPos + pickup.width <= cameraX + 1000):
            pickup.display()
        pickupCount += 1


def pauseScreen(screen: pygame.Surface, backgroundSurface: pygame.Surface, winScreen=False):
    runPause = True
    xPos = (screen.get_width() - 350) // 2
    yPos = (screen.get_height() - 400) // 2
    mainRect = pygame.Rect(xPos, yPos, 350, 400)
    mainMenuRect = pygame.Rect(xPos + 75, yPos + 109, 200, 75)
    playAgainRect = pygame.Rect(xPos + 75, yPos + 218, 200, 75)

    while runPause:
        mx, my = pygame.mouse.get_pos()

        hoveringPlayAgain = False
        hoveringMainMenu = False

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if playAgainRect.collidepoint(mx, my):
                    return "playAgain"
                elif mainMenuRect.collidepoint(mx, my):
                    return "mainMenu"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "escape"

        if playAgainRect.collidepoint(mx, my):
            hoveringPlayAgain = True

        if mainMenuRect.collidepoint(mx, my):
            hoveringMainMenu = True

        screen.blit(backgroundSurface, (0, 0))
        if winScreen:
            screen.blit(ButtonsAndPause.winMenuBackground, (xPos, yPos))
        else:
            screen.blit(ButtonsAndPause.menuBackground, (xPos, yPos))

        if hoveringMainMenu:
            screen.blit(ButtonsAndPause.mainMenuHover, (xPos + 75, yPos + 109))
        else:
            screen.blit(ButtonsAndPause.mainMenu, (xPos + 75, yPos + 109))

        if hoveringPlayAgain:
            screen.blit(ButtonsAndPause.playAgainHover, (xPos + 75, yPos + 218))
        else:
            screen.blit(ButtonsAndPause.playAgain, (xPos + 75, yPos + 218))

        pygame.display.flip()


def levelEndMenu(screen: pygame.Surface, backgroundSurface: pygame.Surface, level: int):
    runPause = True
    xPos = (screen.get_width() - 350) // 2
    yPos = (screen.get_height() - 400) // 2
    while runPause:
        mainRect = pygame.Rect(xPos, yPos, 350, 400)
        nextLevelRect = pygame.Rect(xPos + 75, yPos + 109, 200, 75)
        mainMenuRect = pygame.Rect(xPos + 75, yPos + 218, 200, 75)
        mx, my = pygame.mouse.get_pos()

        hoveringNextLevel = False
        hoveringMainMenu = False

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if nextLevelRect.collidepoint(mx, my):
                    if level == 1:
                        return "level2"
                    if level == 2:
                        return "level3"
                elif mainMenuRect.collidepoint(mx, my):
                    return "mainMenu"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "mainMenu"

        if nextLevelRect.collidepoint(mx, my):
            hoveringNextLevel = True

        if mainMenuRect.collidepoint(mx, my):
            hoveringMainMenu = True

        screen.blit(backgroundSurface, (0, 0))
        screen.blit(ButtonsAndPause.menuBackground, (xPos, yPos))

        if hoveringNextLevel:
            screen.blit(ButtonsAndPause.nextLevelHover, (xPos + 75, yPos + 109))
        else:
            screen.blit(ButtonsAndPause.nextLevel, (xPos + 75, yPos + 109))

        if hoveringMainMenu:
            screen.blit(ButtonsAndPause.mainMenuHover, (xPos + 75, yPos + 218))
        else:
            screen.blit(ButtonsAndPause.mainMenu, (xPos + 75, yPos + 218))

        pygame.display.flip()

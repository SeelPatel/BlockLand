import pygame

import Character
import Constants


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


def controlEnemies(enemyList: list, platforms: list, character: Character, bullets: list):
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


def pauseScreen(screen: pygame.Surface, backgroundSurface: pygame.Surface):
    runPause = True
    xPos = (screen.get_width() - 350) // 2
    yPos = (screen.get_height() - 400) // 2
    while runPause:
        mainRect = pygame.Rect(xPos, yPos, 350, 400)
        playAgainRect = pygame.Rect(xPos + 75, yPos + 109, 200, 75)
        mainMenuRect = pygame.Rect(xPos + 35, yPos + 218, 200, 75)
        mx, my = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if playAgainRect.collidepoint(mx, my):
                    runPause = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    runPause = False

        screen.blit(Constants.Images.ButtonsAndPause.mainMenu, (mainRect[0], mainMenuRect[1]))

        screen.blit(backgroundSurface, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), mainRect, 0)
        pygame.display.flip()

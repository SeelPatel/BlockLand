import pygame
import Character

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

from pygame import *

import Constants
import RunLevel1
import RunLevel2
import tools

screenDim = screenWidth, screenHeight = (1000, 700)

screen = display.set_mode(screenDim)
screen.set_alpha(None)

backXPos = 0

"""
Speedup powerup
main menu
levels
maybe boss
"""

longBackground = image.load("sprites/longBackground.png").convert()


def mainMenu(screen: Surface, backX, background: Surface):
    BG = background
    backXPos = backX

    buttonX = (1000 - 200) // 2

    playGameRect = Rect(buttonX, 300, 200, 75)
    aboutRect = Rect(buttonX, 400, 200, 75)
    runMenu = True
    while runMenu:
        mx, my = mouse.get_pos()
        playGameHover = False
        aboutHover = False

        backXPos += 0.3

        if backXPos >= 2000:
            backXPos = 0

        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if playGameRect.collidepoint(mx, my):
                    return "levelChooser"
                elif aboutRect.collidepoint(mx, my):
                    return "about"
            if e.type == QUIT:
                return "endGame"
        screen.blit(BG.subsurface([int(backXPos), 0, 1000, 700]), (0, 0))

        screen.blit(Constants.Images.Logos.mainLogo, (225, 0))
        if playGameRect.collidepoint(mx, my):
            playGameHover = True
            screen.blit(tools.ButtonsAndPause.playGameHover, (buttonX, 300))
        else:
            screen.blit(tools.ButtonsAndPause.playGame, (buttonX, 300))

        if aboutRect.collidepoint(mx, my):
            aboutHover = True
            screen.blit(tools.ButtonsAndPause.aboutGameHover, (buttonX, 400))
        else:
            screen.blit(tools.ButtonsAndPause.aboutGame, (buttonX, 400))

        display.flip()


def levelChooser(screen: Surface, backX, background: Surface):
    BG = background
    backXPos = backX

    buttonY = (700 - 159) // 2

    level1Rect = Rect(225, buttonY, 150, 150)
    level2Rect = Rect(425, buttonY, 150, 150)
    level3Rect = Rect(625, buttonY, 150, 150)

    backButtonRect = Rect(400, buttonY + 300, 200, 75)

    runMenu = True
    while runMenu:
        mx, my = mouse.get_pos()
        backXPos += 0.3

        if backXPos >= 2000:
            backXPos = 0

        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if level1Rect.collidepoint(mx, my):
                    return "level1"
                elif level2Rect.collidepoint(mx, my):
                    return "level2"
                elif level3Rect.collidepoint(mx, my):
                    return "level3"
                elif backButtonRect.collidepoint(mx, my):
                    return "mainMenu"

        screen.blit(BG.subsurface([int(backXPos), 0, 1000, 700]), (0, 0))
        screen.blit(Constants.Images.Logos.mainLogo, (225, 0))

        if level1Rect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.level1Hover, (225, buttonY))
        else:
            screen.blit(tools.ButtonsAndPause.level1, (225, buttonY))

        if level2Rect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.level2Hover, (425, buttonY))
        else:
            screen.blit(tools.ButtonsAndPause.level2, (425, buttonY))

        if level3Rect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.level3Hover, (625, buttonY))
        else:
            screen.blit(tools.ButtonsAndPause.level3, (625, buttonY))

        if backButtonRect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.backHoverButton, (400, buttonY + 300))
        else:
            screen.blit(tools.ButtonsAndPause.backButton, (400, buttonY + 300))

        display.flip()


runningGame = True

levelAnswer = mainMenu(screen, backXPos, longBackground)
while runningGame:
    if levelAnswer == "endGame":
        runningGame = False
    elif levelAnswer == "mainMenu":
        levelAnswer = mainMenu(screen, backXPos, longBackground)
    elif levelAnswer == "levelChooser":
        levelAnswer = levelChooser(screen, backXPos, longBackground)
    elif levelAnswer == "level1":
        levelAnswer = RunLevel1.start(screen)
    elif levelAnswer == "level2":
        levelAnswer = RunLevel2.start(screen)

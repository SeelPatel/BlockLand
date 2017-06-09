from pygame import *

import RunLevel1
import RunLevel2

screenDim = screenWidth, screenHeight = (1000, 700)

screen = display.set_mode(screenDim)
screen.set_alpha(None)

"""
Speedup powerup
main menu
bullet powerup
pause screen
levels
maybe boss
"""
def pauseScreen(screen: Surface, backgroundSurface: Surface):
    runPause = True
    while runPause:
        pauseBox = Rect(450, 200, 100, 300)
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if pauseBox.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]) and mouse.get_pressed()[0] == 1:
                    runPause = False
            if e.type == KEYDOWN:
                if e.key == K_c:
                    runPause = False
                    return "level1"
        screen.blit(backgroundSurface, (0, 0))
        draw.rect(screen, (255, 255, 255), pauseBox, 0)
        display.flip()


runningGame = True
run1 = RunLevel1.start(screen)

while runningGame:
    if run1 == "levelBeat":
        RunLevel2.start(screen)
    else:
        pause = pauseScreen(screen,screen)
        if pause=="level1":
            RunLevel2.start(screen)

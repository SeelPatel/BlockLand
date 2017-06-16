# Main file for the project
# This is where the game is run from

# Imports

import os

from pygame import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center game window on screen

# Display loading screen. Game could take 10-30 seconds to load
# This is because all levels are loaded before the game starts
# This ensures the game feels fast when the user is playing it
intro = image.load("sprites/blockLandIntro.png")  # get image
screen = display.set_mode((500, 375), NOFRAME)  # Set screen
screen.blit(intro, (0, 0))  # display intro image
display.flip()  # display to display

# Play the background music while loading and continue throughout game
mixer.init()  # Initialize the music system
mixer.music.load("backgroundMusic.mp3")  # Select/load music file
mixer.music.set_volume(0.3)  # Set the volume of the music
mixer.music.play(-1)  # Set the music on an unlimited loop

# IMPORTS
import Constants
import RunLevel1
import RunLevel2
import RunLevel3
import tools

# Create screen with with size 1000,700
# This is the screen size throughout the whole game
screenDim = screenWidth, screenHeight = (1000, 700)
screen = display.set_mode(screenDim)

backXPos = 0  # X Position for moving background in the menu screen

# Background picture for moving background on menu screen
longBackground = image.load("sprites/longBackground.png").convert()

# Display the controls to the user
def controlsScreen(screen: Surface, backX, background: Surface):
    # Screen is the surface to display the menu on
    BG = background  # Surface to scroll through for the background
    backXPos = backX  # X Position of background scrolling

    buttonY = 600  # Preset button Y Position on screen

    # Rects to check collision for buttons
    backButtonRect = Rect(400, buttonY, 200, 75)

    # Run menu while true
    runMenu = True
    while runMenu:
        # Get mouse position
        mx, my = mouse.get_pos()

        # Add to scrolling position for background
        backXPos += 0.3

        # If scrolling goes over 2000, restart it
        if backXPos >= 2000:
            backXPos = 0

        # Check if the player clicks on buttons
        # Returns where to go in game based on user input
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if backButtonRect.collidepoint(mx, my):
                    return "mainMenu"

        # Display the scrolling background
        screen.blit(BG.subsurface([int(backXPos), 0, 1000, 700]), (0, 0))
        # Display the about screen
        screen.blit(tools.MenuImages.controlsScreen, (0, 0))

        # Change button images if hovered over, to indicate user input
        if backButtonRect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.backHoverButton, (400, buttonY))
        else:
            screen.blit(tools.ButtonsAndPause.backButton, (400, buttonY))

        # Display to screen
        display.flip()


# Function to display main menu screen
def mainMenu(screen: Surface, backX, background: Surface):
    # Screen is the surface to display the menu on
    BG = background  # Surface to scroll through for the background
    backXPos = backX  # X Position of background scrolling

    buttonX = (1000 - 200) // 2  # Centered X Position for 200px buttons

    # Rects to check collision for buttons
    playGameRect = Rect(buttonX, 300, 200, 75)  # Rect for PlayGame Button
    aboutRect = Rect(buttonX, 400, 200, 75)  # Rect for About Button
    controlsRect = Rect(buttonX, 500, 200, 75)

    # Run menu while true
    runMenu = True
    while runMenu:
        # Get mouse position
        mx, my = mouse.get_pos()
        # Add to scrolling position for background
        backXPos += 0.3

        # If scrolling goes over 2000, restart it
        if backXPos >= 2000:
            backXPos = 0

        # Check if the player clicks on buttons
        # Returns where to go in game based on user input
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if playGameRect.collidepoint(mx, my):
                    return "levelChooser"  # Go to level chooser
                elif aboutRect.collidepoint(mx, my):
                    return "about"  # Go to about screen
                elif controlsRect.collidepoint(mx, my):
                    return "controls"
            if e.type == QUIT:
                return "endGame"  # End the game

        # Blit the background surface based on scroll position
        screen.blit(BG.subsurface([int(backXPos), 0, 1000, 700]), (0, 0))
        screen.blit(Constants.Images.Logos.mainLogo, (225, 0))  # Display the game logo

        # Change button images if hovered over, to indicate user input
        if playGameRect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.playGameHover, (buttonX, 300))
        else:
            screen.blit(tools.ButtonsAndPause.playGame, (buttonX, 300))

        if aboutRect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.aboutGameHover, (buttonX, 400))
        else:
            screen.blit(tools.ButtonsAndPause.aboutGame, (buttonX, 400))

        if controlsRect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.controlsHoverButton, (buttonX, 500))
        else:
            screen.blit(tools.ButtonsAndPause.controlsButton, (buttonX, 500))

        # Put everything on the display
        display.flip()


# Function to display information about the game
def aboutScreen(screen: Surface, backX, background: Surface):
    # Screen is the surface to display the menu on
    BG = background  # Surface to scroll through for the background
    backXPos = backX  # X Position of background scrolling

    buttonY = 600  # Preset button Y Position on screen

    # Rects to check collision for buttons
    backButtonRect = Rect(400, buttonY, 200, 75)

    # Run menu while true
    runMenu = True
    while runMenu:
        # Get mouse position
        mx, my = mouse.get_pos()

        # Add to scrolling position for background
        backXPos += 0.3

        # If scrolling goes over 2000, restart it
        if backXPos >= 2000:
            backXPos = 0

        # Check if the player clicks on buttons
        # Returns where to go in game based on user input
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if backButtonRect.collidepoint(mx, my):
                    return "mainMenu"

        # Display the scrolling background
        screen.blit(BG.subsurface([int(backXPos), 0, 1000, 700]), (0, 0))
        # Display the about screen
        screen.blit(tools.MenuImages.aboutScreen, (0, 0))

        # Change button images if hovered over, to indicate user input
        if backButtonRect.collidepoint(mx, my):
            screen.blit(tools.ButtonsAndPause.backHoverButton, (400, buttonY))
        else:
            screen.blit(tools.ButtonsAndPause.backButton, (400, buttonY))

        # Display to screen
        display.flip()


# Function to allow user to pick level
def levelChooser(screen: Surface, backX, background: Surface):
    # Screen is the surface to display the menu on
    BG = background  # Surface to scroll through for the background
    backXPos = backX  # X Position of background scrolling

    buttonY = (700 - 159) // 2  # Preset button Y Position on screen

    # Rects to check collision for buttons
    level1Rect = Rect(225, buttonY, 150, 150)
    level2Rect = Rect(425, buttonY, 150, 150)
    level3Rect = Rect(625, buttonY, 150, 150)
    backButtonRect = Rect(400, buttonY + 300, 200, 75)

    # Run menu while true
    runMenu = True
    while runMenu:
        # Get mouse position
        mx, my = mouse.get_pos()

        # Add to scrolling position for background
        backXPos += 0.3

        # If scrolling goes over 2000, restart it
        if backXPos >= 2000:
            backXPos = 0

        # Check if the player clicks on buttons
        # Returns where to go in game based on user input
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

        # Display the scrolling background
        screen.blit(BG.subsurface([int(backXPos), 0, 1000, 700]), (0, 0))
        # Display the game logo
        screen.blit(Constants.Images.Logos.mainLogo, (225, 0))

        # Change button images if hovered over, to indicate user input
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

        # Display to screen
        display.flip()


# Run game while true
runningGame = True

# Run main menu and to indicate where player wants to go at beginning
levelAnswer = mainMenu(screen, backXPos, longBackground)
while runningGame:
    if levelAnswer == "endGame":  # Quit game
        runningGame = False
    elif levelAnswer == "mainMenu":  # Run the main menu
        levelAnswer = mainMenu(screen, backXPos, longBackground)
    elif levelAnswer == "levelChooser":  # Run the level chooser
        levelAnswer = levelChooser(screen, backXPos, longBackground)
    elif levelAnswer == "about":  # run the about screen for info
        levelAnswer = aboutScreen(screen, backXPos, longBackground)
    elif levelAnswer == "controls":
        levelAnswer = controlsScreen(screen, backXPos, longBackground)
    elif levelAnswer == "level1":  # run level 1
        levelAnswer = RunLevel1.start(screen)
    elif levelAnswer == "level2":  # run level 2
        levelAnswer = RunLevel2.start(screen)
    elif levelAnswer == "level3":  # run level 3
        levelAnswer = RunLevel3.start(screen)
exit()  # exit the program

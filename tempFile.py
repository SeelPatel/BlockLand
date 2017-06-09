# from pygame import *
#
# import Background
# import Character
# import Constants
#
# class Level:
#
#     # gameSurface = Surface((15000, 5000), DOUBLEBUF)
#     # gameSurface.set_alpha(None)
#
#     # platformSurface = Surface((15000, 5000), SRCALPHA)
#
#
#     def pauseScreen(self,screen: Surface, backgroundSurface: Surface):
#         runPause = True
#         while runPause:
#             pauseBox = Rect(450, 200, 100, 300)
#             for e in event.get():
#                 if e.type == MOUSEBUTTONDOWN:
#                     if pauseBox.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]) and mouse.get_pressed()[0] == 1:
#                         runPause = False
#                 if e.type == KEYDOWN:
#                     if e.key == K_c:
#                         runPause = False
#             screen.blit(backgroundSurface, (0, 0))
#             draw.rect(screen, (255, 255, 255), pauseBox, 0)
#             display.flip()
#
#
#     event.set_allowed(KEYDOWN | QUIT)  # Allows for more efficiant events
#
#     def controlEnemies(self,enemyList: list, platforms: list, character: Character, bullets: list):
#         enemyCount = 0
#         for enemy in enemyList:
#             if enemy.dead:
#                 del enemyList[enemyCount]
#             else:
#                 if abs(enemy.xPos - character.xPos) < 1500:
#                     enemy.control(platforms, bullets, character)
#             enemyCount += 1
#
#
#     def displayEnemies(self,enemyList: list, cameraX):
#         for enemy in enemyList:
#             if (cameraX <= enemy.xPos <= cameraX + 1000) or \
#                     (cameraX <= enemy.xPos + enemy.width <= cameraX + 1000):
#                 enemy.display()
#
#
#     def controlBullets(self,bullets: list, platforms: list):
#         bulletCounter = 0
#         for bullet in bullets:
#             bullet.control(platforms)
#             if bullet.destroy:
#                 del bullets[bulletCounter]
#             bulletCounter += 1
#
#
#     def displayBullets(self,bullets: list, cameraX: int):
#         for bullet in bullets:
#             if (cameraX <= bullet.xPos <= cameraX + 1000) or \
#                     (cameraX <= bullet.xPos + bullet.width <= cameraX + 1000):
#                 bullet.display()
#
#
#     def controlPickups(self,pickupsList: list, platforms: list):
#         pickupCount = 0
#         for pickup in pickupsList:
#             if pickup.picked:
#                 del pickupsList[pickupCount]
#             else:
#                 pickup.control(platforms)
#             pickupCount += 1
#
#
#     def displayPickups(self,pickupsList: list, cameraX):
#         pickupCount = 0
#         for pickup in pickupsList:
#             if (cameraX <= pickup.xPos <= cameraX + 1000) or \
#                     (cameraX <= pickup.xPos + pickup.width <= cameraX + 1000):
#                 pickup.display()
#             pickupCount += 1
#
#
#     def level1(self,screen):
#         self.gameSurface.fill((255,255,255))
#
#         character = Character.Character(self.gameSurface, startPos=(1050, 2200), width=43, height=68)
#         mainClock = time.Clock()
#
#         cameraX = character.xPos - 500
#         cameraY = character.yPos - 400
#
#         backgroundMain = Background.Background(self.gameSurface, character, cameraX, cameraY)
#
#         Constants.Levels.Level1(self.gameSurface)
#
#         platforms = Constants.Levels.Level1.platforms
#         enemyList = Constants.Levels.Level1.enemies
#         pickupsList = []
#         bullets = []
#
#         done = False
#         fpsCount = 0
#         fpsTotal = 0
#
#         self.platformSurface.fill((0,0,0,0))
#
#         """
#         Generated a Surface for all unmoving platforms
#         It is faster to blit subsurfaces from this rather then
#         blit surfaces in view during every iteraton
#         """
#         for platform in platforms:
#             platform.display(surface=self.platformSurface)
#
#         while not done:
#             #Set camera position
#             cameraX = character.xPos - 500
#             cameraY = character.yPos - 400
#
#             #Get events, passed to character class later
#             events = event.get()
#             for e in events:
#                 if e.type == QUIT: # Quit the level
#                     done = True
#                 if e.type == KEYDOWN:
#                     if e.key == K_ESCAPE: # Open a pause menu
#                         self.pauseScreen(screen, screen)
#
#             #Send inputs from user to character for control
#             character.playerControl(events, bullets)
#
#             #Control character actions and movements
#             character.moveCharacter(platforms, enemyList, pickupsList, bullets)
#
#             #End game if character dies
#             if character.dead:
#                 done = True
#
#             #Control all game objects
#             self.controlEnemies(enemyList, platforms, character, bullets)
#             self.controlBullets(bullets, platforms)
#             self.controlPickups(pickupsList, platforms)
#
#             #Control and display background
#             backgroundMain.control(cameraX, cameraY)
#             backgroundMain.display()
#
#             #Display platforms via generated surface
#             self.gameSurface.blit(self.platformSurface.subsurface(Rect(cameraX, cameraY, 1000, 700)), (cameraX, cameraY))
#
#             # Display all game objects
#             character.display()
#             self.displayEnemies(enemyList, cameraX)
#             self.displayBullets(bullets, cameraX)
#             self.displayPickups(pickupsList, cameraX)
#
#             #Get subsurface to display
#             camera = self.gameSurface.subsurface(Rect(cameraX, cameraY, 1000, 700))
#
#             #Display game screen
#             screen.blit(camera, (0, 0))
#
#             #display GUI
#             character.displayHealth(screen)
#
#             mainClock.tick(60) # Set Frame Cap to 60
#             fps = mainClock.get_fps() # Get FPS
#
#             display.flip() # Update the display
#
#             #Calculate average fps
#             fpsCount += 1
#             fpsTotal += fps
#             averageFps = fpsTotal / fpsCount
#
#             # print("average fps: ", str(averageFps))
#             print(fps)

#1. import pygame files
import pygame
from pygame.locals import * #no need to type pygame.sth every time
import get_words
import random

# Functions
def drawChar(letter, centerX, centerY):
    fontObj = pygame.font.Font('freesansbold.ttf', 44)
    textSurfaceObj = fontObj.render(letter, True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (centerX, centerY)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def printPopup(string, centerX, centerY):
    popupFontObj = pygame.font.Font('freesansbold.ttf', 28)
    textSurfaceObj = popupFontObj.render(string, True, BLACK, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (centerX, centerY)
    bgRect = pygame.Rect.inflate(textRectObj, 30, 30)
    pygame.draw.rect(DISPLAYSURF, WHITE, bgRect, 0, 15)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    return bgRect

#global variable declarations
windowWidth = 600
windowHeight = 900
gridSize = 80
padding = 10
timer = None
window = None
fps = 30
wordList = get_words.get_words()
alphabet = range(pygame.K_a,pygame.K_z+1)

#background colour
bgColour = pygame.Color(255,255,255)

#2. initialize the window
pygame.init() #must write this before using any pygame fucntions
timer = pygame.time.Clock() #this is a variable
DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight), 0, 32) #set the size of the window
pygame.display.set_caption("Wordy")

# set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (84,141,78)
BLUE = ( 0, 0, 255)
GRAY = (127,127,127)
YELLOW = (181,159,58)
DARKGRAY = (57,58,60)

#3. set up the basic game loop
done = False
while done == False:
    #reset variables
    charTyped = 0
    attempt = list()
    numAttempts = 0
    checkAns = False
    delay = fps
    popup = False

    #set the backgorund colour and draw the grids
    DISPLAYSURF.fill(BLACK)
    grids = list()
    for i in range(6):
        gridRows = list()
        for j in range(5):
            gridRows.append(pygame.Rect(gridSize*(j+1) + padding*j,gridSize*(i+1) + padding*i,gridSize,gridSize))
            pygame.draw.rect(DISPLAYSURF, GRAY, gridRows[j] , width=1)
        grids.append(gridRows)

    #select word
    ans = wordList[random.randint(1,len(wordList))]

    gameOver = False
    endScreen = False
    while gameOver == False:
        #contents of the game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                gameOver = True
                done = True
            if not endScreen and event.type == pygame.KEYDOWN:
                # print characters when user typed less than 5 letters
                if charTyped < 5:
                    for letter in alphabet:
                        if event.key == letter:
                            gridCenterX = gridSize*(charTyped+1) + padding*charTyped + gridSize//2
                            drawChar(chr(letter).upper(),grids[numAttempts][charTyped].centerx,grids[numAttempts][charTyped].centery+3)
                            attempt.append(chr(letter))
                            charTyped += 1
                # delete characters
                if charTyped > 0 and event.key == pygame.K_BACKSPACE:
                    eraseRect = pygame.Rect.copy(grids[numAttempts][charTyped-1])
                    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect.inflate(eraseRect, -padding, -padding))
                    attempt.pop()
                    charTyped -= 1
                # check answer when user press enter
                if charTyped == 5 and event.key == pygame.K_RETURN:
                    checkAns = True
            # only check enter key when in endscreen
            if endScreen and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    endScreen = False
                    gameOver = True

        if checkAns:
            attemptStr = "".join(attempt)
            ansList = list(ans)
            checkAns = False
            # print a disappearing popup if the attempted word is not in word list
            if attemptStr not in wordList:
                popup = True
                delay = fps
            else: # check answer and change the colour of characters
                for i in range(5):
                    if attempt[i] == ansList[i]:
                        #turn green
                        pygame.draw.rect(DISPLAYSURF, GREEN, grids[numAttempts][i])
                        drawChar(attempt[i].upper(),grids[numAttempts][i].centerx,grids[numAttempts][i].centery+3)
                        ansList[i] = ""
                        attempt[i] = "1"
                for i in range(5):
                    if attempt[i] in ansList:
                        #turn yellow
                        pygame.draw.rect(DISPLAYSURF, YELLOW, grids[numAttempts][i])
                        drawChar(attempt[i].upper(),grids[numAttempts][i].centerx,grids[numAttempts][i].centery+3)
                        ansList[ansList.index(attempt[i])] = ""
                        attempt[i] = "1"
                for i in range(5):
                    if attempt[i] != "1":
                        #turn dark gray
                        pygame.draw.rect(DISPLAYSURF, DARKGRAY, grids[numAttempts][i])
                        drawChar(attempt[i].upper(),grids[numAttempts][i].centerx,grids[numAttempts][i].centery+3)
                if attemptStr == ans:
                    # win game
                    printPopup("You win!", windowWidth//2, 40)
                    printPopup("Press enter for new game", windowWidth//2, (gridSize+padding)*7+40)
                    endScreen = True
                else: # incorrect attempt
                    numAttempts += 1
                    attempt = list()
                    charTyped = 0
                    if numAttempts == 6:
                        printPopup(ans, windowWidth//2, 40)
                        printPopup("Press enter for new game", windowWidth//2, (gridSize+padding)*7+40)
                        endScreen = True

        #draw popup onto the screen
        if popup:
            if delay == fps:
                popupRect = printPopup("Not in word list", windowWidth//2, 40)
            delay -= 1
            if delay == 0:
                pygame.draw.rect(DISPLAYSURF, BLACK, popupRect)
                popup = False
            

        #update the screen
        pygame.display.update()
        timer.tick(fps)
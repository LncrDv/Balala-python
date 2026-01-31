import pygame as pg
from ui import ShowUI
import jokerManager, deckManager, handManager, selectionManager
mouseButtonDown = False

def GetEvents():
    global mouseButtonDown
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseButtonDown = True
        else :
            mouseButtonDown = False

#10.66 jokers at 2.5x scale fit in the screen
jokerManager.generateRandomJokers(5)
deckManager.create52CardDeck()
handManager.DrawHand()


running = True
while running:
    GetEvents()
    ShowUI()
    selectionManager.CardSelectLogic(mouseButtonDown)
    

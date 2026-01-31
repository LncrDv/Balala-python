import pygame as pg
from ui import ShowUI
import jokerManager, deckManager

def GetEvents():

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
#10.66 jokers at 2.5x scale fit in the screen
jokerManager.generateRandomJokers(5)
deckManager.create52CardDeck()

running = True
while running:
    GetEvents()
    ShowUI()

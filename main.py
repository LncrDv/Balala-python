import pygame as pg
from ui import showUI
import gameManager

def getEvents():

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()


running = True
while running:
    getEvents()
    showUI()

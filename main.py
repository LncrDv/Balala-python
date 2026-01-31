import pygame as pg
from ui import ShowUI
import jokerManager

def GetEvents():

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()


running = True
while running:
    GetEvents()
    ShowUI()

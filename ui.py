import pygame as pg
from jokers import *
import gameManager

#Default lines to show a window with pygame
pg.init()

#Resizable window logic
window = pg.display.set_mode((1280, 720), pg.RESIZABLE)
screen = pg.Surface((1920,1080))
clock = pg.time.Clock()

def scale_surface(surface, window_size):
    win_w, win_h = window_size
    surf_w, surf_h = surface.get_size()

    scale = min(win_w / surf_w, win_h / surf_h)

    scaled_w = int(surf_w * scale)
    scaled_h = int(surf_h * scale)

    scaled_surface = pg.transform.smoothscale(
        surface, (scaled_w, scaled_h)
    )

    x = (win_w - scaled_w) // 2
    y = (win_h - scaled_h) // 2

    return scaled_surface, (x, y)

JOKER_ATLAS_IMAGE = pg.image.load("resources/textures/Jokers.png")

class SpriteAtlas:
    def __init__(self, surface, tile_w, tile_h):
        self.surface = surface
        self.tile_w = tile_w
        self.tile_h = tile_h

    def get(self, x, y):
        rect = pg.Rect(
            x * self.tile_w,
            y * self.tile_h,
            self.tile_w,
            self.tile_h
        )
        return self.surface.subsurface(rect)
JOKER_W = 71
JOKER_H = 95
JOKER_SCALE = 2.5
JOKER_ATLAS = SpriteAtlas(JOKER_ATLAS_IMAGE, JOKER_W, JOKER_H)


def centerObjects(objectIndex, numberOfObjects, objectWidth, padding, screenWidth):
    return (screenWidth - (numberOfObjects*objectWidth + (numberOfObjects-1)*padding)) / 2 + objectIndex*(objectWidth + padding)

def drawJoker(joker : Joker, slot):
    #set the image to corresponding atlas coords
    image_joker = JOKER_ATLAS.get(joker.textureCoords[0], joker.textureCoords[1])
    #scale it 
    image_joker = pg.transform.smoothscale_by(image_joker, JOKER_SCALE)

    #display it centered to the screen
    screen.blit(image_joker, (centerObjects(slot, len(gameManager.equippedJokers), JOKER_W*JOKER_SCALE, 5, screen.get_width()), 0))
    

    

def drawJokers():
    for i in range(len(gameManager.equippedJokers)):
        joker = gameManager.equippedJokers[i]
        drawJoker(joker, i)


def drawToInternalScreen():
    #Draw to internal screen
    screen.fill((27,112,50))
    drawJokers()
def showUI():
    drawToInternalScreen()

    #-- Scale to window --
    window.fill((0, 0, 0))  # black bars
    scaled, pos = scale_surface(screen, window.get_size())
    window.blit(scaled, pos)

    pg.display.flip()
    clock.tick(60)
import pygame as pg
from cards import Card
def GetCardsValue(cards : list[Card]):
    values = []
    for card in cards:
        values.append(card.value)
    return values
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

def CenterObject(objectIndex, numberOfObjects, objectWidth, padding, screenWidth, areaWidth):
    # Total width using desired padding
    totalWidth = numberOfObjects * objectWidth + (numberOfObjects - 1) * padding

    #If overflow, decrease padding
    if totalWidth > areaWidth and numberOfObjects > 1:
        padding = (areaWidth - numberOfObjects * objectWidth) / (numberOfObjects - 1)
        totalWidth = numberOfObjects * objectWidth + (numberOfObjects - 1) * padding

    #Center cards on screen
    startX = (screenWidth - totalWidth) / 2

    return startX + objectIndex * (objectWidth + padding)

def CalculatePadding(numberOfObjects, objectWidth, padding, areaWidth):

    totalWidth = numberOfObjects * objectWidth + (numberOfObjects - 1) * padding

    if totalWidth > areaWidth and numberOfObjects > 1:
        padding = (areaWidth - numberOfObjects * objectWidth) / (numberOfObjects - 1)

    return padding

def EmptyImage(width, height):
    surf = pg.Surface((width, height), pg.SRCALPHA)
    surf.fill((0,0,0,0))
    return surf
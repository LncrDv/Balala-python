import pygame as pg
from cards import Card
import timeManager
def GetCardsValue(cards : list[Card]):
    values = []
    for card in cards:
        values.append(card.value)
    return values
def WindowToScreenPos(mousePos, screen, window):
    scaled, pos = scale_surface(screen, window.get_size())
    render_offset = pos
    render_scale = scaled.get_width() / screen.get_width()

    mouseX, mouseY = mousePos
    offsetX, offsetY = render_offset

    scaledX = (mouseX - offsetX) / render_scale
    scaledY = (mouseY - offsetY) / render_scale

    return scaledX, scaledY
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

def CenterObject(
    objectIndex,
    numberOfObjects,
    objectWidth,
    padding,
    leftX,
    rightX,
    maxPadding=True
):
    areaWidth = rightX - leftX

    if numberOfObjects > 1:
        # Padding that maximizes spacing while staying in bounds
        maxPossiblePadding = (areaWidth - numberOfObjects * objectWidth) / (numberOfObjects - 1)

        if not maxPadding:
            # Use user padding ONLY if it fits
            totalWidth = numberOfObjects * objectWidth + (numberOfObjects - 1) * padding
            if totalWidth <= areaWidth:
                finalPadding = padding
            else:
                finalPadding = maxPossiblePadding
        else:
            finalPadding = maxPossiblePadding
    else:
        finalPadding = 0

    totalWidth = numberOfObjects * objectWidth + (numberOfObjects - 1) * finalPadding

    # Center within bounds
    startX = leftX + (areaWidth - totalWidth) / 2

    return startX + objectIndex * (objectWidth + finalPadding)


def CalculatePadding(numberOfObjects, objectWidth, padding, areaWidth):

    totalWidth = numberOfObjects * objectWidth + (numberOfObjects - 1) * padding

    if totalWidth > areaWidth and numberOfObjects > 1:
        padding = (areaWidth - numberOfObjects * objectWidth) / (numberOfObjects - 1)

    return padding

def EmptyImage(width, height):
    surf = pg.Surface((width, height), pg.SRCALPHA)
    surf.fill((0,0,0,0))
    return surf


class WaitForSeconds:
    def __init__(self, duration):
        self.duration = duration
        self.elapsed = 0
        self.finished = False

    def update(self, deltaTime):
        if self.finished:
            return True

        self.elapsed += deltaTime
        if self.elapsed >= self.duration:
            self.finished = True
            return True

        return False
  
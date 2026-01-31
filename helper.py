import pygame as pg

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

def centerObject(objectIndex, numberOfObjects, objectWidth, padding, screenWidth):
    return (screenWidth - (numberOfObjects*objectWidth + (numberOfObjects-1)*padding)) / 2 + objectIndex*(objectWidth + padding)

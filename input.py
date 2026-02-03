import pygame as pg

spaceBar = False
lmb = False
rmb = False
def GetEvents():
    global spaceBar
    global lmb, rmb
    spaceBar = False
    lmb = rmb = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            spaceBar = True

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                lmb = True
            else:
                lmb = False
            
            if event.button == 3:
                rmb = True
            else:
                rmb = False

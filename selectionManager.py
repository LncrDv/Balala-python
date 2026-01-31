import ui, pygame

def CardSelectLogic(mouseButton):

    mousePos = pygame.mouse.get_pos()
    scaleX = ui.screen.get_size()[0]/ui.DEFAULT_SCREEN_SIZE_X
    scaleY = ui.screen.get_size()[1]/ui.DEFAULT_SCREEN_SIZE_Y
    
    mousePos = (mousePos[0] / scaleX, mousePos[1] / scaleY)

    
    for cardRect in ui.cardRects:
        if mouseButton:
            if cardRect[0].collidepoint(mousePos):
                print("On card !")
            else:
                print(mousePos)
        
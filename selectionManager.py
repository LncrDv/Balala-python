import ui, pygame, handManager
mousePressed = False

selectedCards = []
def WindowToScreenPos(mousePos):
        mx, my = mousePos
        ox, oy = ui.render_offset

        sx = (mx - ox) / ui.render_scale
        sy = (my - oy) / ui.render_scale

        return sx, sy
def GetEvents():
    global mousePressed
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousePressed = True
        else :
            mousePressed = False

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def OnCardSelection(slot):
    if slot in selectedCards:
        ui.DeselectCard(slot)
        selectedCards.pop(selectedCards.index(slot))
    else:
        ui.SelectCard(slot)
        selectedCards.append(slot)
def CardSelectLogic():
    global mousePressed
    GetEvents()

    if mousePressed:
        mousePos = pygame.mouse.get_pos()
        mouseScreenPos = WindowToScreenPos(mousePos)
        for cardRect in reversed(ui.cardSelectionRect):
            if cardRect.collidepoint(mouseScreenPos):
                print(f"On card ! : {handManager.currentHand[ui.cardSelectionRect.index(cardRect)].name}")
                OnCardSelection(ui.cardSelectionRect.index(cardRect))
                break
            #else:
                #print(f"Boowomp : {handManager.currentHand[i].name}")
        
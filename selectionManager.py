import ui, pygame, handManager

selectedCards = []
CARD_SELECTION_LIMIT = 5

def WindowToScreenPos(mousePos):
        mouseX, mouseY = mousePos
        offsetX, offsetY = ui.render_offset

        scaledX = (mouseX - offsetX) / ui.render_scale
        scaledY = (mouseY - offsetY) / ui.render_scale

        return scaledX, scaledY
def SelectCard(_slot):
    ui.SelectCard(_slot)
    selectedCards.append(_slot)

def DeselectCard(_slot):
    ui.DeselectCard(_slot)
    selectedCards.pop(selectedCards.index(_slot))

def OnCardSelection(slot):
    global selectedCards

    if slot in selectedCards:
        #Deselect a card bc already selected
        DeselectCard(slot)
    else:
        #Failsafe to prevent over-selecting
        if len(selectedCards) >= CARD_SELECTION_LIMIT:
            return
        #Select a card bc not already selected
        SelectCard(slot)

def CardSelectLogic():
    global selectedCards
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #Mouse left click pressed yippee

                mousePos = pygame.mouse.get_pos()
                mouseScreenPos = WindowToScreenPos(mousePos)

                for cardRect in reversed(ui.cardSelectionRect):

                    if cardRect.collidepoint(mouseScreenPos):

                        #print(f"On card ! : {handManager.currentHand[ui.cardSelectionRect.index(cardRect)].name}")
                        OnCardSelection(ui.cardSelectionRect.index(cardRect))

                        break
                    #else:
                        #print(f"Boowomp : {handManager.currentHand[i].name}")
            elif event.button == 3:
                for _ in range(len(selectedCards)):
                    #Discard at index 0 bc else index error
                    DeselectCard(selectedCards[0])

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        
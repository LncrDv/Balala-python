import ui, pygame, handManager, input
from cards import Card

selectedCards = []
CARD_SELECTION_LIMIT = 5

def WindowToScreenPos(mousePos):
        mouseX, mouseY = mousePos
        offsetX, offsetY = ui.render_offset

        scaledX = (mouseX - offsetX) / ui.render_scale
        scaledY = (mouseY - offsetY) / ui.render_scale

        return scaledX, scaledY
def SelectCard(_card : Card):
    ui.SelectCard(_card)
    selectedCards.append(_card)
    

def DeselectCard(_card : Card):
    try:
        ui.DeselectCard(_card)
        selectedCards.remove(_card)
    except ValueError:
        print(_card.name," is not selected")

def DeselectAllCards():
    for _ in range(len(selectedCards)):
        #Discard at index 0 bc else index error
        DeselectCard(selectedCards[0])

def OnCardSelection(_card : Card):
    global selectedCardsIndexes

    if _card in selectedCards:
        #Deselect a card bc already selected
        DeselectCard(_card)
    else:
        #Failsafe to prevent over-selecting
        if len(selectedCards) >= CARD_SELECTION_LIMIT:
            return
        #Select a card bc not already selected
        SelectCard(_card)

def CardSelectLogic():
    if input.lmb:
        mousePos = pygame.mouse.get_pos()
        mouseScreenPos = WindowToScreenPos(mousePos)

        for cardRect in reversed(ui.cardSelectionRect):

            if cardRect.collidepoint(mouseScreenPos):

                #print(f"On card ! : {handManager.currentHand[ui.cardSelectionRect.index(cardRect)].name}")
                OnCardSelection(handManager.currentHand[ui.cardSelectionRect.index(cardRect)])

                break
            #else:
                #print(f"Boowomp : {handManager.currentHand[i].name}")
    elif input.rmb:
        DeselectAllCards()

        
import ui, pygame, handManager, input, handTypesManager
from cards import Card
import helper

selectedCards = []
CARD_SELECTION_LIMIT = 5

currentHand_handTypes = None
currentHand_bestHandType = None

def SelectCard(_card : Card):
    slot = handManager.currentHand.index(_card)
    ui.SelectCard(slot)
    selectedCards.append(_card)
    
def DeselectCard(_card : Card):
    try:
        slot = handManager.currentHand.index(_card)
        ui.DeselectCard(slot)
        selectedCards.remove(_card)
    except ValueError:
        print(_card.name, "is not selected")


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
    global currentHand_bestHandType, currentHand_handTypes
    #Mouse inputs
    if input.lmb:
        mousePos = pygame.mouse.get_pos()
        mouseScreenPos = helper.WindowToScreenPos(mousePos, ui.screen, ui.window)

        for cardRect in reversed(ui.cardSelectionRect):

            if cardRect.collidepoint(mouseScreenPos):

                #print(f"On card ! : {handManager.currentHand[ui.cardSelectionRect.index(cardRect)].name}")
                OnCardSelection(handManager.currentHand[ui.cardSelectionRect.index(cardRect)])

                break
            #else:
                #print(f"Boowomp : {handManager.currentHand[i].name}")
    elif input.rmb:
        DeselectAllCards()

    #Hand score
    #Determine hand types in hand
    currentHand_handTypes = handTypesManager.DetermineHandTypes(selectedCards, CARD_SELECTION_LIMIT)
    #Determine best hand type from hand types
    currentHand_bestHandType = handTypesManager.DetermineBestHandType(currentHand_handTypes)
    #print(f'''Best hand type : {currentHand_bestHandType} with value {handTypesManager.handTypes[currentHand_bestHandType]["default"]["chips"]} chips and {handTypesManager.handTypes[currentHand_bestHandType]["default"]["mult"]} mult''')

        
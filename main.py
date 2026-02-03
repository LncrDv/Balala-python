from ui import ShowUI
import jokerManager, deckManager, handManager, selectionManager, roundManager, input

#10.66 jokers at 2.5x scale fit in the screen
jokerManager.generateRandomJokers(5)
deckManager.create52CardDeck()
handManager.DrawFullHand()


running = True
while running:
    input.GetEvents()
    ShowUI(roundManager.inRound)
    selectionManager.CardSelectLogic()
    roundManager.RoundLoop()

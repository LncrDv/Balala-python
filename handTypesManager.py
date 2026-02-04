from collections import Counter
import deckManager
handTypes = {
    None:{"default":{"chips":0,"mult":1}},
    "High Card":{"default":{"chips":5,"mult":1}},
    "Pair":{"default":{"chips":10,"mult":2}},
    "Two Pair":{"default":{"chips":20,"mult":2}},
    "Three Of A Kind":{"default":{"chips":30,"mult":3}},
    "Straight":{"default":{"chips":30,"mult":4}},
    "Flush":{"default":{"chips":35,"mult":4}},
    "Full House":{"default":{"chips":40,"mult":4}},
    "Four Of A Kind":{"default":{"chips":60,"mult":7}},
    "Straight Flush":{"default":{"chips":100,"mult":8}},
}

levelUpHandTypes = {
    "High Card":{"chips":10,"mult":1},
    "Pair":{"chips":15,"mult":2},
    "Two Pair":{"chips":20,"mult":1},
    "Three Of A Kind":{"chips":20,"mult":2},
    "Straight":{"chips":30,"mult":3},
    "Flush":{"chips":15,"mult":2},
    "Full House":{"chips":25,"mult":2},
    "Four Of A Kind":{"chips":30,"mult":3},
    "Straight Flush":{"chips":40 ,"mult":4},
}

def DetermineHandTypes(cards, maxSelectionSize):

    if len(cards) == 0:
        return
    thisHandTypes = ["High Card"]

    #Check for hands of multiple times the same card
    cardsValues = [card.value for card in cards]
    cardsSuits = [card.suit for card in cards]
    
    frequencyOfSameSymbol = Counter(cardsValues)

    if 2 in frequencyOfSameSymbol.values():
        thisHandTypes.append("Pair")
    elif 3 in frequencyOfSameSymbol.values():
        thisHandTypes.append("Three Of A Kind")
    elif 4 in frequencyOfSameSymbol.values():
        thisHandTypes.append("Four Of A Kind")
    elif 5 in frequencyOfSameSymbol.values():
        #thisHandTypes.append("Five Of A Kind")
        pass
    
    #Check for pair+pair and pair+3oak
    
    freq = sorted(frequencyOfSameSymbol.values(), reverse=True)
    if freq == [2,2,1] or freq == [2,2]:
        thisHandTypes.append("Two Pair")
    if freq == [3,2]:
        thisHandTypes.append("Full House")
    
    #Si la main (sans les duplications) ne vaut pas 1 (donc pas le mm symbole) alors demi tour
    if len(set(cardsSuits)) == 1 and len(cardsSuits) == maxSelectionSize:
        #Check for flush
        if all(suit == cardsSuits[0] for suit in cardsSuits):
            thisHandTypes.append("Flush")
    

    #Check for straight
    valueToRank = {v: i for i, v in enumerate(deckManager.cardValues, start=2)}     #Convertir une valeur en index
    ranks = sorted(valueToRank[card.value] for card in cards)

    #Si la main c'est [10,10,J,Q,K], elle sera interprétée comme [10,J,Q,K]. Dcp c un failsafe
    if len(set(ranks)) == len(ranks) and len(ranks) == maxSelectionSize:
        if ranks == list(range(ranks[0], ranks[0] + len(ranks))):
            thisHandTypes.append("Straight")

        elif ranks == [2,3,4,5,14]:         #5,4,3,2,A, dans l'ordre croissant
            thisHandTypes.append("Straight")
    
    #Check for complex hands
    if "Straight" in thisHandTypes and "Flush" in thisHandTypes:
        thisHandTypes.append("Straight Flush")
    return thisHandTypes

def DetermineBestHandType(_handTypes):
    global handTypes
    if _handTypes is None:
        return
    bestHandType = "High Card"

    handTypesNames = list(handTypes.keys())
    for handType in _handTypes:
        if not handType in handTypesNames:
            #Error ! Hand type doesn't exist !
            print(f'''Error ! Hand type '{handType}' doesn't exist !''')
        else:
            if handTypesNames.index(handType) >= handTypesNames.index(bestHandType):
                bestHandType = handType
    
    return bestHandType



class PlanetCard:
    name : str
    handType : str | list[str]
    levelAugAmount : int
    mostPlayed : bool
    handLevel : int

    def __init__(self, _name = "Pluto", _handType = "High Card", _levelAugAmount = 1):
        self.name = _name
        self.handType = _handType
        self.levelAugAmount = _levelAugAmount
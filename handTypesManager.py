from collections import Counter
handTypes = {
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

def DetermineHandType(cards):
    cardsValues = [card.value for card in cards]
    thisHandTypes = ["High Card"]
    counts = Counter(cardsValues)
    
    #Check for hands of multiple times the same card
    if 2 in counts.values():
        thisHandTypes.append("Pair")
    elif 3 in counts.values():
        thisHandTypes.append("Three Of A Kind")
    elif 4 in counts.values():
        thisHandTypes.append("Four Of A Kind")
    elif 5 in counts.values():
        #thisHandTypes.append("Five Of A Kind")
        pass
    
    


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
class Joker:
    name : str

    modifiers : dict

    def __init__(self, _name : str, _modifiers : dict):
        self.name = _name
        self.modifiers = _modifiers
    
    def describe(self):
        print(f"Name : {self.name}\nModifiers : {self.modifiers}")

#Example of a Joker
#joker_jimbo = Joker("Jimbo",{"plusMult" : 4})
#joker_jimbo.describe()


#Creating all the jokers
collection_jokers = {
    "joker_grosMichel" : Joker("Gros Michel",{"plusMult" : 15,"extinctionProba" : 1/6}),
    "joker_jimbo" : Joker("Jimbo",{"plusMult" : 4}),
    "joker_juggler" : Joker("Juggler",{"plusHandSize" : 1}),
    "joker_drunkard" : Joker("Drunkard",{"plusDiscard" : 1})
}

#TEST FUNC : DEBUG ALL JOKERS
for joker in collection_jokers.values():
    joker.describe()
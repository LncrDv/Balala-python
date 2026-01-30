class Joker:
    name : str
    textureCoords : tuple
    modifiers : dict

    def __init__(self, _name : str, _textureCoords, _modifiers : dict):
        self.name = _name
        self.textureCoords = _textureCoords
        self.modifiers = _modifiers
    
    def describe(self):
        print(f"Name : {self.name}\nTexture Coords : {self.textureCoords}\nModifiers : {self.modifiers}\n-\n")

#Example of a Joker
#joker_jimbo = Joker("Jimbo",(0,0),{"plusMult" : 4})
#joker_jimbo.describe()


#Creating all the jokers
collection_jokers = {
    "joker_grosMichel" : Joker(
        "Gros Michel",
        (7,6),
        {"plusMult" : 15,"extinctionProba" : 1/6}
        ),

    "joker_jimbo" : Joker(
        "Jimbo",
        (0,0),
        {"plusMult" : 4}
        ),

    "joker_juggler" : Joker(
        "Juggler",
        (0,1),
        {"plusHandSize" : 1}
        ),

    "joker_drunkard" : Joker(
        "Drunkard",
        (1,1),
        {"plusDiscard" : 1}
        ),
    
    "joker_blueprint" : Joker(
        "Blueprint",
        (0,3),
        {"compatible" : False, "copyingJoker" : None}
    ),

    "joker_chaos" : Joker(
        "Chaos The Clown",
        (1,0),
        {"plusFreeRerolls":1,"isActive":False}
    )
}

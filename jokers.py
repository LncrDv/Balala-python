import pygame as pg
JOKER_ATLAS_IMAGE = pg.image.load("resources/textures/Jokers.png")

class SpriteAtlas:
    def __init__(self, surface, tile_w, tile_h):
        self.surface = surface
        self.tile_w = tile_w
        self.tile_h = tile_h

    def get(self, x, y):
        rect = pg.Rect(
            x * self.tile_w,
            y * self.tile_h,
            self.tile_w,
            self.tile_h
        )
        return self.surface.subsurface(rect)
JOKER_W = 71
JOKER_H = 95
JOKER_SCALE = 2.5
JOKER_ATLAS = SpriteAtlas(JOKER_ATLAS_IMAGE, JOKER_W, JOKER_H)

class Joker:
    name : str
    textureCoords : tuple
    modifiers : dict

    def __init__(self, _name : str, _textureCoords, _modifiers : dict):
        self.name = _name
        self.textureCoords = _textureCoords
        self.modifiers = {
            "active":False,
            "debuffed":False
            }
        self.modifiers.update(_modifiers)
    
    def describe(self):
        print
        (
            "\nName : ",self.name,
            "\nTexture Coords : ",self.textureCoords,
            "\nModifiers : ",self.modifiers
        )

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

    # "joker_juggler" : Joker(
    #     "Juggler",
    #     (0,1),
    #     {"plusHandSize" : 1}
    #     ),

    # "joker_drunkard" : Joker(
    #     "Drunkard",
    #     (1,1),
    #     {"plusDiscard" : 1}
    #     ),
    
#    "joker_blueprint" : Joker(
#        "Blueprint",
#        (0,3),
#        {"compatible" : False, "copyingJoker" : None}
#    ),

#    "joker_chaos" : Joker(
#        "Chaos The Clown",
#        (1,0),
#        {"plusFreeRerolls":1,"isActive":False}
#    ),
    "joker_droll": Joker(
        "Droll Joker",
        (6,0),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Flush"},"plusMult":10}
    )

}

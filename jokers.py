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

    "joker_sly":Joker(
        "Sly Joker",
        (0,14),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Pair"},"plusChips":50}
    ),
    "joker_wily":Joker(
        "Wily Joker",
        (1,14),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Three Of A Kind"},"plusChips":100}
    ),
    "joker_clever":Joker(
        "Clever Joker",
        (2,14),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Two Pair"},"plusChips":80}
    ),
    "joker_devious":Joker(
        "Devious Joker",
        (3,14),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Straight"},"plusChips":100}
    ),
    "joker_crafty":Joker(
        "Crafty Joker",
        (4,14),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Flush"},"plusChips":80}
    ),
    "joker_jolly":Joker(
        "Jolly Joker",
        (2,0),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Pair"},"plusMult":8}
    ),
    "joker_zany":Joker(
        "Zany Joker",
        (3,0),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Three Of A Kind"},"plusMult":12}
    ),
    "joker_mad":Joker(
        "Mad Joker",
        (4,0),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Two Pair"},"plusMult":10}
    ),
    "joker_crazy":Joker(
        "Crazy Joker",
        (5,0),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Straight"},"plusMult":12}
    ),
    "joker_droll": Joker(
        "Droll Joker",
        (6,0),
        {"conditionnal":{"fulfilled":False,"requireHandOfType":"Flush"},"plusMult":10}
    ),
    "joker_greedy": Joker(
        "Greedy Joker",
        (6,1),
        {"conditionnal":{"conditionAffectDomain":"plusMult","fulfilled":False,"requireCardOfSuit":"Diamonds","increment":3}, "plusMult":0}
    ),
    "joker_lusty": Joker(
        "Lusty Joker",
        (7,1),
        {"conditionnal":{"conditionAffectDomain":"plusMult","fulfilled":False,"requireCardOfSuit":"Hearts","increment":3}, "plusMult":0}
    ),
    "joker_wrathful": Joker(
        "Wrathful Joker",
        (8,1),
        {"conditionnal":{"conditionAffectDomain":"plusMult","fulfilled":False,"requireCardOfSuit":"Spades","increment":3}, "plusMult":0}
    ),
    "joker_gluttonous": Joker(
        "Gluttonous Joker",
        (9,1),
        {"conditionnal":{"conditionAffectDomain":"plusMult","fulfilled":False,"requireCardOfSuit":"Clubs","increment":3}, "plusMult":0}
    ),

}

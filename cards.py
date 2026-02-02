import pygame as pg
CARD_ATLAS_IMAGE = pg.image.load("resources/textures/8BitDeck.png")
CARD_BG_IMAGE = pg.image.load("resources/textures/Enhancers.png")

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
CARD_W = 71
CARD_H = 95
CARD_SCALE = 2.5

CARD_ATLAS = SpriteAtlas(CARD_ATLAS_IMAGE, CARD_W, CARD_H)
CARD_BG_ATLAS =SpriteAtlas(CARD_BG_IMAGE, CARD_W, CARD_H)

ENHANCEMENT_TO_ATLASCOORDS = {
    "None":(1,0),
    "FaceDown":(0,0),
    "Stone":(5,0),
    "Gold":(6,0),
    "Chips":(1,1),
    "Mult":(2,1),
    "Wild":(3,1),
    "Lucky":(4,1),
    "Glass":(5,1),
    "Steel":(6,1)
}
SEAL_TO_ATLASCOORDS = {
    "None":None,
    "GoldSeal":(2,0),
    "PurpleSeal":(4,4),
    "RedSeal":(5,4),
    "BlueSeal":(6,4)
}
ENHANCEMENT_OVERLAYS = ["Stone","FaceDown"]
ENHANCEMENT_NO_SEAL = ["FaceDown"]

def ValueAndSuitToAtlasCoords(value, suit):
    valueToAtlas = 0
    suitToAtlas = 0
    match value:
        case "2":
            valueToAtlas = 0
        case "3":
            valueToAtlas = 1
        case "4":
            valueToAtlas = 2
        case "5":
            valueToAtlas = 3
        case "6":
            valueToAtlas = 4
        case "7":
            valueToAtlas = 5
        case "8":
            valueToAtlas = 6
        case "9":
            valueToAtlas = 7
        case "10":
            valueToAtlas = 8
        case "Jack":
            valueToAtlas = 9
        case "Queen":
            valueToAtlas = 10
        case "King":
            valueToAtlas = 11
        case "Ace":
            valueToAtlas = 12
        case __:
            valueToAtlas = 0
    match suit:
        case "Hearts":
            suitToAtlas = 0
        case "Clubs":
            suitToAtlas = 1
        case "Diamonds":
            suitToAtlas = 2
        case "Spades":
            suitToAtlas = 3
        case __:
            suitToAtlas = 0

    return (valueToAtlas, suitToAtlas)


class Card:
    value : str
    suit : str | list
    edition : str
    enhancement : str
    seal : str
    #sticker : str
    debuffed : bool
    chips : int
    mult : int

    @property
    def name(self) -> str:
        return (f"{self.value} of {self.suit}")
    



    def __init__(self, _value, _suit, _edition, _enhancement, _seal, _sticker, _debuffed, _chips, _mult):
        self.value = _value
        self.suit = _suit
        self.edition = _edition
        self.enhancement = _enhancement
        self.seal = _seal
        #self.sticker = _sticker
        self.debuffed = _debuffed

        self.chips = _chips
        self.mult = _mult

    def describe(self):
        print(
            "\nName : ",self.name,
            "\nEdition : ",self.edition,
            "\nEnhancement : ",self.enhancement,
            "\nSeal : ",self.seal,
            #"\nSticker : ",self.sticker,
            "\nDebuffed : ",self.debuffed,
            "\nChips : ",self.chips,
            "\nMult : ",self.mult
            )
        
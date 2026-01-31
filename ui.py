import pygame as pg
from jokers import *
from cards import *
from helper import *
import jokerManager, deckManager, handManager

#Default lines to show a window with pygame
pg.init()

#Resizable window logic
DEFAULT_WINDOW_SIZE_X = 1280
DEFAULT_WINDOW_SIZE_Y = 720

DEFAULT_SCREEN_SIZE_X = 1920
DEFAULT_SCREEN_SIZE_Y = 1080

window = pg.display.set_mode((DEFAULT_WINDOW_SIZE_X, DEFAULT_WINDOW_SIZE_Y), pg.RESIZABLE)
screen = pg.Surface((DEFAULT_SCREEN_SIZE_X,DEFAULT_SCREEN_SIZE_Y))
clock = pg.time.Clock()

scaleX = screen.get_size()[0]/DEFAULT_WINDOW_SIZE_X
scaleY = screen.get_size()[1]/DEFAULT_WINDOW_SIZE_Y

JOKER_AREA_X = 1000
CARD_AREA_X = 1500
CARD_AREA_POS_Y = 800

cardRects = []

def DrawCard(card : Card, slot):
    #set the image to corresponding atlas coords
    cardTexCoords = ValueAndSuitToAtlasCoords(card.value, card.suit)

    #Enhancement in background first
    if not card.enhancement in ENHANCEMENT_OVERLAYS:
        #Check if card enhancement is not considered an overlay
        image_enh_bg_card = CARD_BG_ATLAS.get(*ENHANCEMENT_TO_ATLASCOORDS[card.enhancement])
    else:
        image_enh_bg_card = EmptyImage(CARD_W, CARD_H)

    #Then number
    image_card = CARD_ATLAS.get(*cardTexCoords)

    #Then enhancement in overlay
    if card.enhancement in ENHANCEMENT_OVERLAYS:
        image_enh_over_card = CARD_BG_ATLAS.get(*ENHANCEMENT_TO_ATLASCOORDS[card.enhancement])
    else:
        image_enh_over_card = EmptyImage(CARD_W, CARD_H)
    #Then edition

    #Then seal
    if (card.seal is not "None") and (not card.enhancement in ENHANCEMENT_NO_SEAL):
        image_card_seal = CARD_BG_ATLAS.get(*SEAL_TO_ATLASCOORDS[card.seal])
    else:
        image_card_seal = EmptyImage(CARD_W, CARD_H)

    #Then debuff if needed
    if card.debuffed:
        image_card_debuff = CARD_BG_ATLAS.get(7,0)
    else:
        image_card_debuff = EmptyImage(CARD_W, CARD_H)


    #scale it 
    image_enh_bg_card = pg.transform.smoothscale_by(image_enh_bg_card, CARD_SCALE)
    image_card = pg.transform.smoothscale_by(image_card, CARD_SCALE)
    image_enh_over_card = pg.transform.smoothscale_by(image_enh_over_card, CARD_SCALE)
    image_card_seal = pg.transform.smoothscale_by(image_card_seal, CARD_SCALE)
    image_card_debuff = pg.transform.smoothscale_by(image_card_debuff, CARD_SCALE)

    #show images
    cardRect = []
    cardRect.append(screen.blit(image_enh_bg_card, (CenterObject(slot, handManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width(), CARD_AREA_X), CARD_AREA_POS_Y)))
    cardRect.append(screen.blit(image_card, (CenterObject(slot, handManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width(), CARD_AREA_X), CARD_AREA_POS_Y)))
    cardRect.append(screen.blit(image_enh_over_card, (CenterObject(slot, handManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width(), CARD_AREA_X), CARD_AREA_POS_Y)))
    cardRect.append(screen.blit(image_card_seal, (CenterObject(slot, handManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width(), CARD_AREA_X), CARD_AREA_POS_Y)))
    cardRect.append(screen.blit(image_card_debuff, (CenterObject(slot, handManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width(), CARD_AREA_X), CARD_AREA_POS_Y)))

    global cardRects
    cardRects.append(cardRect)
def DrawHand(_handSize):
    for i in range(_handSize):
        DrawCard(handManager.currentHand[i], i)
    

def DrawJoker(joker : Joker, slot):
    #set the image to corresponding atlas coords
    image_joker = JOKER_ATLAS.get(joker.textureCoords[0], joker.textureCoords[1])
    #scale it 
    image_joker = pg.transform.smoothscale_by(image_joker, JOKER_SCALE)

    #display it centered to the screen
    screen.blit(image_joker, (CenterObject(slot, len(jokerManager.equippedJokers), JOKER_W*JOKER_SCALE, 5, screen.get_width(), JOKER_AREA_X), 0))
def DrawJokers():
    for i in range(len(jokerManager.equippedJokers)):
        joker = jokerManager.equippedJokers[i]
        DrawJoker(joker, i)


def DrawToInternalScreen():
    #Draw to internal screen
    screen.fill((27,112,50))
    DrawJokers()
    DrawHand(handManager.handSize)
def ShowUI():
    DrawToInternalScreen()

    #-- Scale to window --
    window.fill((0, 0, 0))  # black bars
    scaled, pos = scale_surface(screen, window.get_size())
    window.blit(scaled, pos)

    pg.display.flip()
    clock.tick(60)
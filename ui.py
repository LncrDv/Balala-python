import pygame as pg
from jokers import *
from cards import *
from helper import *
import jokerManager, deckManager

#Default lines to show a window with pygame
pg.init()

#Resizable window logic
window = pg.display.set_mode((1280, 720), pg.RESIZABLE)
screen = pg.Surface((1920,1080))
clock = pg.time.Clock()

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
    screen.blit(image_enh_bg_card, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    screen.blit(image_card, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    screen.blit(image_enh_over_card, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    screen.blit(image_card_seal, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    screen.blit(image_card_debuff, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    
def DrawHand(_handSize):
    for i in range(_handSize):
        DrawCard(deckManager.full_deck[i], i)
    

def DrawJoker(joker : Joker, slot):
    #set the image to corresponding atlas coords
    image_joker = JOKER_ATLAS.get(joker.textureCoords[0], joker.textureCoords[1])
    #scale it 
    image_joker = pg.transform.smoothscale_by(image_joker, JOKER_SCALE)

    #display it centered to the screen
    screen.blit(image_joker, (centerObject(slot, len(jokerManager.equippedJokers), JOKER_W*JOKER_SCALE, 5, screen.get_width()), 0))
def DrawJokers():
    for i in range(len(jokerManager.equippedJokers)):
        joker = jokerManager.equippedJokers[i]
        DrawJoker(joker, i)


def DrawToInternalScreen():
    #Draw to internal screen
    screen.fill((27,112,50))
    DrawJokers()
    DrawHand(deckManager.handSize)
def ShowUI():
    DrawToInternalScreen()

    #-- Scale to window --
    window.fill((0, 0, 0))  # black bars
    scaled, pos = scale_surface(screen, window.get_size())
    window.blit(scaled, pos)

    pg.display.flip()
    clock.tick(60)
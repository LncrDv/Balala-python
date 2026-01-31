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
    card_tex_coords = valueAndSuitToAtlasCoords(card.value, card.suit)
    image_bg_card = CARD_BG_ATLAS.get(*ENHANCEMENT_TO_ATLASCOORDS[card.enhancement]) #Bg first
    image_card = CARD_ATLAS.get(*card_tex_coords)   #Then number
    #Then enhancement
    #Then edition
    #Then debuff if needed
    
    #scale it 
    image_bg_card = pg.transform.smoothscale_by(image_bg_card, CARD_SCALE)
    image_card = pg.transform.smoothscale_by(image_card, CARD_SCALE)

    screen.blit(image_bg_card, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    screen.blit(image_card, (centerObject(slot, deckManager.handSize, CARD_W*CARD_SCALE, 5, screen.get_width()), 800))
    
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
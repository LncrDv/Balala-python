import pygame as pg
from jokers import *
from cards import *
from helper import *
import jokerManager, deckManager, handManager, selectionManager

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



#region CardsDrawing
CARD_AREA_X = 1500
CARD_AREA_DEFAULT_POS_Y = 800
CARD_SELECT_OFFSET = -100

cardSelectionRect : list[pg.Rect]
cardSelectionRect = []

allCardsRects : list[list[pg.Rect]]
allCardsRects = []

cardYOffset = [0 for _ in range(handManager.handSize)]

def CreateCardRects(_slot, *layers):
    global cardYOffset

    thisCardRects = []
    for layer in layers:
        thisCardRects.append(
        screen.blit
        (
            layer,
            (
                CenterObject
                (
                    _slot,
                    handManager.handSize,
                    CARD_W*CARD_SCALE,
                    5,
                    screen.get_width(),
                    CARD_AREA_X
                ),
                CARD_AREA_DEFAULT_POS_Y + cardYOffset[_slot]
            )
        )
    )
    
    return thisCardRects

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
    thisCardRects = CreateCardRects(slot, image_enh_bg_card, image_card, image_enh_over_card, image_card_seal, image_card_debuff)
    
    global allCardsRects
    allCardsRects.append(thisCardRects)

    global cardSelectionRect
    cardSelectionRect.append(thisCardRects[0])

def SelectCard(slot):
    cardYOffset[slot] = CARD_SELECT_OFFSET

def DeselectCard(slot):
    cardYOffset[slot] = 0

def DrawHand(_handSize):
    global cardSelectionRect
    cardSelectionRect = []
    for i in range(_handSize):
        DrawCard(handManager.currentHand[i], i)
    
#endregion
#region Jokers
JOKER_AREA_X = 1000

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
#endregion
#region Score Display
SCORE_CHIPS_TEXT_SIZE = 50
SCORE_CHIPS_TEXT_POS = (100, 540+SCORE_CHIPS_TEXT_SIZE)
def CalculateChips():
    chipsScore = 0
    for selectedCardIndex in selectionManager.selectedCards:
        selectedCard = handManager.currentHand[selectedCardIndex]
        chipsScore += selectedCard.chips
    return chipsScore
def DrawChipsDisplay():
    papyrusFontChips = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_CHIPS_TEXT_SIZE)
    chipsText = papyrusFontChips.render(f"Chips : {CalculateChips()}", True, (255,255,255), (0,0,128))
    screen.blit(chipsText, SCORE_CHIPS_TEXT_POS)

SCORE_MULT_TEXT_SIZE = 50
SCORE_MULT_TEXT_POS = (100, 540-SCORE_MULT_TEXT_SIZE)
def CalculateMult():
    multScore = 1
    for selectedCardIndex in selectionManager.selectedCards:
        selectedCard = handManager.currentHand[selectedCardIndex]
        multScore += selectedCard.mult
    return multScore
def DrawMultDisplay():
    papyrusFontMult = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_MULT_TEXT_SIZE)
    multText = papyrusFontMult.render(f"Mult : {CalculateMult()}", True, (255,255,255), (128,0,0))
    screen.blit(multText, SCORE_MULT_TEXT_POS)

SCORE_HAND_DISPLAY_TEXT_SIZE = 50
SCORE_HAND_DISPLAY_TEXT_POS = (100, 540-SCORE_HAND_DISPLAY_TEXT_SIZE*3)
def CalculateHandScore():
    handScore = 0
    handScore = CalculateChips() * CalculateMult()
    return handScore
def DrawHandScoreDisplay():
    papyrusFontHandScore = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_HAND_DISPLAY_TEXT_SIZE)
    handScoreText = papyrusFontHandScore.render(f"Hand Score : {CalculateHandScore()}", True, (255,255,255), (0,0,0))
    screen.blit(handScoreText, SCORE_HAND_DISPLAY_TEXT_POS)


#endregion
def DrawToInternalScreen():
    #Draw to internal screen
    #Black borders
    screen.fill((27,112,50))
    #Draw cards
    DrawJokers()
    DrawHand(handManager.handSize)
    #Score
    DrawChipsDisplay()
    DrawMultDisplay()
    DrawHandScoreDisplay()
def ShowUI():
    global render_scale, render_offset

    DrawToInternalScreen()

    window.fill((0, 0, 0))
    scaled, pos = scale_surface(screen, window.get_size())

    render_offset = pos
    render_scale = scaled.get_width() / screen.get_width()

    window.blit(scaled, pos)
    pg.display.flip()
    clock.tick(60)

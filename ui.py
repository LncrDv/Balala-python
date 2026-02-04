import pygame as pg
from jokers import *
from cards import *
from helper import *
import jokerManager, deckManager, handManager, selectionManager, roundManager, input
import ui_state

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
CARD_AREA_DEFAULT_POS_Y = 700
CARD_SELECT_OFFSET = -100

cardSelectionRect : list[pg.Rect]
cardSelectionRect = []

allCardsRects : list[list[pg.Rect]]
allCardsRects = []

playButtonRect = None
discardButtonRect = None
cardYOffset = [0 for _ in range(handManager.currentHandSize)]

pressedPlayHand = False
pressedDiscardHand = False

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
                    handManager.currentHandSize,
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

def SelectCard(slot: int):
    cardYOffset[slot] = CARD_SELECT_OFFSET

def DeselectCard(slot: int):
    cardYOffset[slot] = 0


def DrawHand():
    global cardSelectionRect
    global cardYOffset
    cardSelectionRect = []
    for i in range(len(handManager.currentHand)):
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
def DrawChipsDisplay():
    papyrusFontChips = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_CHIPS_TEXT_SIZE)

    chips = roundManager.CalculateChips(selectionManager.currentHand_bestHandType)[0]
    addedChips = roundManager.CalculateChips(selectionManager.currentHand_bestHandType)[1]

    if addedChips == 0:
        chipsText = papyrusFontChips.render(f"Chips : {chips}", True, (255,255,255), (0,0,128))
    else:
        chipsText = papyrusFontChips.render(f"Chips : {chips} + {addedChips}", True, (255,255,255), (0,0,128))

    screen.blit(chipsText, SCORE_CHIPS_TEXT_POS)

SCORE_MULT_TEXT_SIZE = 50
SCORE_MULT_TEXT_POS = (100, 540-SCORE_MULT_TEXT_SIZE)
def DrawMultDisplay():
    papyrusFontMult = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_MULT_TEXT_SIZE)

    mult = roundManager.CalculateMult(selectionManager.currentHand_bestHandType)[0]
    addedMult = roundManager.CalculateMult(selectionManager.currentHand_bestHandType)[1]

    if addedMult == 0:
        multText = papyrusFontMult.render(f"Mult : {mult}", True, (255,255,255), (128,0,0))
    else:
        multText = papyrusFontMult.render(f"Mult : {mult} + {addedMult}", True, (255,255,255), (128,0,0))
    

    screen.blit(multText, SCORE_MULT_TEXT_POS)

SCORE_HAND_DISPLAY_TEXT_SIZE = 50
SCORE_HAND_DISPLAY_TEXT_POS = (100, 540-SCORE_HAND_DISPLAY_TEXT_SIZE*3)
def DrawHandScoreDisplay():
    papyrusFontHandScore = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_HAND_DISPLAY_TEXT_SIZE)
    handScoreText = papyrusFontHandScore.render(f"Hand Score : {roundManager.CalculateHandScore(selectionManager.currentHand_bestHandType)}", True, (255,255,255), (0,0,0))
    screen.blit(handScoreText, SCORE_HAND_DISPLAY_TEXT_POS)

SCORE_TOTAL_DISPLAY_TEXT_SIZE = 50
SCORE_TOTAL_DISPLAY_TEXT_POS = (100, 540-SCORE_TOTAL_DISPLAY_TEXT_SIZE*5)
def DrawTotalScoreDisplay():
    papyrusFontTotalScore = pg.font.Font("resources/fonts/papyrus.ttf", SCORE_HAND_DISPLAY_TEXT_SIZE)
    totalScoreText = papyrusFontTotalScore.render(f"Total Score : {roundManager.totalScore}", True, (255,255,255), (0,0,0))
    screen.blit(totalScoreText, SCORE_TOTAL_DISPLAY_TEXT_POS)

HAND_TYPE_DISPLAY_TEXT_SIZE = 50
HAND_TYPE_DISPLAY_TEXT_POS = (100, 540-HAND_TYPE_DISPLAY_TEXT_SIZE*7)
def DrawHandTypeDisplay():
    papyrusFontHandType = pg.font.Font("resources/fonts/papyrus.ttf", HAND_TYPE_DISPLAY_TEXT_SIZE)
    handTypeText = papyrusFontHandType.render(f"{selectionManager.currentHand_bestHandType}", True, (255,255,255), (0,0,0))
    screen.blit(handTypeText, HAND_TYPE_DISPLAY_TEXT_POS)


HANDS_LEFT_TEXT_SIZE = 50
HANDS_LEFT_TEXT_POS = (0, 540+HANDS_LEFT_TEXT_SIZE)
def DrawHandsLeftDisplay():
    papyrusFontHandsLeft = pg.font.Font("resources/fonts/papyrus.ttf", HANDS_LEFT_TEXT_SIZE)
    handsLeftText = papyrusFontHandsLeft.render(f"{roundManager.handsLeft}", True, (255,255,255), (0,0,128))
    screen.blit(handsLeftText, HANDS_LEFT_TEXT_POS)

DISCARDS_LEFT_TEXT_SIZE = 50
DISCARDS_LEFT_TEXT_POS = (0, 540-DISCARDS_LEFT_TEXT_SIZE)
def DrawDiscardsLeftDisplay():
    papyrusFontDiscardsLeft = pg.font.Font("resources/fonts/papyrus.ttf", DISCARDS_LEFT_TEXT_SIZE)
    discardsLeftText = papyrusFontDiscardsLeft.render(f"{roundManager.discardsLeft}", True, (255,255,255), (128,0,0))
    screen.blit(discardsLeftText, DISCARDS_LEFT_TEXT_POS)

PLAY_BUTTON_TEXT_SIZE = 50
def DrawPlayHandButton():
    font = pg.font.Font("resources/fonts/papyrus.ttf", 50)
    text = font.render("Play Hand", True, (255,255,255), (0,0,128))
    ui_state.playButtonRect = screen.blit(
        text,
        ((DEFAULT_SCREEN_SIZE_X/2 - 350), 1000)
    )
DISCARD_BUTTON_TEXT_SIZE = 50
def DrawDiscardHandButton():
    font = pg.font.Font("resources/fonts/papyrus.ttf", 50)
    text = font.render("Discard Hand", True, (255,255,255), (128,32,0))
    ui_state.discardButtonRect = screen.blit(
        text,
        ((DEFAULT_SCREEN_SIZE_X/2 + 100), 1000)
    )
#endregion
def CheckForButtonsPress():
    mouse_pos = pg.mouse.get_pos()
    # convert to screen coords if using scaled surface
    # scr_mouse = WindowToScreenPos(mouse_pos, screen, window)
    scr_mouse = WindowToScreenPos(mouse_pos, screen, window)
    if input.lmb:
        ui_state.pressedPlayHand = ui_state.playButtonRect.collidepoint(scr_mouse)
        ui_state.pressedDiscardHand = ui_state.discardButtonRect.collidepoint(scr_mouse)
    else:
        ui_state.pressedPlayHand = False
        ui_state.pressedDiscardHand = False
#endregion
def DrawToInternalScreen(_inRound):
    #Draw to internal screen
    #Black borders
    screen.fill((27,112,50))
    #Draw cards
    DrawJokers()
    if _inRound:
        DrawHand()
        #Score
        DrawChipsDisplay()
        DrawMultDisplay()
        DrawHandScoreDisplay()
        DrawTotalScoreDisplay()

        DrawHandTypeDisplay()
        #Hands&Discards
        DrawHandsLeftDisplay()
        DrawDiscardsLeftDisplay()
        DrawPlayHandButton()
        DrawDiscardHandButton()
def ShowUI(_inRound):
    
    DrawToInternalScreen(_inRound)

    window.fill((0, 0, 0))
    CheckForButtonsPress()

    scaled, pos = scale_surface(screen, window.get_size())
    window.blit(scaled, pos)
    pg.display.flip()
    clock.tick(60)

import pygame as pg
from jokers import *
from cards import *
from helper import *
import jokerManager, deckManager, handManager, selectionManager, roundManager, input
import ui_state
import timeManager

# ----------------------------
# INITIAL SETUP
# ----------------------------
pg.init()

DEFAULT_WINDOW_SIZE_X = 1280
DEFAULT_WINDOW_SIZE_Y = 720
DEFAULT_SCREEN_SIZE_X = 1920
DEFAULT_SCREEN_SIZE_Y = 1080

window = pg.display.set_mode((DEFAULT_WINDOW_SIZE_X, DEFAULT_WINDOW_SIZE_Y), pg.RESIZABLE)
screen = pg.Surface((DEFAULT_SCREEN_SIZE_X, DEFAULT_SCREEN_SIZE_Y))
clock = pg.time.Clock()

scaleX = screen.get_size()[0] / DEFAULT_WINDOW_SIZE_X
scaleY = screen.get_size()[1] / DEFAULT_WINDOW_SIZE_Y

FLOATING_TEXT_SPEED = 80
GLOBAL_FONT = "resources/fonts/balatroFont.ttf"

# ----------------------------
# FLOATING TEXTS
# ----------------------------

def UpdateFloatingDisplays():
    for floatingText in ui_state.floatingTexts:
        floatingText.elapsedTime += timeManager.deltaTime
        if floatingText.elapsedTime > floatingText.timer:
            ui_state.floatingTexts.remove(floatingText)

def DrawFloatingTexts():

    for floatingText in ui_state.floatingTexts:
        
        floatingTextFont = pg.font.Font(GLOBAL_FONT, 40)

        if not floatingText.invertBgAndColor:
            text_surface = floatingTextFont.render(
                floatingText.text,
                True,
                (255, 255, 255),
                floatingText.color
            )
        else:
            text_surface = floatingTextFont.render(
                floatingText.text,
                True,
                floatingText.color
                
            )
        
        floatingTextPos = (CenterObject(floatingText.pos[0], len(jokerManager.equippedJokers), JOKER_W*JOKER_SCALE, 5, JOKER_ZONE_LEFTX, JOKER_ZONE_RIGHTX) + JOKER_W*JOKER_SCALE/2, floatingText.pos[1] + JOKER_H*JOKER_SCALE)
        

        text_surface = floatingTextFont.render(
            floatingText.text,
            True,
            (255, 255, 255),
            floatingText.color
        )

        screen.blit(
            text_surface,
            (floatingTextPos)
        )



# ----------------------------
# CARDS
# ----------------------------
CARD_ZONE_LEFTX = 530
CARD_ZONE_RIGHTX = 1650
CARD_AREA_DEFAULT_POS_Y = 633
CARD_SELECT_OFFSET = -100

cardSelectionRect: list[pg.Rect] = []
allCardsRects: list[list[pg.Rect]] = []

playButtonRect = None
discardButtonRect = None
cardYOffset = [0 for _ in range(handManager.currentHandSize)]
pressedPlayHand = False
pressedDiscardHand = False

def CreateCardRects(_slot, *layers):
    rects = []
    for layer in layers:
        rects.append(
            screen.blit(
                layer,
                (
                    CenterObject(
                        _slot,
                        handManager.currentHandSize,
                        CARD_W * CARD_SCALE,
                        5,
                        CARD_ZONE_LEFTX,
                        CARD_ZONE_RIGHTX
                    ),
                    CARD_AREA_DEFAULT_POS_Y + cardYOffset[_slot]
                )
            )
        )
    return rects

def DrawCard(card: Card, slot):
    cardTexCoords = ValueAndSuitToAtlasCoords(card.value, card.suit)

    image_enh_bg_card = CARD_BG_ATLAS.get(*ENHANCEMENT_TO_ATLASCOORDS[card.enhancement]) if card.enhancement not in ENHANCEMENT_OVERLAYS else EmptyImage(CARD_W, CARD_H)
    image_card = CARD_ATLAS.get(*cardTexCoords)
    image_enh_over_card = CARD_BG_ATLAS.get(*ENHANCEMENT_TO_ATLASCOORDS[card.enhancement]) if card.enhancement in ENHANCEMENT_OVERLAYS else EmptyImage(CARD_W, CARD_H)
    image_card_seal = CARD_BG_ATLAS.get(*SEAL_TO_ATLASCOORDS[card.seal]) if card.seal != "None" and card.enhancement not in ENHANCEMENT_NO_SEAL else EmptyImage(CARD_W, CARD_H)
    image_card_debuff = CARD_BG_ATLAS.get(7, 0) if card.debuffed else EmptyImage(CARD_W, CARD_H)

    # Scale all
    image_enh_bg_card = pg.transform.smoothscale_by(image_enh_bg_card, CARD_SCALE)
    image_card = pg.transform.smoothscale_by(image_card, CARD_SCALE)
    image_enh_over_card = pg.transform.smoothscale_by(image_enh_over_card, CARD_SCALE)
    image_card_seal = pg.transform.smoothscale_by(image_card_seal, CARD_SCALE)
    image_card_debuff = pg.transform.smoothscale_by(image_card_debuff, CARD_SCALE)

    rects = CreateCardRects(slot, image_enh_bg_card, image_card, image_enh_over_card, image_card_seal, image_card_debuff)
    allCardsRects.append(rects)
    cardSelectionRect.append(rects[0])

def DrawHand():
    global cardSelectionRect
    cardSelectionRect = []
    for i, card in enumerate(handManager.currentHand):
        DrawCard(card, i)

def SelectCard(slot: int):
    cardYOffset[slot] = CARD_SELECT_OFFSET

def DeselectCard(slot: int):
    cardYOffset[slot] = 0


# ----------------------------
# JOKERS
# ----------------------------
JOKER_ZONE_LEFTX = 508
JOKER_ZONE_RIGHTX = 1410
JOKER_TEXT_OFFSET_Y = 140
JOKER_Y_POS = 15

def DrawJoker(joker: Joker, slot):
    image_joker = JOKER_ATLAS.get(joker.textureCoords[0], joker.textureCoords[1])
    image_joker = pg.transform.smoothscale_by(image_joker, JOKER_SCALE)
    screen.blit(image_joker, (CenterObject(slot, len(jokerManager.equippedJokers), JOKER_W*JOKER_SCALE, 5, JOKER_ZONE_LEFTX, JOKER_ZONE_RIGHTX), JOKER_Y_POS))

def DrawJokers():
    for i, joker in enumerate(jokerManager.equippedJokers):
        DrawJoker(joker, i)


# ----------------------------
# SCORE DISPLAY
# ----------------------------

def CenterObjectFromCorners(upperLeft, bottomRight, surface):
    """
    Returns the top-left position needed to center `surface`
    inside the rectangle defined by upperLeft and bottomRight.
    """
    rectWidth = bottomRight[0] - upperLeft[0]
    rectHeight = bottomRight[1] - upperLeft[1]

    centerX = upperLeft[0] + rectWidth / 2
    centerY = upperLeft[1] + rectHeight / 2

    return (
        centerX - surface.get_width() / 2,
        centerY - surface.get_height() / 2
    )

GLOBAL_FONT_SIZE = 72

SCORE_CHIPS_TEXT_POS = [(25, 545),(213, 643)]
SCORE_MULT_TEXT_POS = [(270, 545),(456, 643)]
SCORE_HAND_DISPLAY_POS = (110, 465)
HAND_TYPE_DISPLAY_POS = [(10,431),(472,528)]
SCORE_TOTAL_DISPLAY_POS = [(151,340),(460,410)]
HANDS_LEFT_DISPLAY_POS = [(201,713),(314,780)]
DISCARDS_LEFT_DISPLAY_POS = [(349,713),(461,780)]

def DrawChipsDisplay():
    chips, addedChips = roundManager.CalculateChips(selectionManager.currentHand_bestHandType)

    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)
    textSurface = font.render(f"{chips}", True, (255,255,255), (0,146,255))

    pos = CenterObjectFromCorners(SCORE_CHIPS_TEXT_POS[0], SCORE_CHIPS_TEXT_POS[1], textSurface)
    screen.blit(textSurface, pos)

def DrawMultDisplay():
    mult, addedMult = roundManager.CalculateMult(selectionManager.currentHand_bestHandType)
    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)

    textSurface = font.render(f"{mult}", True, (255,255,255), (254,76,64))

    pos = CenterObjectFromCorners(SCORE_MULT_TEXT_POS[0], SCORE_MULT_TEXT_POS[1], textSurface)
    screen.blit(textSurface, pos)

def DrawHandScoreDisplay():
    score = roundManager.CalculateHandScore()
    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)
    screen.blit(font.render(str(score), True, (255, 255, 255), (47, 58, 60)), SCORE_HAND_DISPLAY_POS)

def DrawHandTypeDisplay():
    handType = selectionManager.currentHand_bestHandType
    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)

    textSurface = font.render(str(handType), True, (255, 255, 255), (24, 35, 37))
    pos = CenterObjectFromCorners(HAND_TYPE_DISPLAY_POS[0],HAND_TYPE_DISPLAY_POS[1],textSurface)
    screen.blit(textSurface, pos)

def DrawTotalScoreDisplay():
    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)

    textSurface = font.render(str(roundManager.totalScore), True, (255, 255, 255), (47,58,60))
    pos = CenterObjectFromCorners(SCORE_TOTAL_DISPLAY_POS[0],SCORE_TOTAL_DISPLAY_POS[1], textSurface)
    screen.blit(textSurface, pos)

def DrawHandsLeftDisplay():
    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)

    textSurface = font.render(str(roundManager.handsLeft), True, (0, 146, 255))
    pos = CenterObjectFromCorners(HANDS_LEFT_DISPLAY_POS[0], HANDS_LEFT_DISPLAY_POS[1], textSurface)
    screen.blit(textSurface, pos)

def DrawDiscardsLeftDisplay():
    font = pg.font.Font(GLOBAL_FONT, GLOBAL_FONT_SIZE)

    textSurface = font.render(str(roundManager.discardsLeft), True, (254,76,64))
    pos = CenterObjectFromCorners(DISCARDS_LEFT_DISPLAY_POS[0], DISCARDS_LEFT_DISPLAY_POS[1], textSurface)
    screen.blit(textSurface, pos)


# ----------------------------
# BUTTONS
# ----------------------------
PLAY_HAND_BUTTON_POS = [(729,900),(936,1027)]
DISCARD_HAND_BUTTON_POS = [(1153,900),(1360,1026)]
def DrawPlayHandButton():

    font = pg.font.Font(GLOBAL_FONT, 35)

    if(len(selectionManager.selectedCards) > 0 and roundManager.handsLeft > 0):
        textSurface = font.render("Play Hand", True, (0,83,157))
        buttonBg = pg.draw.rect(screen, (0, 146, 255), pg.Rect(PLAY_HAND_BUTTON_POS[0][0],
                                                    PLAY_HAND_BUTTON_POS[0][1],
                                                    PLAY_HAND_BUTTON_POS[1][0]-PLAY_HAND_BUTTON_POS[0][0],
                                                    PLAY_HAND_BUTTON_POS[1][1]-PLAY_HAND_BUTTON_POS[0][1]))
    
    else:
        textSurface = font.render("Play Hand", True, (255,255,255), (84,76,77))
        buttonBg = pg.draw.rect(screen, (84,76,77), pg.Rect(PLAY_HAND_BUTTON_POS[0][0],
                                                    PLAY_HAND_BUTTON_POS[0][1],
                                                    PLAY_HAND_BUTTON_POS[1][0]-PLAY_HAND_BUTTON_POS[0][0],
                                                    PLAY_HAND_BUTTON_POS[1][1]-PLAY_HAND_BUTTON_POS[0][1]))
    
    ui_state.playButtonRect = buttonBg

    pos = CenterObjectFromCorners(PLAY_HAND_BUTTON_POS[0], PLAY_HAND_BUTTON_POS[1], textSurface)
    screen.blit(textSurface, pos)

def DrawDiscardHandButton():

    font = pg.font.Font(GLOBAL_FONT, 35)

    if(len(selectionManager.selectedCards) > 0 and roundManager.discardsLeft > 0):
        textSurface = font.render("Discard Hand", True, (156,37,30))
        buttonBg = pg.draw.rect(screen, (254,76,64), pg.Rect(DISCARD_HAND_BUTTON_POS[0][0],
                                                        DISCARD_HAND_BUTTON_POS[0][1],
                                                        DISCARD_HAND_BUTTON_POS[1][0]-DISCARD_HAND_BUTTON_POS[0][0],
                                                        DISCARD_HAND_BUTTON_POS[1][1]-DISCARD_HAND_BUTTON_POS[0][1]))
    else:
        textSurface = font.render("Discard Hand", True, (255,255,255),(84,76,77))
        buttonBg = pg.draw.rect(screen, (84,76,77), pg.Rect(DISCARD_HAND_BUTTON_POS[0][0],
                                                        DISCARD_HAND_BUTTON_POS[0][1],
                                                        DISCARD_HAND_BUTTON_POS[1][0]-DISCARD_HAND_BUTTON_POS[0][0],
                                                        DISCARD_HAND_BUTTON_POS[1][1]-DISCARD_HAND_BUTTON_POS[0][1]))
    
    ui_state.discardButtonRect = buttonBg
    
    pos = CenterObjectFromCorners(DISCARD_HAND_BUTTON_POS[0], DISCARD_HAND_BUTTON_POS[1], textSurface)
    screen.blit(textSurface, pos)

def CheckForButtonsPress():
    mouse_pos = pg.mouse.get_pos()
    scr_mouse = WindowToScreenPos(mouse_pos, screen, window)
    if input.lmb:
        ui_state.pressedPlayHand = ui_state.playButtonRect.collidepoint(scr_mouse)
        ui_state.pressedDiscardHand = ui_state.discardButtonRect.collidepoint(scr_mouse)
    else:
        ui_state.pressedPlayHand = False
        ui_state.pressedDiscardHand = False


# ----------------------------
# MAIN DRAW
# ----------------------------
def DrawToInternalScreen(_inRound):
    screen.fill((27, 112, 50))
    bannerImg = pg.image.load("resources/textures/banner.png")
    screen.blit(bannerImg, (0,0))
    DrawJokers()
    DrawFloatingTexts()

    if _inRound:
        DrawHand()
        DrawChipsDisplay()
        DrawMultDisplay()
        #DrawHandScoreDisplay()
        DrawTotalScoreDisplay()
        DrawHandTypeDisplay()
        DrawHandsLeftDisplay()
        DrawDiscardsLeftDisplay()
        DrawPlayHandButton()
        DrawDiscardHandButton()

        UpdateFloatingDisplays()

def ShowUI(_inRound):
    DrawToInternalScreen(_inRound)
    window.fill((0, 0, 0))
    CheckForButtonsPress()
    scaled, pos = scale_surface(screen, window.get_size())
    window.blit(scaled, pos)
    pg.display.flip()
    clock.tick(60)

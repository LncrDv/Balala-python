import pygame as pg
from jokers import *
from cards import *
from helper import *
import jokerManager, deckManager, handManager, selectionManager, roundManager, input
import ui_state

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
def DrawFloatingTexts():
    font = pg.font.Font(GLOBAL_FONT, 36)
    mult_stack = 0
    chips_stack = 0

    for ft in ui_state.floatingTexts[:]:
        ft.timer -= clock.get_time() / 1000
        ft.alpha = int(255 * (ft.timer / 0.6))
        ft.pos[1] -= FLOATING_TEXT_SPEED * clock.get_time() / 1000

        if ft.timer <= 0:
            ui_state.floatingTexts.remove(ft)
            continue

        # Stack MULT and CHIPS separately
        if "MULT" in ft.text:
            ft.pos[0], ft.pos[1] = ui_state.MULT_FLOAT_POS[0], ui_state.MULT_FLOAT_POS[1] - mult_stack * 40
            mult_stack += 1
        elif "CHIPS" in ft.text:
            ft.pos[0], ft.pos[1] = ui_state.CHIPS_FLOAT_POS[0], ui_state.CHIPS_FLOAT_POS[1] - chips_stack * 40
            chips_stack += 1

        surf = font.render(ft.text, True, ft.color)
        surf.set_alpha(ft.alpha)
        screen.blit(surf, ft.pos)


# ----------------------------
# CARDS
# ----------------------------
CARD_AREA_X = 1500
CARD_AREA_DEFAULT_POS_Y = 700
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
                        screen.get_width(),
                        CARD_AREA_X
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
JOKER_AREA_X = 1000
JOKER_TEXT_OFFSET_Y = 140

def DrawJoker(joker: Joker, slot):
    image_joker = JOKER_ATLAS.get(joker.textureCoords[0], joker.textureCoords[1])
    image_joker = pg.transform.smoothscale_by(image_joker, JOKER_SCALE)
    screen.blit(image_joker, (CenterObject(slot, len(jokerManager.equippedJokers), JOKER_W*JOKER_SCALE, 5, screen.get_width(), JOKER_AREA_X), 0))

def DrawJokers():
    for i, joker in enumerate(jokerManager.equippedJokers):
        DrawJoker(joker, i)


# ----------------------------
# SCORE DISPLAY
# ----------------------------
SCORE_CHIPS_TEXT_POS = (100, 590)
SCORE_MULT_TEXT_POS = (100, 490)
SCORE_HAND_DISPLAY_POS = (100, 400)
HAND_TYPE_DISPLAY_POS = (100, 300)
SCORE_TOTAL_DISPLAY_POS = (100, 180)
HANDS_LEFT_DISPLAY_POS = (0, 590)
DISCARDS_LEFT_DISPLAY_POS = (0, 180)

ui_state.MULT_FLOAT_POS = (SCORE_MULT_TEXT_POS[0] + 260, SCORE_MULT_TEXT_POS[1])
ui_state.CHIPS_FLOAT_POS = (SCORE_CHIPS_TEXT_POS[0] + 260, SCORE_CHIPS_TEXT_POS[1])

def DrawChipsDisplay():
    chips, addedChips = roundManager.CalculateChips(selectionManager.currentHand_bestHandType)
    font = pg.font.Font(GLOBAL_FONT, 50)
    text = f"Chips : {chips}" + (f" + {addedChips}" if addedChips else "")
    screen.blit(font.render(text, True, (255, 255, 255), (0, 0, 128)), SCORE_CHIPS_TEXT_POS)

def DrawMultDisplay():
    mult, addedMult = roundManager.CalculateMult(selectionManager.currentHand_bestHandType)
    font = pg.font.Font(GLOBAL_FONT, 50)
    text = f"Mult : {mult}" + (f" + {addedMult}" if addedMult else "")
    screen.blit(font.render(text, True, (255, 255, 255), (128, 0, 0)), SCORE_MULT_TEXT_POS)

def DrawHandScoreDisplay():
    score = roundManager.CalculateHandScore()
    font = pg.font.Font(GLOBAL_FONT, 50)
    screen.blit(font.render(str(score), True, (255, 255, 255), (0, 0, 0)), SCORE_HAND_DISPLAY_POS)

def DrawHandTypeDisplay():
    handType = selectionManager.currentHand_bestHandType
    font = pg.font.Font(GLOBAL_FONT, 50)
    screen.blit(font.render(str(handType), True, (255, 255, 255), (0, 0, 0)), HAND_TYPE_DISPLAY_POS)

def DrawTotalScoreDisplay():
    font = pg.font.Font(GLOBAL_FONT, 50)
    screen.blit(font.render(str(roundManager.totalScore), True, (255, 255, 255), (0, 0, 0)), SCORE_TOTAL_DISPLAY_POS)

def DrawHandsLeftDisplay():
    font = pg.font.Font(GLOBAL_FONT, 50)
    screen.blit(font.render(str(roundManager.handsLeft), True, (255, 255, 255), (0, 0, 128)), HANDS_LEFT_DISPLAY_POS)

def DrawDiscardsLeftDisplay():
    font = pg.font.Font(GLOBAL_FONT, 50)
    screen.blit(font.render(str(roundManager.discardsLeft), True, (255, 255, 255), (128, 0, 0)), DISCARDS_LEFT_DISPLAY_POS)


# ----------------------------
# BUTTONS
# ----------------------------
def DrawPlayHandButton():
    font = pg.font.Font(GLOBAL_FONT, 50)
    text = font.render("Play Hand", True, (255, 255, 255), (0, 0, 128))
    ui_state.playButtonRect = screen.blit(text, ((DEFAULT_SCREEN_SIZE_X / 2 - 350), 1000))

def DrawDiscardHandButton():
    font = pg.font.Font(GLOBAL_FONT, 50)
    text = font.render("Discard Hand", True, (255, 255, 255), (128, 32, 0))
    ui_state.discardButtonRect = screen.blit(text, ((DEFAULT_SCREEN_SIZE_X / 2 + 100), 1000))

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
    DrawJokers()
    DrawFloatingTexts()

    if _inRound:
        DrawHand()
        DrawChipsDisplay()
        DrawMultDisplay()
        DrawHandScoreDisplay()
        DrawTotalScoreDisplay()
        DrawHandTypeDisplay()
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

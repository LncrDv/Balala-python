# ui_state.py

# --------------------------------------------------
# Button state
# --------------------------------------------------

MULT_FLOAT_POS = (360, 490)
CHIPS_FLOAT_POS = (360, 590)

playButtonRect = None
discardButtonRect = None
pressedPlayHand = False
pressedDiscardHand = False



joker_mult_stack = 0
joker_chips_stack = 0

floatingTexts = []


class FloatingText:
    def __init__(self, text, pos, color, timer, invertBgAndColor = False):
        self.text = text

        self.pos = [pos[0], pos[1]]
        self.start_y = pos[1]

        self.color = color
        self.timer = timer
        self.elapsedTime = 0

        self.invertBgAndColor = invertBgAndColor

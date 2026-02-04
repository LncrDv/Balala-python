# ui_state.py

# --------------------------------------------------
# Button state
# --------------------------------------------------
playButtonRect = None
discardButtonRect = None
pressedPlayHand = False
pressedDiscardHand = False


# --------------------------------------------------
# Floating text anchor positions (screen space)
# These should match your UI layout
# --------------------------------------------------
MULT_FLOAT_POS = (360, 490)
CHIPS_FLOAT_POS = (360, 590)


# --------------------------------------------------
# Floating text stacking state
# (prevents overlap)
# --------------------------------------------------
joker_mult_stack = 0
joker_chips_stack = 0


# --------------------------------------------------
# Floating text storage
# --------------------------------------------------
floatingTexts = []


class FloatingText:
    def __init__(self, text, pos, color):
        self.text = text

        # IMPORTANT: copy position so instances don't share it
        self.pos = [pos[0], pos[1]]
        self.start_y = pos[1]

        self.color = color
        self.timer = 0.6
        self.alpha = 255

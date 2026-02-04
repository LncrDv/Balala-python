from jokers import *
import random
import roundManager
import ui_state

equippedJokers = []

def generateRandomJokers(n):
    global equippedJokers
    equippedJokers = []
    for _ in range(n):
        equippedJokers.append(random.choice(list(collection_jokers.values())))

    for joker in equippedJokers:
        print("Equipped Joker : ", joker.name)

def ApplyJoker(joker: Joker):
    for modifier in joker.modifiers.keys():
        value = joker.modifiers[modifier]

        if modifier in ("active", "debuffed") and value is True:
            return

        if modifier == "conditionnal":
            for condition in value:
                match condition:
                    case "requireHandOfType":
                        if value["requireHandOfType"] not in roundManager.currentHand_handTypes:
                            return

        match modifier:
            case "plusMult":
                roundManager.UpdateScore(_plusMult=value)

                # ✅ Joker-only visual
                ui_state.floatingTexts.append(
                    ui_state.FloatingText(
                        f"+{value} MULT",
                        ui_state.MULT_FLOAT_POS,
                        (255, 220, 0)
                    )
                )

            case "plusChips":
                roundManager.UpdateScore(_plusChips=value)

                # ✅ Joker-only visual
                ui_state.floatingTexts.append(
                    ui_state.FloatingText(
                        f"+{value} CHIPS",
                        ui_state.CHIPS_FLOAT_POS,
                        (120, 255, 200)
                    )
                )

def ApplyJokerEffects():
    global equippedJokers
    for joker in equippedJokers:
        ApplyJoker(joker)
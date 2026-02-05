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
    for modifier, modifierValue in joker.modifiers.items():

        if modifier in ("active", "debuffed") and modifierValue is True:
            return

        if modifier == "conditionnal":
            for condition, conditionValue in modifierValue.items():
                match condition:
                    case "requireHandOfType":
                        if conditionValue not in roundManager.currentHand_handTypes:
                            print(roundManager.currentHand_handTypes)
                            print(f'''Joker "{joker.name}" did not fulfill condition : {condition} = {conditionValue} !''')
                            return
                    case "requireCardOfSuit":

                        condAffectDomain = joker.modifiers[modifier]["conditionAffectDomain"]

                        joker.modifiers[condAffectDomain] = 0

                        for card in roundManager.playedHand:
                            if card.suit == conditionValue:
                                joker.modifiers[condAffectDomain] += joker.modifiers[modifier]["increment"]



        match modifier:
            case "plusMult":
                roundManager.UpdateScore(_plusMult=modifierValue)

                # Joker-only visual
                ui_state.floatingTexts.append(
                    ui_state.FloatingText(
                        f"+{modifierValue}",
                        (equippedJokers.index(joker), 10),
                        (255, 0, 0),
                        1
                    )
                )

            case "plusChips":
                roundManager.UpdateScore(_plusChips=modifierValue)

                # Joker-only visual
                ui_state.floatingTexts.append(
                    ui_state.FloatingText(
                        f"+{modifierValue}",
                        (equippedJokers.index(joker), 10),
                        (0, 0, 255),
                        1
                    )
                )

def ApplyJokerEffects():
    global equippedJokers
    for joker in equippedJokers:
        ApplyJoker(joker)
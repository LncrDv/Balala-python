from jokers import *
import random
import roundManager
equippedJokers = []

def generateRandomJokers(n):
    global equippedJokers
    equippedJokers = []
    for _ in range(n):
        equippedJokers.append(random.choice(list(collection_jokers.values())))

    for joker in equippedJokers:
        print("Equipped Joker : ", joker.name)

def ApplyJokerEffects():
    global equippedJokers
    for joker in equippedJokers:
        for modifier in joker.modifiers.keys():
            if modifier == "active" or modifier == "debuffed":
                if joker.modifiers[modifier] == True:
                    print(f'''Joker {joker.name} is debuffed !''')
                    continue
            else:
                match modifier:
                    case "plusMult":
                        print(f'''Joker {joker.name} added {joker.modifiers["plusMult"]} mult !''')
                        roundManager.UpdateScore(_plusMult = joker.modifiers["plusMult"])
                    case "plusChips":
                        print(f'''Joker {joker.name} added {joker.modifiers["plusChips"]} chips !''')
                        roundManager.UpdateScore(_plusChips = joker.modifiers["plusChips"])
                    case __:
                        pass
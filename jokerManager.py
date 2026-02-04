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

def ApplyJoker(joker : Joker):
    for modifier in joker.modifiers.keys():
            value = joker.modifiers[modifier]
            if modifier == "active" or modifier == "debuffed":
                if value == True:
                    print(f'''Joker {joker.name} is debuffed !''')
                    return
            
            else:
                #Conditionnal Jokers
                if modifier == "conditionnal":
                    for condition in value:
                        
                        #For each condition in the conditionnal dict
                        match condition:
                            #Conditions in conditionnal dict
                            case "requireHandOfType":
                                if not value["requireHandOfType"] in roundManager.currentHand_handTypes:
                                    print(f'''Joker {joker.name} did not fulfill condition : {value["requireHandOfType"]} !''')
                                    return
                
                
                match modifier:
                    case "plusMult":
                        print(f'''Joker {joker.name} added {value} mult !''')
                        roundManager.UpdateScore(_plusMult = value)
                    case "plusChips":
                        print(f'''Joker {joker.name} added {value} chips !''')
                        roundManager.UpdateScore(_plusChips = value)
                    case __:
                        pass
def ApplyJokerEffects():
    global equippedJokers
    for joker in equippedJokers:
        ApplyJoker(joker)
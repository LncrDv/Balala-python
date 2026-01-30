from jokers import *
import random
equippedJokers = []

def generateRandomJokers(n):
    global equippedJokers
    equippedJokers = []
    for i in range(n):
        equippedJokers.append(random.choice(list(collection_jokers.values())))

    for joker in equippedJokers:
        print("Equipped Joker : ", joker.name)

#10.66 jokers at 2.5x scale fit in the screen
#generateRandomJokers(5)

def generate52CardDeck():
    pass
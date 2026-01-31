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
#treshold = 16 (600x100000) -> mean = -0.05469955


import itertools
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def new_deck():
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'I', 'I']*4
    random.shuffle(deck)
    return deck

def evaluate_hand(hand):
    value = 0
    A_cards = 0
    I_cards = 0
    for card in hand:
        if card in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            value += int(card)
        if card in ['J', 'Q', 'K']:
            value += 10
        if card == 'A':
            A_cards += 1
        if card == 'I':
            I_cards += 1
            
    if I_cards > 0 and I_cards % 4 == 0:
        value += 1
    if I_cards % 4 == 2:
        value -= 1
    values = [value]
    for _ in range(A_cards):
        updated_values = []
        for v in values:
            updated_values.append(v+1)
            updated_values.append(v+11)
        values = list(set(updated_values))
    return values

def init_dealer(deck):
    dealer_hand = []
    dealer_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    
    #print('initial dealer_hand', dealer_hand)
    return dealer_hand
    
def dealer(deck, dealer_hand):
    values = evaluate_hand(dealer_hand)
    values = [i for i in values if i <= 21]
    while values and max(values) < 17:
        dealer_hand.append(deck.pop())
        values = evaluate_hand(dealer_hand)
        values = [i for i in values if i <= 21]
        if not values:
            break
    
    #print('dealer_hand', dealer_hand)
    if not values:
        return -1
    else:
        return max(values)
    
def init_player(deck):
    player_hand = []
    player_hand.append(deck.pop())
    player_hand.append(deck.pop())
    #print('initial player_hand', player_hand)
    return player_hand

def player(deck, player_hand):
    #define treshold -> HARDCODED
    treshold = 17
    
    values = evaluate_hand(player_hand)
    values = [i for i in values if i <= 21]
    
    while max(values) < treshold:
        player_hand.append(deck.pop())
        values = evaluate_hand(player_hand)
        values = [i for i in values if i <= 21]
        if not values:
            break
            
    #print('player_hand', player_hand)        
    if not values:
        return -1
    else:
        return max(values)


res = []

#simulation
for _ in range(100):
    player_account = 0
    n = 100000
    for _ in range(n):
        deck = new_deck()
        initial_dealer_hand = init_dealer(deck)
        initial_player_hand = init_player(deck)

        #check if player gets a blackjack
        if 21 in evaluate_hand(initial_player_hand):
            #in case dealer also gets a blackjack it's a tie
            if not 21 in evaluate_hand(initial_dealer_hand):
                player_account += 1.5
                continue

        player_score = player(deck, initial_player_hand)
        dealer_score = dealer(deck, initial_dealer_hand)

        if player_score == -1:
            player_account -= 1
        else:
            if dealer_score == -1:
                player_account += 1
            else:
                if player_score > dealer_score:
                    player_account += 1
                if player_score < dealer_score:
                    player_account -= 1
    
    res.append(player_account/n)

plt.hist(res)
res = np.array(res)
print(res.mean())
plt.show()
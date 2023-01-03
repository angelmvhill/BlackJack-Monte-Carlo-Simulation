from random import randint
import numpy as np

class Dealer:
    flag_ace = False
    firstcard = 0
    cards = []

    def __init__(self, card):
        if card>10:
            card=10
        self.firstcard = card

    def getcard(self):
        card = randint(1,13)
        if card>10:
            card=10
        if card==1:
            self.flag_ace = True
        self.cards.append(card)

    def calculatescore(self):
        score = np.sum(np.array(self.cards))
        if self.flag_ace:
            if score<=11:
                score += 10    #This means one ace can be treat as 11 not 1
        return score

    def play(self):
        self.cards = [self.firstcard]
        if self.firstcard==1:
            self.flag_ace = True
        else:
            self.flag_ace = False
        while True:
            self.getcard()
            score = self.calculatescore()
            if self.flag_ace and score>17:
                break
            if self.flag_ace==False and score>16:
                break
        return score


class Player:
    cards = []
    flag_ace = False

    def __init__(self, card1, card2):
        self.cards = [card1, card2]
        if card1==1 or card2==1:
            self.flag_ace = True

    def hit(self):
        card = randint(1,13)
        if card>10:
            card=10
        if card==1:
            self.flag_ace = True
        self.cards.append(card)

    def calculatescore(self):
        score = np.sum(np.array(self.cards))
        if self.flag_ace:
            if score<=11:
                score += 10    #This means one ace can be treat as 11 not 1
        return score

def play(self, dealercard, policy, simulate=False):
    card1 = self.cards[0]
    card2 = self.cards[1]
    hitcount = 0
    scale = 1.0
    count = 0
    while True:
        if self.flag_ace and len(self.cards)==2:
            if max(card1, card2)==10:
                scale=1.5
                score=21
                break
            else:
                key = "A,"+str(np.sum(np.array(self.cards))-1)
                action = policy[key][dealercard-1]
        else:
            score = self.calculatescore()
            if score>=18:
                break
            else:
                if self.flag_ace:
                    cardsum = np.sum(np.array(self.cards))
                    if cardsum<12:
                        key = 'A,'+str(cardsum-1)
                    else:
                        key = str(score)
                else:
                    key = str(score)
                action = policy[key][dealercard-1]
        if (action=='D' or action=='D/S') and hitcount==0:
            if simulate:
                self.hit(0)
            else:
                self.hit()
            score = self.calculatescore()
            scale = 2.0
            break
        elif action=='S' or (action=='D/S' and hitcount>0):
            score = self.calculatescore()
            break
        else:
            if simulate:
                self.hit(count)
            else:
                self.hit()
            score = self.calculatescore()
            if score>=18:
                break
            hitcount+=1
            count += 1
    return score, scale

bet = 100
games = 100
loops = 1000
money = []

# create decks of cards
    # encore uses 6 decks
    # create 1 deck full of random cards
        # 24 of each number
    # slice the array at index between 4 and 5 decks
    # ONLY RESHUFFLE WHEN THE DECK IS FINISHED - KEEP GOING UNTIL ALL THE CARDS HAVE GONE THROUGH

# create dealer
    # give 1 card to player - delete card from array
    # give 1 card to dealer - delete card from array
    # give another card to player - delete card from array
    # give another card to dealer (hidden card) - delete card from array

# create player
    # pay bet cost
    # use pandas to reference strategy excel file
        # load strategy as pandas dataframe
        # use column lookup and index from player cards to find strategy rule
        # if value == H
            # draw another random card - delete card from array
            # repeat lookup function
        # if value == S
            # continue to finishing dealer function
        # if value = D
            # double bet - pay another bet
            # draw again - delete card from array
            # repeat lookup
            # continue to finishing dealer function - YOU CAN ONLY DRAW 1 CARD
        # if value == p
            # create two decks - pay another bet
                # repeat H
                    # draw another random card - delete card from array
                    # repeat lookup function

# ace function

# finish dealer strategy
    # keep hitting until cards >= 17 - delete each card drawn
    # if you have a blackjack, and you win, you win 1.2 x initial bet
    # calculate pnl from this bet and find total pnl
    # store total pnl, win/loss or tally Boolean value, tally for doubles and splits, tally for blackjack, tally for H and S

# A BLACKJACK IS AN ACE AND A 10

# Betting strategy
    # try several rounds with the same bet for each iteration
    # 1,3,2,6 betting 
    # 1,2,2,2 betting

# surrender function
    # if you choose to surrender, you canget half your bet back
    # calculate the probability of winning from the specific hand
    # if probability of winning > 50%, don't surrender

# match the dealer and same suit payout
    # what is the expected value

# optimization
    # betting
    # surrender

# how to find patterns

'''
bet1 = 25
bet2 = 50
bet3 = 75
bet6 = 150

for i in number_of_bets:
    if i/4 % 0:
        bet = bet6
    if i/3 % 0:
        bet = bet3
WE WILL NEED TO CHANGE THIS - THIS IS ONLY FOR WINNING STREAK
DOES i START AT 0 OR 1
'''

'''
win == 0 # global variable instantiated outside monte carlo

if win:
    win_streak += 1
if lose:
    win_streak == 0
'''
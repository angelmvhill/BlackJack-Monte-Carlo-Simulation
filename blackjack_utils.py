import random
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn as sns

class Dealer:
    
    def __init__(self):
        pass

    def create_single_deck(self):
        
        unique_cards_within_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 'A']
        unshuffled_card_deck = []
        # create card deck
        for i in range(4):
            for i in unique_cards_within_deck:
                unshuffled_card_deck.append(i)
                
        return unshuffled_card_deck

    def create_multi_deck(self, unshuffled_card_deck):
        
        multi_deck = []
        # add additional decks - for Encore, we will add 6 decks
        for i in range(6):
            for i in unshuffled_card_deck:
                multi_deck.append(i)

        return multi_deck

    def shuffle_deck(self, multi_deck):
        
        random.shuffle(multi_deck)

        return multi_deck

    def cut_deck(self, multi_deck):
        
        # generate random slice number to cut deck
        min_slice = 4.25 * 52
        max_slice = 4.75 * 52
        list_slice = random.randrange(min_slice, max_slice)
        # cut deck
        cut_deck = multi_deck[:list_slice]

        return cut_deck

    def deal_card(self, deck, cards):

        # select 1st card from deck
        deal_card = deck[:1]
        # add 1st card from deck to player cards (we use a loop to remove the item from the deal_card list)
        for i in deal_card:
            cards.append(i)
        # delete 1st card from deck
        del(deck[:1])

        return cards

class Strategy(Dealer):

    def __init__(self, bet, blackjack_payout, portfolio, surrender_loss):
        self.bet = bet
        self.blackjack_payout = blackjack_payout
        self.portfolio = portfolio
        self.surrender_loss = surrender_loss

    def check_ace(self, player_cards):
        
        index_value = None

        # check for ace
        ace_boolean = False
        # check for ace within list
        for i in player_cards:
            if i == 'A':
                ace_boolean = True
        
        # sum cards if ace isn't there
        if ace_boolean == False:
            index_value = sum(player_cards)
            return index_value

        # list for all integer cards
        aceless_list = []
        # count aces
        ace_tally = 0

        # process if there is an ace
        if ace_boolean == True:            
            # add integer cards to list
            for i in player_cards:
                if i != 'A':
                    aceless_list.append(i)
                if i == 'A':
                    ace_tally += 1
            
            # check if there is more than 1 ace -> excess aces count as 1
            if ace_tally > 1:
                ace_excess = ace_tally - 1
                aceless_list.append(ace_excess)
            # sum all non aces
            sum_cards = sum(aceless_list)
            # if greater than 21, ace = 1
            if sum_cards + 11 > 21:
                index_value = sum_cards + 1
            # if not, refer to A,n decision rule
            else:
                index_value = f'A,{sum_cards}'

            return index_value

        else:
            return 'Nothing Returned'

    def get_strategy_decision(self, player_cards, dealer_cards, strategy_df):
               
        player_card_1 = player_cards[0]
        player_card_2 = player_cards[1]
        index_value = None
        bust_value = None
        
        # identify what player card's index value is to search df index
        if len(player_cards) == 2:
            if player_card_1 == player_card_2:
                index_value = f'{player_card_1},{player_card_2}'
            elif player_card_1 == 'A' or player_card_2 == 'A':
                if player_card_1 == 'A':
                    index_value = f'{player_card_1},{player_card_2}'
                if player_card_2 == 'A':
                    index_value = f'{player_card_2},{player_card_1}'
            else:
                index_value = sum(player_cards)

        else:
            index_value = self.check_ace(player_cards)

        if isinstance(index_value, int) == True:
            if index_value > 21:
                # print('Bust')
                return 'Bust'
        
        index_value = str(index_value)
        dealer_card_1 = f'{dealer_cards[0]}'
        decision = strategy_df.loc[index_value][dealer_card_1]
        
        return decision

    def hit(self, deck, player_cards):
        
        # deal card
        player_cards = self.deal_card(deck, player_cards)
        return player_cards

class Payout(Strategy):

    def __init__(self):
        
        pass

    def card_score(self, cards):
        
        # check for ace
        ace_boolean = False
        # check for ace within list
        for i in cards:
            if i == 'A':
                ace_boolean = True
        
        # sum cards if ace isn't there
        if ace_boolean == False:
            score = sum(cards)
            return score

        # list for all integer cards
        aceless_list = []
        # count aces
        ace_tally = 0

        # process if there is an ace
        if ace_boolean == True:            
            # add integer cards to list
            for i in cards:
                if i != 'A':
                    aceless_list.append(i)
                if i == 'A':
                    ace_tally += 1

            if ace_tally == 1:
                temp_score = sum(aceless_list) + 11
                if temp_score > 21:
                    score = sum(aceless_list) + 1
                else:
                    score = temp_score
            else:
                score = sum(aceless_list) + 11 + ace_tally - 1
        
            return score
             
    def blackjack_value(self, cards):

        if len(cards) == 2:
            if self.card_score(cards) == 21:
                return True

        else:
            return False

    def bust(self, card_score):
        
        if card_score > 21:
            return True
        else:
            return False

    def win_loss(self, player_score, dealer_score, player_bust, dealer_bust, bet):

        payout = None

        # both bust
        if player_bust == True and dealer_bust == True:
            payout = 0
            return payout
        # player busts and dealer doesn't
        elif player_bust == True and dealer_bust == False:
            payout = bet
            return payout
        # dealer busts and player doesn't
        elif player_bust == False and dealer_bust == True:
            payout = bet * -1
            return payout
        # player and dealer tie
        elif player_score == dealer_score:
            payout = 0
            return payout
        # player wins
        elif player_score > dealer_score:
            payout = bet * -1
            return payout
        # dealer wins
        elif player_score < dealer_score:
            payout = bet
            return payout
        else:
            return 'Error'

    def blackjack_payout_function(self, blackjack_player, blackjack_dealer, bet, blackjack_payout_ratio):
        # player gets blackjack
        if blackjack_player == True and blackjack_dealer == False:

            payout = bet * -1 * blackjack_payout_ratio
            return payout

        # dealer gets black jack
        elif blackjack_player == False and blackjack_dealer == True:

            payout = bet
            return payout

        # push
        elif blackjack_player == True and blackjack_dealer == True:

            payout = 0
            return payout

        # no blackjacks
        else:
            return None

class Dealer_strategy(Payout):

    def __init__(self):
        
        pass
    
    def dealer_strategy(self, deck, dealer_cards):

        card_count = self.card_score(dealer_cards)

        while card_count < 17:
            self.hit(deck, dealer_cards)
            card_count = self.card_score(dealer_cards)

        return dealer_cards
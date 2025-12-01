import random
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn as sns
from blackjack_utils import Dealer
from blackjack_utils import Strategy
from blackjack_utils import Dealer_strategy
from blackjack_utils import Payout

'''INSTANTIATE CLASSES'''
deck1 = Dealer()
strategy = Strategy(-25, 1.2, 300, -12.5)
dealer = Dealer_strategy()
payout_calc = Payout()

'''GLOBAL VARIABLES'''
bet = -50
blackjack_payout_ratio = 1.5
initial_portfolio = 300 # for house edge calculation
portfolio = 300
surrender_loss = -25
portfolio_df = df = pd.DataFrame([{'Payout': 0, 'Portfolio_Value': 300, 'Win': 0, 'Loss': 0, 'Surrender': 0,
                                   'Blackjack': 0, 'Push': 0, 'Dealer_Cards':0, 'Player_Cards':0}])

'''LOAD STRATEGY'''
df = pd.read_csv('policy.csv')
df.columns = ['Index', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']    
df.set_index('Index', inplace=True, drop=True)

'''CREATE DECK'''   
mega_deck = []

for i in range(4500):
    single_deck = deck1.create_single_deck()
    # print(single_deck)

    multi_deck = deck1.create_multi_deck(single_deck)
    # print(multi_deck)

    shuffle = deck1.shuffle_deck(multi_deck)
    # print(shuffle)

    cut_deck = deck1.cut_deck(multi_deck)

    for i in cut_deck:
        mega_deck.append(i)

# print(f'first 20 cards in deck: {mega_deck[:20]}')

'''RUN MONTE CARLO SIMULATION'''
for monte_carlo_index, i in enumerate(range(100000)):
    
    if monte_carlo_index % 1000 == 0:
        print(f'iteration: {monte_carlo_index}')

    '''DEAL CARDS'''
    player_hand = []
    dealer_hand = []

    # add cards to empty hand lists
    player_hand = deck1.deal_card(mega_deck, player_hand)
    dealer_hand = deck1.deal_card(mega_deck, dealer_hand)
    player_hand = deck1.deal_card(mega_deck, player_hand)
    dealer_hand = deck1.deal_card(mega_deck, dealer_hand)

    # create dictionary for player hand, decisions, and associated bet
    hand_and_strategy_dict = {}
    hand_and_strategy_dict['player hand'] = player_hand
    decision = strategy.get_strategy_decision(player_hand, dealer_hand, df)
    hand_and_strategy_dict['decision'] = decision
    hand_and_strategy_dict['bet'] = bet

    # create list for all player hands and decisions dictionaries (in case of split)
    player_hands_list = []
    player_hands_list.append(hand_and_strategy_dict)
    
    # print(f'dealer hand: {dealer_hand}')
    # print(f'player hand dict: {player_hands_list}')
    # print(f'first 20 cards in deck: {mega_deck[:20]}')

    '''RUN STRATEGY'''

    # check for surrender
    if player_hands_list[0]['decision'] == 'SU':
        player_hands_list[0]['bet'] = surrender_loss
        # print(f'surrender: {player_hands_list}')

    # for each player hand and decision (enumerate is for indexing)
    for index, player_dict in enumerate(player_hands_list):

        # decision iteration
        decision = player_dict['decision']
        # print(f'decision iteration: {decision}')
            
        # while EACH decision is not stand or surrender
        while decision != 'S' and decision != 'SU' and decision != 'Bust':

            # split
            if decision == 'P':
                
                # player hand for this iteration
                player_hand_iteration = player_dict['player hand']
                        
                # split player hands in 2 lists
                split_hand_1 = []
                split_hand_1.append(player_hand_iteration[0])
                split_hand_2 = []
                split_hand_2.append(player_hand_iteration[-1])

                # automatically hit each split
                strategy.hit(mega_deck, split_hand_1)
                strategy.hit(mega_deck, split_hand_2)
                # print(f'new hands: {split_hand_1, split_hand_2}')

                # get decision for each split
                decision_1 = strategy.get_strategy_decision(split_hand_1, dealer_hand, df)
                decision_2 = strategy.get_strategy_decision(split_hand_2, dealer_hand, df)
                # print(f'new decisions: {decision_1, decision_2}')

                # with an ace split, you are only dealt 1 card
                if player_hand_iteration == ['A', 'A']:
                    decision_1 = 'S'
                    decision_2 = 'S'

                # change original hand to null so we can delete it after the loop (in order to not disrupt the loop iteration)
                player_hands_list[index]['decision'] = None

                # add new hands and decisions to player_hands_list
                new_hand_dict_1 = {}
                new_hand_dict_2 = {}

                new_hand_dict_1['player hand'] = split_hand_1
                new_hand_dict_2['player hand'] = split_hand_2
                
                new_hand_dict_1['decision'] = decision_1
                new_hand_dict_2['decision'] = decision_2

                new_hand_dict_1['bet'] = bet
                new_hand_dict_2['bet'] = bet

                player_hands_list.append(new_hand_dict_1)
                player_hands_list.append(new_hand_dict_2)
                # print(player_hands_list)

                break

            if decision == 'H':

                # get player hand for this iteration
                player_hand_iteration = player_dict['player hand']
                # hit hand iteration
                strategy.hit(mega_deck, player_hand_iteration)
                # get decision
                decision = strategy.get_strategy_decision(player_hand_iteration, dealer_hand, df)
                # update player hand and decision
                player_dict['player hand'] = player_hand_iteration
                player_dict['decision'] = decision

                # print(f'player dict: {player_dict}')

            # cannot surrender after hit
            if decision == 'SU':
                
                # if decision is surrender after a hit, you stand instead
                decision = 'S'
                break

            if decision == 'D':
                
                # get player hand for this iteration
                player_hand_iteration = player_dict['player hand']
                # hit hand iteration
                strategy.hit(mega_deck, player_hand_iteration)
                # double bet
                player_dict['bet'] = player_dict['bet'] * 2
                # update player hand and decision
                player_dict['player hand'] = player_hand_iteration
                player_dict['decision'] = 'S'
                break

    '''CHECK FOR SURRENDER'''
    if player_hands_list[0]['decision'] == 'SU':
        payout = player_hands_list[0]['bet']
        # print('surrender')
        portfolio += payout
        # print(f'portfolio: {portfolio}')
        # print(f'payout: {payout}')

        temp = pd.DataFrame([[payout, portfolio, 0, 0, 1, 0, 0]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
        portfolio_df = pd.concat([portfolio_df, temp])
        continue

    '''RUN DEALER STRATEGY'''
    dealer_cards = dealer.dealer_strategy(mega_deck, dealer_hand)
    # print(f'dealer cards: {dealer_hand}')

    '''CHECK FOR BLACKJACK'''
    # we only need the first hand to verify if there was a blackjack, so we will not loop through all hands
    # check if first hand decision is None type - if so, there was a split, and you cannot have a blackjack
    if player_hands_list[0]['player hand'] == None:
        print('cannot have blackjack after split')
        # break
        
    else:
        # check if player or dealer have blackjack
        blackjack_player = payout_calc.blackjack_value(player_hands_list[0]['player hand'])
        blackjack_dealer = payout_calc.blackjack_value(dealer_hand)
        
        # print(f' blackjack player: {blackjack_player}')
        # print(f' blackjack dealer: {blackjack_dealer}')

        blackjack_payout_value = payout_calc.blackjack_payout_function(blackjack_player, blackjack_dealer, bet, blackjack_payout_ratio)

        # print(f'blackjack payout value: {blackjack_payout_value}')

        # no blacjack -> do nothing
        if blackjack_payout_value == None:
            pass
        
        # calc payout if blackjack
        else:
            payout = blackjack_payout_value
            portfolio += blackjack_payout_value
            # print('blackjack')
            # print(payout)
            # print(portfolio)
            if payout == 0:
                temp = pd.DataFrame([[payout, portfolio, 0, 0, 0, 0, 1]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
                portfolio_df = pd.concat([portfolio_df, temp])

            if payout > 0:
                temp = pd.DataFrame([[payout, portfolio, 1, 0, 0, 1, 0]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
                portfolio_df = pd.concat([portfolio_df, temp])

            if payout < 0:
                temp = pd.DataFrame([[payout, portfolio, 0, 1, 0, 0, 0]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
                portfolio_df = pd.concat([portfolio_df, temp])

            # go to next simulation iteration
            continue

    '''DELETE NULL HANDS (FROM SPLIT)'''
    player_hands_list = [x for x in player_hands_list if x['decision'] != None]
    # print(f'player hands list: {player_hands_list}')

    '''GET PAYOUT'''
    # loop through each player hand
    for dict in player_hands_list:

        # get player hand for this iteration
        player_hand_iteration = dict['player hand']
        bet_iteration = dict['bet']

        # get hand score
        player_score = payout_calc.card_score(player_hand_iteration)
        dealer_score = payout_calc.card_score(dealer_hand)
        # print(f'player score: {player_score}')
        # print(f'dealer score: {dealer_score}')

        # check for bust
        player_bust = payout_calc.bust(player_score)
        dealer_bust = payout_calc.bust(dealer_score)
        # print(f'player bust: {player_bust}')
        # print(f'dealer bust: {dealer_bust}')

        # compare scores
        payout = payout_calc.win_loss(player_score, dealer_score, player_bust, dealer_bust, bet_iteration)
        # print(payout)
        
        portfolio += payout
        # print(portfolio)

        if payout == 0:
            temp = pd.DataFrame([[payout, portfolio, 0, 0, 0, 0, 1]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
            portfolio_df = pd.concat([portfolio_df, temp])

        if payout > 0:
            temp = pd.DataFrame([[payout, portfolio, 1, 0, 0, 0, 0]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
            portfolio_df = pd.concat([portfolio_df, temp])

        if payout < 0:
            temp = pd.DataFrame([[payout, portfolio, 0, 1, 0, 0, 0]],
                                columns=['Payout', 'Portfolio_Value', 'Win', 'Loss', 'Surrender', 'Blackjack', 'Push'],
                                index=[monte_carlo_index])
            portfolio_df = pd.concat([portfolio_df, temp])

        # temp = pd.DataFrame([[dealer_hand, player_hands_list]],
        #                                 columns=['Dealer_Hand', 'Player_Hand'],
        #                                 index=[monte_carlo_index])
        # portfolio_df = pd.concat([portfolio_df, temp])

# portfolio_df.head()
# portfolio_df = portfolio_df.iloc[1:]

'''GENERATE GRAPHS'''
# portfolio value
plt.figure(figsize=(12,5))
plt.plot(portfolio_df['Portfolio_Value'])
plt.title('Portfolio Value')
plt.xlabel('Iteration')
plt.ylabel('Dollars ($)')
plt.tick_params(rotation=45)
# plt.show()
plt.savefig('simulation_output/portfolio_value.png')

# hand outcomes
fig, ax = plt.subplots()

data_name = ['Win', 'Loss', 'Surrender', 'Blackjack', 'Push']
win = portfolio_df['Win'].sum()
loss = portfolio_df['Loss'].sum()
surrender = portfolio_df['Surrender'].sum()
blackjack = portfolio_df['Blackjack'].sum()
push = portfolio_df['Push'].sum()
counts = [win, loss, surrender, blackjack, push]
data_label = ['Win', 'Loss', 'Surrender', 'Blackjack', 'Push']
bar_colors = ['tab:green', 'tab:red', 'tab:orange', 'tab:gray', 'tab:blue']

ax.set_facecolor('white')
ax.bar(data_name, counts, label=data_label, color=bar_colors)

ax.set_ylabel('Counts')
ax.set_title('Hand Outcome Counts')
ax.legend(title='Legend')

# plt.show()
plt.savefig('simulation_output/hand_outcomes.png')

# payouts
# plt.figure(figsize=(12,5))
# plt.plot(portfolio_df['Payout'])
# plt.title('Payouts')
# plt.xlabel('Iterations')
# plt.ylabel('Dollars ($)')
# plt.tick_params(rotation=45)
# plt.show()
# plt.savefig('simulation_output/payouts.png')

'''SUMMARY STATISTICS'''
# expected payout
expected_payout = portfolio_df['Payout'].mean()
print(f'Expected Payout: {expected_payout}')

# max drawdown
max_drawdown = portfolio_df['Portfolio_Value'].min()
print(f'Max Drawdown: {max_drawdown}')

# win/loss ratio
win_loss_ratio = portfolio_df['Win'].sum() / portfolio_df['Loss'].sum()
print(f'Win/Loss Ratio: {win_loss_ratio}')

# house edge
house_edge = -1 * ((initial_portfolio - portfolio_df['Portfolio_Value'].iloc[-1]) / (monte_carlo_index * bet)) * 100
print(f'House Edge: {house_edge}%')

# final portfolio value
final_portfolio_value = portfolio_df['Portfolio_Value'].iloc[-1]
print(f'Final Portfolio Value: {final_portfolio_value}')

# save results to csv
portfolio_df.to_csv('monte_carlo_results.csv')

# save final portfolio value to csv
final_portfolio_value = str(final_portfolio_value)
open('portfolio_value.csv', 'a').write(final_portfolio_value) 

# save summary statistics to csv
summary_statistics = pd.DataFrame([[expected_payout, max_drawdown, win_loss_ratio, house_edge, final_portfolio_value]],
                                columns=['Expected Payout', 'Max Drawdown', 'Win/Loss Ratio', 'House Edge', 'Final Portfolio Value'])
summary_statistics.to_csv('simulation_output/summary_statistics.csv')
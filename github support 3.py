import numpy as np
import random

def BlackJackStrategy(hand, dealer_card):
    hard_count=sum(hand)
    cards=len(hand)
    aces_count= 1*(1 in hand)
    soft_count=hard_count
    good_cards=[1,7,8,9,10]
    
    if cards<2:
        return 'Not enough cards'
    if hard_count<=11:
        soft_count= hard_count + 10*aces_count
    if cards==2 and soft_count==21:
        return 'Blackjack'
    if soft_count>=19:
        return 'Stay'
    if hand==[9,9] and dealer_card not in [1,7,10]:
        return 'Split'
    if hard_count>=17:
        return 'Stay'

    if cards>2:
        if hard_count==soft_count:
            if hard_count<=11:
                return 'Hit'
            if hard_count==12 and dealer_card <3:
                return 'Hit'
            if dealer_card in good_cards:
                return 'Hit'
            return 'Stay'
        if soft_count<=17:
            return 'Hit'
        if soft_count==18 and dealer_card in [1,9,10]:
            return 'Hit'
        return 'Stay'

    if cards==2:  
        if hand[0]==hand[1]:
            card= hand[0]
            if card==1:
                return 'Split'
            if card==8 and dealer_card!=1:
                return 'Split' 
            if card in [2,3,7] and dealer_card not in [1,8,9,10]:
                return 'Split'
            if card==6 and dealer_card not in [1,8,9,10]:
                return 'Split'
            if card==4 and dealer_card in [5,6]:
                return 'Split'
            
        if hard_count==soft_count:
            if hard_count==11 and dealer_card not in [1,10]:
                return 'Double'
            if hard_count==10 and dealer_card not in [1,10]:
                return 'Double'
            if hard_count==9 and dealer_card in [3,4,5,6]:
                return 'Double'
            if hard_count<=11:
                return 'Hit'
            if hard_count==12 and dealer_card <3:
                return 'Hit'
            if hard_count==16 and dealer_card in [7,8,9]:
                return 'Hit'
            if dealer_card in good_cards:
                return 'Hit'
            return 'Stay'
        
        if hard_count!=soft_count:           
            if soft_count==18:
                if dealer_card==6:
                    return 'Double'
                if dealer_card in [2,3,4,5,7,8]:
                    return 'Stay'
            if soft_count==17 and dealer_card in [2,3,4,5,6]:
                return 'Double'
            if soft_count==16 and dealer_card in [3,4,5,6]:
                return 'Double'
            if soft_count==15 and dealer_card in [4,5,6]:
                return 'Double'
            if soft_count in [13,14] and dealer_card in [5,6]:
                return 'Double'
            return 'Hit'

def blackjack_hand_result(bet=10, player_hand='q', dealer_card='q', hard_code= 4):
    #Deck of cards, 4 types of 10
    deck=np.array([1,2,3,4,5,6,7,8,9,10,10,10,10])
    
    #hard stay condition for split aces
    hard_stay=False

    #Creating a random hand if none is input
    if type(player_hand)==str:
        player_hand=[random.choice(deck), random.choice(deck)]

    #Turning on hard stay for split aces
    if player_hand==[1]:
        hard_stay==True
        
    #Adding a 2nd card to hand after splits    
    while len(player_hand)<2:
        player_hand.append(random.choice(deck))
        
    #Creating dealer card, and dealer cards
    if type(dealer_card)==str:
        dealer_card=random.choice(deck)
    dealer_cards=[dealer_card]

    #If hard stay condition is false
    if hard_stay==False:
        #Seeing if player hit blackjack        
        if BlackJackStrategy(player_hand, dealer_card) == 'Blackjack':
            
            #Seeing if casino also hit blackjack, in which case tie
            dealer_cards.append(random.choice(deck))
            if 1 in (dealer_cards):
                if sum(dealer_cards)==11:
                    return 0
            #Blackjack bonus, if any
            return bet*1.5

        if type(hard_code)== str:
            if hard_code=='Hit':
                player_hand.append(random.choice(deck))
                return blackjack_hand_result(bet, player_hand, dealer_card, hard_code= 4)
            if hard_code=='Double':
                if len(player_hand)==2:
                    player_hand.append(random.choice(deck))
                    bet= bet*2
                    if sum(player_hand)>21:
                        return 0 - bet
                else:
                    return 'Double Not Possible'
            if hard_code=='Split':
                if len(player_hand)==2: 
                    if player_hand[0]==player_hand[1]: 
                        res = blackjack_hand_result(bet=bet, player_hand=[player_hand[0]], dealer_card=dealer_card, hard_code= 'Split')
                        res+= blackjack_hand_result(bet=bet, player_hand=[player_hand[0]], dealer_card=dealer_card, hard_code= 'Split')
                        return res 
                    else:
                        return blackjack_hand_result(bet=bet, player_hand= player_hand, dealer_card=dealer_card)  
                else:
                    return blackjack_hand_result(bet=bet, player_hand=player_hand, dealer_card=dealer_card)
        else:
        #Seeing how often it says to 'hit'

            while BlackJackStrategy(player_hand, dealer_card) == 'Hit':
                #Adding one card for every hit
                player_hand.append(random.choice(deck))

                #Player loses bet if hand goes above 21
                if sum(player_hand)>21:
                    return 0- bet

                #If player Doubles

            if BlackJackStrategy(player_hand, dealer_card)=='Double':
                #He gets exactly one extra card and the bet size is doubled
                player_hand.append(random.choice(deck))
                bet= bet * 2
                if sum(player_hand)>21:
                    return 0- bet

                #If player Splits

            if BlackJackStrategy(player_hand, dealer_card)== 'Split':
                #Runs the sim twice, as different hands, slightly less variance than real life, but it's okay

                res= blackjack_hand_result(bet, [player_hand[0]], dealer_card) 
                res+= blackjack_hand_result(bet, [player_hand[0]], dealer_card)
                

                return res
        
        while True:
            #Plays out the blackjack hand from dealer's side
            
            #Give dealer extra card if loop hasn't broken
            dealer_cards.append(random.choice(deck))
            
            
            #Keep track of sum of dealer's cards
            dealer_score= sum(dealer_cards)
            
            #Keep track of soft score if dealer has an ace
            
            soft_score= dealer_score
            if dealer_score<=11 and 1 in dealer_cards:
                soft_score+=10
                
            #If dealer gets blackjack you lose even if you have 21
            if len(dealer_cards)==2 and soft_score==21:
                return 0-bet
                
            #Keeps track of player's score     
            player_score=sum(player_hand)
            
            #Uses soft score if that is better for player
            if player_score<=11 and 1 in player_hand:
                player_score+=10
                
            #Dealer stays on all 17s
            if soft_score>=17:
                #If dealer bust, player wins bet
                if soft_score>21:
                    return bet
                #If player has more than dealer, player wins bet
                if player_score>soft_score:
                    return bet
                #Tie means no money changes hands
                if player_score==soft_score:
                    return 0
                #If player has lower, player loses bet
                if player_score<soft_score:
                    return 0 - bet
    if hard_stay==True:
        
        #Plays out only dealer's side, as player has to stop after 1 card
        
        while True:

                #Give dealer extra card if loop hasn't broken
            dealer_cards.append(random.choice(deck))
            
            
            #Keep track of sum of dealer's cards
            dealer_score= sum(dealer_cards)
            
            #Keep track of soft score if dealer has an ace
            
            soft_score= dealer_score
            if dealer_score<=11 and 1 in dealer_cards:
                soft_score+=10
                
            #If dealer gets blackjack you lose even if you have 21
            if len(dealer_cards)==2 and soft_score==21:
                return 0-bet
                
            #Keeps track of player's score     
            player_score=sum(player_hand)
            
            #Uses soft score if that is better for player
            if player_score<=11 and 1 in player_hand:
                player_score+=10
                
            
            #Dealer stays on all 17s
            if soft_score>=17:
                
                #If dealer bust, player wins bet
                if soft_score>21:
                    return bet
                
                #If player has more than dealer, player wins bet
                if player_score>soft_score:
                    return bet
                
                #Tie means no money changes hands
                if player_score==soft_score:
                    return 0
                
                #If player has lower, player loses bet
                if player_score<soft_score:
                    return 0 - bet

def blackjack_sim(n_hands=1_00_000, player_h='q', dealer_c='q', bet=10, hard_c=4):
    pnl=0
    res=[]
    p=player_h
    q=len(player_h)
    for i in range(n_hands):
        pnl+= blackjack_hand_result(bet=bet, player_hand=p[:q], dealer_card=dealer_c, hard_code= hard_c)
        
    return pnl

#Simulates a million hands to estimate house edge
house_edge=-100*(blackjack_sim(n_hands=1_00_000, bet=1) / 1_00_000)
print(house_edge) #percentage
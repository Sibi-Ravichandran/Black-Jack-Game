# Title:        Black Jack Game 
# Description:  Black Jack Game between a computer and a player. 
# Author:       Sibi Ravichandran
# Date:         09-June-2020

import random

# Global variables: tuples with suits and ranks and dictionary with corressponding values: 
suits = ('Hearts', 'Diamonds', 'Spade', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven' , 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# Variable that says the game is on or not:
game_on=True

# Class Card that contains all the attributes of the card: 
class card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank 
        
    def __str__(self):
        return self.rank+" of "+self.suit
     
# Building a deck of cards:     
class deck():
    
    def __init__ (self):
        self.deck = [ ]
        for suit in suits:
            for rank in ranks: 
                self.deck.append(card(suit,rank)) 
                
    def __str__ (self):
        deck_comp = ''
        for card in self.deck: 
            deck_comp += '\n'+ card.__str__() 
        return "The deck has: "+deck_comp
           
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# Class hand to calculate the value of cards at any time in hand:         
class hand:
    
    def __init__(self):
        self.card = []
        self.value=0
        self.aces=0
        
    def add_card (self,card):
        self.card.append(card)
        self.value+=values[card.rank]
        #track aces 
        if card.rank == 'Ace':
            self.aces+=1
        
    # if total value is greater than 21 and if we have aces we have to treat value of aces as 1 and not 11. 
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value-=10
            self.aces-=1

# class chip to keep track of player's starting chip, bets and ongoing wins. 
class chips:

    def __init__(self,total=100):
        self.total=total
        self.bet=0
        
    def win_bet(self):
        self.total+=self.bet 
        
    def lose_bet(self):
        self.total-=self.bet         
       
def take_bet(chips):
        
    while True:
        try:
            chips.bet=int(input("How many chips would you like to bet?"))
        except:
            print ("Sorry provide an integer")
        else: 
            if chips.bet > chips.total:
                print ("Sorry, your bet can't exceed", chips.total)
            else: 
                break
                
                
def hit (deck,hand):
    single_card=deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    
def hit_or_stand (deck,hand):
        
        global game_on
        
        while True:
            x=input("Hit or Stand? Enter h or s:  ")         
            if x[0].lower()=='h':
                hit(deck,hand)
            elif x[0].lower() == 's':
                print ("Player stands dealer's turn") 
                game_on= False 
            else:
                print ("Sorry please enter h or s only!")
                continue
                
            break
                
def player_busts (player,dealer,chips):
    print ("BUST PLAYER!")
    chips.lose_bet()


def player_wins (player,dealer,chips):
    print ("PLAYER WINS!")
    chips.win_bet()


def dealer_busts (player,dealer,chips):
    print ("PLAYER WINS! DEALER BUSTED! ")
    chips.win_bet()

def dealer_wins (player,dealer,chips):
    print ("DEALER WINS!")
    chips.lose_bet()

def push (player,dealer):  
    print ("Dealer and Player tie!")
    
def show_some (player, dealer):
    print ("Dealers hand: ")
    print ("One card Hidden!" )
    print (dealer.card[1])
    print ("\n")
    print ("Players hand: ")
    for card in player.card:
        print (card) 
        
def show_all (player, dealer): 
    print ("Dealers hand: ")
    for card in dealer.card:
        print (card) 
    print ("\n")
    print ("Players hand: ")
    for card in player.card:
        print (card)     

while True: 

    print ('#######################')
    print ('Welcome to BLACK JACK!')
    print ('#######################')   

    # Creating and Shuffling deck, deal two cards to each player.
    mydeck=deck()
    mydeck.shuffle() 
    
    # Creating hand for player
    player_hand=hand()
    player_hand.add_card(mydeck.deal())
    player_hand.add_card(mydeck.deal())
    
    #Creating hand for dealer 
    dealer_hand=hand()
    dealer_hand.add_card(mydeck.deal())
    dealer_hand.add_card(mydeck.deal())
           
    #Setting up the player's chips 
    player_chips = chips()
    
    # prompting player to take bet 
    take_bet(player_chips)
    
    # Show cards - but keep one dealer card hidden: 
    show_some(player_hand, dealer_hand)
    
    while game_on:
        
        # prompt the player to hit or stand: 
        hit_or_stand (mydeck, player_hand) 
         
        # show cards (keep one dealer card hidden) 
        show_some(player_hand,dealer_hand)
        # if the player_hand exceeds 21, run player_busts() and break out of the loop 
        if player_hand.value>21:
            player_busts(player_hand,dealer_hand,player_chips)
            break 
            
    # if player hasnt busted, play dealer's hand until dealer reaches 17 
    if player_hand.value <=21: 
        while dealer_hand.value < player_hand.value: 
        # instead of player_hand.value we can have 17 if we want soft 17 rule 
            hit(mydeck,dealer_hand)
        
        #show all cards 
        show_all (player_hand, dealer_hand)
        
        # Run different winning scenarios: 
        if dealer_hand.value > 21:
            dealer_busts (player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins (player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins (player_hand, dealer_hand, player_chips)
        else:
            push (player_hand, dealer_hand)
            
    # Inform player of their remaining chips 
    print ("\nThe total chips the player have is : " +str(player_chips.total))
    
    # Ask for a replay 
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    if new_game[0].lower()=='y':
        game_on=True
        continue
    else:
        print("Thanks for playing!")
        break


###########################################################################################################################        
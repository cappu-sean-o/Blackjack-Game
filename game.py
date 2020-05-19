import random
import time
from libdw import sm

# A class which contains functions used to
# draw on screen graphics and text in the
# terminal emulator in which the game is run
class graphics():
    def __init__(self):
        self.suits = {
            'Diamonds':'♦',
            'Clubs':'♣',
            'Hearts':'♥',
            'Spades':'♠'
            }
    
    def draw_cards(self,cards,name):
        output = " {0:s}'s Cards:\n".format(name)
        for i in range(9):
            for j in range(len(cards)):
                if i == 0 or i == 8:
                    output +=' +-----------+'
                    if j == len(cards)-1 and i == 0:
                        output += '\n'
                elif i == 1:
                    output +=' | {0:10s}|'.format(cards[j]['rank'])
                    if j == len(cards)-1:
                        output += '\n'
                elif i == 2:
                    output +=' | {0:10s}|'.format(self.suits[cards[j]['suit']])
                    if j == len(cards)-1:
                        output += '\n'
                else:
                    output +=' |           |'
                    if j == len(cards)-1:
                        output += '\n'
        print(output)
        return None
    
    def draw_banner(self):
        banner =  ' +---------------------+\n'
        banner += ' | B L A C K   J A C K |\n'
        banner += ' |    (Press Enter)    |\n'
        banner += ' +---------------------+'
        input(banner)
        return True
    
    def player_setup(self):
        return input(' Enter Name: ')

    def draw_win(self):
        banner =  ' +---------------------+\n'
        banner += ' |                     |\n'
        banner += ' |       You Win!      |\n'
        banner += ' |                     |\n'
        banner += ' +---------------------+'
        print(banner)

    def draw_tie(self):
        banner =  ' +---------------------+\n'
        banner += ' |                     |\n'
        banner += ' |     Its A Tie...    |\n'
        banner += ' |                     |\n'
        banner += ' +---------------------+'
        print(banner)
    
    def draw_lose(self):
        banner =  ' +---------------------+\n'
        banner += ' |                     |\n'
        banner += ' |      You Lose...    |\n'
        banner += ' |                     |\n'
        banner += ' +---------------------+'
        print(banner)
    
    def draw_prompt(self):
        while True:
            prompt = input(' Draw card? (hit/stay) ')
            if prompt == 'hit' or prompt == 'stay':
                return prompt

    def draw_dealer_drawing(self):
        print(" Dealer's hand is less than 17, drawing...")
    
    def draw_dealer_bust(self):
        banner =  ' +---------------------+\n'
        banner += ' |     Dealer  Bust    |\n'
        banner += ' |       You Win!      |\n'
        banner += ' +---------------------+'
        print(banner)

    def draw_blackjack(self):
        banner =  ' +---------------------+\n'
        banner += ' |      Blackjack!     |\n'
        banner += ' |       You Win!      |\n'
        banner += ' +---------------------+'
        print(banner)
    
    def draw_bust(self):
        banner =  ' +---------------------+\n'
        banner += ' |         Bust        |\n'
        banner += ' |      You Lose...    |\n'
        banner += ' +---------------------+'
        print(banner)
    
    def draw_dealing(self):
        banner =  ' +---------------------+\n'
        banner += ' |                     |\n'
        banner += ' |   Dealing Cards...  |\n'
        banner += ' |                     |\n'
        banner += ' +---------------------+'
        print(banner)

    def draw_restart(self):
        while True:
            prompt = input(' Restart? (yes/no) ')
            if prompt == 'yes':
                return True
            elif prompt == 'no':
                return False
ui = graphics()

# A State Machine that tracks the state of the
# deck and allows cards to be drawn from it.
class card_deck_shuffled(sm.SM):
    def __init__(self):

        # Open and file containing cards
        # and store each entry as an element
        # in the list
        f = open('cards','r')
        cards = [] #initialise list variable
        for i in f.readlines():
            rank = i.split(' ')[0] 
            suit = i.split(' ')[1][:-1]
            cards.append({'rank':rank,'suit':suit})
        f.close()

        # Shuffle cards in the deck
        random.shuffle(cards)

        # Set start state of State Machine
        self.start_state = cards 

    def get_next_values(self,state,inp):

        # Allow cards to be drawn if there
        # are sufficient cards in the deck
        if len(state) >= 0 and len(state) >= inp:
            drawn_cards = state[:inp]
            output_state = state[inp:]
            return output_state,drawn_cards
        elif len(state) == 0:
            return state,'Deck Empty'
        else:
            return state,'Invalid'

# A function that tracks calculates the value
# of a hand given the cards of the hand. It
# sets the value of Ace to be 1 or 11
# whichever is more favourable to the hand
def hand_calculate(cards):

    hand = 0

    # Calculate the value of the hand
    for i in cards:
        if i['rank'].isdigit():
            hand += int(i['rank'])
        elif i['rank'] == 'Ace':
            hand += 11
        else:
            hand += 10
    
    # Recalculates the value of the hand using
    # a value of 1 for Ace if the hand will 
    # bust (higher than 21) when using the 
    # value of 11 for Ace Card
    if hand > 21:
        hand = 0
        for i in cards:
            if i['rank'].isdigit():
                hand += int(i['rank'])
            elif i['rank'] == 'Ace':
                hand += 1
            else:
                hand += 10

    return hand

# A State Machine that tracks the hand of a
# player and allows the player to receive cards
# which are added to the hand
class player(sm.SM):
    def __init__(self,inp=''):
        self.name = inp
        self.start_state = []
    def get_next_values(self,state,inp):
        state += inp
        return state, state

# This is the main logic of the game.
# A State Machine whose states are the current 
# state of the game. It has no output other 
# than a boolean value that allows a while 
# loop to call blackjack_game.step()
class blackjack_game(sm.SM):
    def __init__(self):
        ui.draw_banner()
        self.start_state = 'game setup'
    
    def get_next_values(self,state,inp):
        
        # Start the deck State Machine and
        # the dealer which is an instance of
        # the player State Machine
        if state == 'game setup':
            self.deck = card_deck_shuffled()
            self.deck.start()
            self.dealer = player("Dealer")
            self.dealer.start()

            return 'player setup',True

        # Creates and starts a player instance
        elif state == 'player setup':
            self.player1 = player(ui.player_setup())
            self.player1.start()

            return 'game start',True

        # Deals 2 cards to the player and the
        # dealer each
        elif state == 'game start':
            ui.draw_dealing()
            self.player1.step(self.deck.step(2))
            self.dealer.step(self.deck.step(2))
            time.sleep(1)

            #display player's cards
            ui.draw_cards(self.player1.state,self.player1.name)
            time.sleep(1)

            #display dealer's first card
            ui.draw_cards(self.dealer.state[:1],self.dealer.name)

            return 'hand checking',True

        # Checks if the value of the player's hand
        # has gone over 21 (bust) and ends the game
        # if it is
        elif state == 'hand checking':
            if hand_calculate(self.player1.state) > 21:
                ui.draw_bust()
                return 'game ended',True
            
            elif hand_calculate(self.player1.state) == 21:
                ui.draw_blackjack()
                return 'game ended',True
            
            else:
                return 'card drawing',True
        
        # Prompts the player if they want to draw
        # another card to raise the value of their hand
        elif state == 'card drawing':
            r = ui.draw_prompt()
            
            if  r == 'hit':
                self.player1.step(self.deck.step(1))

                ui.draw_cards(self.player1.state,self.player1.name)

                return 'hand checking',True

            elif r == 'stay':
                return 'dealer card reveal',True

        # Reveals the full hand of the dealer after
        # the player has finished drawing their cards
        elif state == 'dealer card reveal':
            ui.draw_cards(self.dealer.state,self.dealer.name)
            
            # If the dealer's hand has a value greater than
            # 21, the dealer busts and the player wins
            if hand_calculate(self.dealer.state) > 21:
                ui.draw_dealer_bust()

                return 'game ended',True
            
            # If the dealer's hand has a value lower than
            # 17, they must draw until the value of their 
            # hand is at least 17
            elif hand_calculate(self.dealer.state) < 17:
                return 'dealer hit',True
            
            else: 
                return 'judging',True

        # Dealer draws a card
        elif state == 'dealer hit':
            while hand_calculate(self.dealer.state) < 17:
                ui.draw_dealer_drawing()
                time.sleep(0.5)
                self.dealer.step(self.deck.step(1))

            return 'dealer card reveal',True

        # Compares the value of the players hand and
        # the dealers hand to see if the player wins
        elif state == 'judging':
            if hand_calculate(self.player1.state) > hand_calculate(self.dealer.state):
                ui.draw_win()
            elif hand_calculate(self.player1.state) == hand_calculate(self.dealer.state):
                ui.draw_tie()
            elif hand_calculate(self.player1.state) < hand_calculate(self.dealer.state):
                ui.draw_lose()
            
            return 'game ended',True
        
        # Allow the player to choose if they want to
        # play another round
        elif state == 'game ended':
            if ui.draw_restart():
                return 'game setup',True
            else:
                return 'quit',False


# Create an instance of the game an initialise it
game = blackjack_game()
game.start()

# Game will run as long as the State Machine outputs True
# else the program will execute to the end and exit
s = True
while s:
    s = game.step(None)
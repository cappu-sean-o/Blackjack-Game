# Terminal Emulator Based Blackjack

## About

This is a Blackjack game implemented in python incorporating the state machine class `sm` from `libdw` 

Blackjack is a card game in which the objective is to draw cards and beat the dealer in hand value and to reach a hand value of 21

Watch a playthrough here : https://youtu.be/VJLbEvWrnXI

Credits:

+ Director: Sean Yeo

+ Written by: Sean Yeo

+ Game art by: Sean Yeo

A Sean Yeo game

### Dependencies

These are the python libraries needed to run the game

+ `libdw`
  + The game makes heavy use of the state machine class `sm` from this library
+ `time`
  + Used to delay game actions to prevent the game from being too fast paced
+ `random` 
  + This is used to shuffle the deck of virtual cards

## Rules

This game follows the basic rules of blackjack:

+ Winning Conditions
  1. By having a hand value greater than the dealer's hand value at the end of the round
  2. By having a hand value of 21 before the dealer does, a.k.a **Blackjack**
  3. The dealer has a hand value greater than 21
+ Losing Conditions
  1. By having a hand value greater than 21, a.k.a **Bust**
  2. By having a hand value smaller than the dealer's hand value at the end of the round

+ Other Rules
  1. The hand value of a card is the sum of the values of all the cards in the players hand
  2. The value of numbered cards (2 to 10) is the number on the card
  3. The value of face cards (King, Queen, Jack) is 10
  4. The value of an Ace card is either 1 or 11 depending on which is most favorable to the hand
     + By default the value of an Ace card is 11
     + It will become 1 if the hand value exceeds 21 when calculating the hand value using the default value of Ace to prevent the hand from going over 21 (bust)

## How to play

1. The deck will be shuffled and the player will be dealt 2 cards. Both cards will be exposed
2. The dealer also gets 2 cards, however only one will be exposed with the other card's value hidden
3. The player will be allowed to choose if they want to draw another card to increase the value of their hand based on the information they have about the dealer's hand, a.k.a **Hit**
4. The player will be allowed to draw as many cards as they want, however if the next card drawn by the player causes their hand value to rise above 21, they lose (Bust)
5. When the player is satisfied with the value of their hand, they can signal that they do not wish to draw anymore cards, a.k.a **Stay**
6. The dealer will now expose the hidden card to show their full hand. If the hand value of the dealer is less than 17, they are required to draw cards until their hand value is 17 or greater
7. If the dealer draws a card that causes their hand value to rise above 21, the dealer busts and the player wins
8. Once the dealer has finished drawing their cards, the hand values are compared and the player wins if they have a higher hand value
9. If both have the same value, it is a tie and no one wins

## Description of code

The code is generally separated into 4 main components:

+ `blackjack_game()`
+ `card_deck_shuffled()`
+ `player()`
+ `graphics()`

This is done in order to provide a greater level of organization in the code, making it more understandable and easier to debug. It also attempts to separate out the code into 3 components:

+ Core Game logic
+ Game data
+ User interaction 

#### Core Game Logic

The class `blackjack_game` is the main component of the code which comprise the logic of the game. It is a state machine that is a subclass of `sm.SM` from `libdw` which models a game of Blackjack according to common rules of Blackjack The main states of this state machine are:

+ game setup
  + In this state, an object `deck` of class `card_deck_shuffled` and an object `dealer` of class `player()` is created and started. Both of these classes are state machines and are a subclass of `sm.SM` 
  + This state always transitions into the 'player setup' state
+ player setup
  + In this state, a second instance of the `player()`class, `player1` is created. It then draws an on screen prompt which allows the player to enter their name.
  + This state always transitions into the 'game start' state
+ game start
  + The state machines `player1` and `deck` are stepped advanced by 1 step, with the output of `deck` being passed to the input of `player1` . This is equivalent to a player drawing a card from a deck in real life
  + This occurs a second time but this time for the `dealer` and `deck` state machines this time and serves a similar purpose as before
  + The game will then show the players cards and then one of the dealer's cards
  + This state always transitions to the the 'hand checking' state
+ hand checking
  + When in this state, the logic checks if the value of the users hand value is 21 or above.
    + If the user's hand value  is 21 or above, the player wins or loses respectively and the state machine goes to the 'game ended' state
    + If the user's hand value is lower than 21, the state machine goes to the 'card drawing' state
+ card drawing
  + In this state, the state machine prompts the player if they want to draw another card
  + The player may choose to draw another card (hit) or to pass (stay)
    + If the player chooses to draw, the state machine will go back to the 'hand checking' state
    + If the player chooses not to draw, the state machine will go to the 'dealer card reveal' state
+ dealer card reveal
  + The full hand of the dealer will be revealed (previously only 1 card was revealed)
  + There are 3 possible state transitions at this point
    + If the dealer's hand has a value lesser than 17, the state machine will go into the 'dealer hit' state
    + If the dealer's hand has a value between 17 and 21 inclusive, the state machine will go to the 'judging' state
    + If the dealer's hand has a value above 21, the player wins and the state machine goes to the 'game ended' state
+ dealer hit
  + At this state, the `dealer` state machine and `deck` state machine will be stepped until the value of the dealers hand is 17 or above. This is equivalent to the dealer of the real life blackjack game hitting until his hand value is 17 or above
  + This state will always transition back to the 'dealer card reveal' state
+ judging
  + The values of the player's and and the dealer's hands are compared
    + If the player's hand is higher, the player wins
    + If the player's hand is lower, the player loses
    + If the player's hand and the dealer's hand is tied, neither wins
  + This state always transitions to the 'game ended' state
+ game ended
  + At this state, the player is prompted if they would like to play another round
    + If the player chooses to play again, the state machine transitions to the 'game setup' state
    + If the player chooses not to play again, the state machine outputs a `False` . This is the only point at which the state machine will output a `False`, at all other times it will output a `True` when stepped in order to signify that the game is still in progress and to continue the while loop which continually progresses the state machine.

Other components of the core game logic include the function `hand_calculate` which is a function that calulates the value of a given number of cards passed into the function as a list of dictionaries which is described inthe following section

#### Game Data

The state machine classes `card_deck_shuffled()` and  `player()` are the 2 main components that keep track of Game Data.

The main data of the game is the cards which are held either in the players hands or the deck. The cards are represented as dictionaries, each dictionary has 2 key value pairs and represents a card in the deck in the format using the keys 'rank' and 'suit' where their corresponding values are the value of the card (Ace,2,3 etc) and the suit being one of the 4 suits: Diamonds, Clubs, Hearts, Spades. For example, an Ace of Spades would be represented as `{'rank':'Ace','suit':'Spades'}`. However cards are always passed between functions as a list of dictionaries. This allows for more than one card to be passed at a time

The state of `card_deck_shuffled()` is a list containing the dictionaries representing each card. Each time the state machine is stepped, it accepts an integer as input which tells the state machine how many cards to output. Those cards from the top of the deck which in this case, is the start of the list of dictionaries. It returns a slice of the original state without the cards that were removed as its next state and outputs a list containing those cards. Additionally, the data containing the cards is stored in a text file in the same directory as the main game.py file and is read and parsed when `__init__` function of the class is called.

The state of `player()` is a list of dictionaries as well and represents the current state of a players hand. The `player()` state machine accepts inputs and outputs its current state. Usually the output of an instance of `card_deck_shuffled()` is passed into the input of an instance of `player()` which in this game is the `dealer` and `player1`. Each time an instance of `player()` is stepped, it takes the input and adds it to its state. 

#### User Interaction

The main component of the code that handles the user interaction is the `graphics()` class. This class contains the functions used for drawing various banners and prompts on screen. Other eye candy can easily be added to this class as well. The functions used to write on screen prompt also handle user input as well, allowing user input errors to be rejected.  
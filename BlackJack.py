# Importing modules and files
from Cards import pack_of_cards
from Cards import pack_of_cards_untouched
from TitleArt import title_art
from Rules import rules
import random
import copy
import sys
import time

# Creating a deep copy of the pack of cards to use and modify without modifying the original
cards = copy.deepcopy(pack_of_cards)
# Creating a container (list) to hold dealers cards
dealers_cards = []


# Function to type print statements letter by letter
def type_fast(string):
    """Types char by char instead of all at once like a print statement"""
    for letter in string:
        print(letter, end='')
        sys.stdout.flush()
        time.sleep(0.02)
    print('\n')


# Function to retrieve a random dict key from a pack of cards (a random card)
def get_one_card():
    """return a random dict key from dict cards and then pop the value from dict cards"""
    # Getting the random card
    card = random.choice(list(cards))
    # Removing that card from the pack of cards
    cards.pop(card)
    # Returning the card to be used elsewhere
    return card


# Function to get the dealers card value total
def get_dealers_total():
    """Returns the dealers total"""
    total = 0
    # Iterating through dealers cards and adding the value of that card (which it finds in the dictionary) and adds
    # it to the total
    for index in dealers_cards:
        total += pack_of_cards_untouched.get(index)
    return total


# Function to give the dealer two random cards from a pack of cards (two dict keys)
def give_dealer_first_cards():
    """Adds two random keys (cards) from the dict cards to dealers cards and removes them from the dict cards"""
    # Retrieving card 1
    card1 = get_one_card()
    # Adding it to dealers_cards
    dealers_cards.append(card1)
    # Retrieving card 2
    card2 = get_one_card()
    # Adding it to dealers_cards
    dealers_cards.append(card2)


# Function to make the dealer hit if his card value total is less than 15
def dealers_play():
    """Adds more random keys (cards) from dict cards until the dealers total is more than 15"""
    # Making the list dealers_cards accessible in the function using global
    global dealers_cards
    # Setting the dealers_cards list to empty
    dealers_cards = []
    # Filling the list with two random cards
    give_dealer_first_cards()
    # Using a while loop to keep adding random cards until the dealers total is more than 15
    while get_dealers_total() < 15:
        dealers_cards.append(get_one_card())
    return


# Function to ask the user how much they would like to bet in chips
def bet_chips():
    """Asks the user how many chips they would like to bet and if they enter more than they have it will ask them to
    renter. Returns the users input as an int"""
    # Asking the user to input the amount of chips they would like to bet for this round
    chip_bet = int(input('How many chips would you like to bet? \nChips: '))
    # Using a while loop to check the user did not enter an amount more than they have
    while chip_bet > user1.chips:
        type_fast('\nSorry you do not have that amount of chips. Please try again\n')
        chip_bet = int(input('How many chips would you like to bet? \nChips: '))
    print('\n')
    # Returning what the user entered
    return chip_bet


# Function to check if the users card value total is equal to 21
def blackjack_check():
    """Checks if users total is exactly 21"""
    if user1.total == 21:
        type_fast('BLACKJACK!!! You win')
        # Updating users chips to be there original chips plus what they bet
        user1.chips += user1.chips_bet
        # Showing the user how many chips they now have
        type_fast(f'You now have {user1.chips} chips')
        type_fast('\n')
        return True


# Function to check if the users cards value total is over 21
def bust_check():
    """Checks if users total is over 21"""
    if user1.total > 21:
        type_fast('You bust')
        # Updating users chips to be there original chips minus what they bet
        user1.chips -= user1.chips_bet
        # Showing the user how many chips they now have
        type_fast(f'You now have {user1.chips} chips')
        type_fast('\n')
        return True


# Function that asks the user if they would like to hit or stick
def dealers_question(turns):
    """Asks the user if they would like to hit or stick and returns the users answer"""
    # Asking the user if they would like to hit or stick
    type_fast('\nWould you like to hit or stick?')

    # If it is there first turn they will receive a more detailed description of what to enter
    if turns == 0:
        answer = (input('Enter \"h\" for hit or \"s\" for stick: '))
        # Using a while loop to check if they entered a valid option
        while answer != 'h' and answer != 's':
            type_fast('Invalid input')
            answer = (input('Enter \"h\" for hit or \"s\" for stick: '))
        return answer

    else:
        answer = (input('(h/s) '))
        while answer != 'h' and answer != 's':
            type_fast('Invalid input')
            answer = (input('(h/s) '))
        return answer


# Function to create the beginning of the application
def application_beginning():
    """Runs the first part of the application"""

    # Checking if the user hit 21 with there first two cards
    if blackjack_check():
        return

    # Creating a nested if statement to carry on asking them if they want to hit or stick if they haven't already stuck
    if hit(user1.users_cards, 0, user1.chips, user1.chips_bet, user1.total) is True:
        if hit(user1.users_cards, 1, user1.chips, user1.chips_bet, user1.total) is True:
            if hit(user1.users_cards, 2, user1.chips, user1.chips_bet, user1.total) is True:

                # Checking if the user has gone bust and if not they would have won the round with 5 cards
                user1.update_total()
                bust_check()
                type_fast('\nYou have automatically won since you hold 5 cards with a total less than 22!!!')
                # Updating the users chips
                chips = user1.chips_bet + user1.chips
                user1.update_chips(chips)
                # Showing the user their chip total
                type_fast(f'You now have {user1.chips} chips\n')
                # Running the application again
                user1.reset_total(0)
                application()


# Function to make action on the input of the dealers question (hit or stick?)
def hit(user_cards, turns, user_chips, user_bet_chips, user_total):
    """If the user has entered 'h' to the dealers question this function will add a random card/key from dict cards
    to the users cards and display the users cards including the total value of their cards. Else if the user entered
    's' it will check who won out of the dealer and user and print a display showing who won"""

    # Using an if statement to add a random card to users_cards if they entered "h" for hit
    if dealers_question(turns) == 'h':
        hit_card = get_one_card()
        user_cards.append(hit_card)
        type_fast(f'\nThe dealer dealt you a [{hit_card}]')

        # Showing the user their cards and total value
        if turns == 0:
            type_fast(f'\nYou now have the [{user1.users_cards[0]}], [{user1.users_cards[1]}] and the '
                      f'[{user1.users_cards[2]}]')
            user1.update_total()
            type_fast(f'That brings you to {user1.total}')
            # Checking if the user bust or hit 21
            if bust_check():
                return False
            if blackjack_check():
                return False

        # Repeating the process for every time they hit
        elif turns == 1:
            type_fast(f'\nYou now have the [{user1.users_cards[0]}], '
                      f'[{user1.users_cards[1]}], [{user1.users_cards[2]}] and the [{user1.users_cards[3]}]')
            user1.update_total()
            type_fast(f'That brings you to {user1.total}')
            if bust_check():
                return False
            if blackjack_check():
                return False

        elif turns == 2:
            type_fast(f'\nYou now have the [{user1.users_cards[0]}], [{user1.users_cards[1]}], [{user1.users_cards[2]}]'
                      f', [{user1.users_cards[3]}] and the [{user1.users_cards[4]}]')
            user1.update_total()
            type_fast(f'That brings you to {user1.total}')
            if bust_check():
                return False
            if blackjack_check():
                return False
        return True

    # Using an else: statement for if they entered "s" for the dealers question
    else:
        # Allowing the dealer to play his turn
        dealers_play()
        # Showing the user what the deal got
        type_fast(f'\nThe dealer had {dealers_cards}')
        type_fast(f'The dealers total is {get_dealers_total()}')

        # Using an if elif else statement for different outcomes due to the dealers play
        if user_total < get_dealers_total() < 22:
            type_fast('\nThe Dealer won')
            # Updating the users chips
            user_chips -= user_bet_chips
            user1.update_chips(user_chips)
            # Showing the user their chips
            type_fast(f'You now have {user_chips} chips')
            type_fast('\n')

        # Repeating for different outcomes
        elif user_total == get_dealers_total():
            type_fast('\nYou and the dealer had the same score. Your chips were returned')
            type_fast(f'You now have {user_chips} chips')
            type_fast('\n')

        elif get_dealers_total() > 21:
            type_fast('\nThe Dealer bust \n\nYou win!!!')
            user_chips += user_bet_chips
            user1.update_chips(user_chips)
            type_fast(f'You now have {user_chips} chips')
            type_fast('\n')

        else:
            type_fast('\nYou win!!!')
            user_chips += user_bet_chips
            user1.update_chips(user_chips)
            type_fast(f'You now have {user_chips} chips')
            type_fast('\n')
        return False


# Creating a class user to hold users data and methods to update the data
class User:

    # Creating an initializing method to hold user variable
    def __init__(self, chips):
        self.users_cards = []
        self.total = 0
        self.chips = chips
        self.chips_bet = 0

    # Method to give the user two random cards from a pack of cards (two random dict keys)
    def give_user_first_cards(self):
        card1 = get_one_card()
        self.users_cards.append(card1)
        card2 = get_one_card()
        self.users_cards.append(card2)

    # Method to update the users card value total
    def update_total(self):
        self.total = 0
        for i in self.users_cards:
            self.total += pack_of_cards_untouched.get(i)

    # Method to update the users chip total
    def update_chips(self, chips):
        self.chips = chips

    # Method to create a beginning message in relation to the users first cards and the total value of them
    def beginning_message(self):
        self.give_user_first_cards()
        self.update_total()
        type_fast(f'The dealer has dealt you the [{self.users_cards[0]}] and the [{self.users_cards[1]}]')
        type_fast(f'That brings you to {self.total}')

    # Method to reset the users cards value total
    def reset_total(self, reset_total):
        self.total = reset_total

    # Method to replace beginning message after the user has played one round of blackjack
    def next_message(self):
        global cards
        self.users_cards = []
        self.update_total()
        self.give_user_first_cards()
        self.update_total()
        type_fast(f'The dealer has dealt you the [{self.users_cards[0]}] and the [{self.users_cards[1]}]')
        type_fast(f'That brings you to {self.total}')


# Initializing a User class
user1 = User(100)
# Giving the dealer his first cards
give_dealer_first_cards()


# Function That holds the other function to be called to create the application as a whole
def application():
    """Runs the main application with all the necessary functions"""
    global cards
    # Making sure the total is rest each round
    user1.reset_total(0)
    # Getting the users input for the chips they want to bet
    user1.chips_bet = bet_chips()
    # Printing the beginning message
    user1.beginning_message()
    # calling the function application_beginning
    application_beginning()
    # Using a while loop to check if the user has hit the goal of the game
    while user1.chips < 300:
        # Using an if statement to check if the user has run out of chips
        if user1.chips == 0:
            print('Sorry you are out of chips\nGame Over')
            exit()
        user1.reset_total(0)
        type_fast(input('Press enter for next round'))
        # Putting the cards that were in play back into the deck
        cards = copy.deepcopy(pack_of_cards)
        user1.chips_bet = bet_chips()
        user1.next_message()
        type_fast('\n')
        application_beginning()
    else:
        if user1.chips >= 300:
            type_fast('CONGRATS!!! YOU COMPLETED THE GAME AND BEAT THE DEALER!!')


# Creating a welcome message to be displayed after the title art
welcome_message = f'\nWelcome To Blackjack!!!\nYou currently have {user1.chips} chips \n\nThe aim of the game is to ' \
                  f'reach a total of 300 chips! Good luck!\n '
# Printing the title art
print(title_art)
# Printing the welcome message
type_fast(welcome_message)
# Showing the user different navigation options
type_fast('1. Continue\n2. How to play')
# Allowing the user to navigate the beginning of the application
user_input = input('\nEnter the number you wish to proceed with: ')
if user_input == '1':
    type_fast('\n')
    application()

# Allowing the user to see the rules of the game
elif user_input == '2':
    type_fast(rules)
    input('\nPress enter to continue to the game\n')
    application()

# Using a while loop to check if the user entered a valid input
while user_input != '1' and user_input != '2':
    type_fast('Invalid input')
    user_input = input('\nEnter the number you wish to proceed with: ')

    if user_input == '1':
        type_fast('\n')
        application()

    elif user_input == '2':
        type_fast(rules)
        input('\nPress enter to continue to the game\n')
        application()

import random

class Card:
    """Represents a single playing card with suit and value."""
    suit_symbols = {'Hearts': '\033[31m♥\033[0m',  # Red
                    'Diamonds': '\033[31m♦\033[0m',  # Red
                    'Clubs': '\033[30m♣\033[0m',    # Black
                    'Spades': '\033[30m♠\033[0m'}   # Black

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f'{self.value}{Card.suit_symbols[self.suit]}'

class Deck:
    """Deck of 52 cards, able to deal and shuffle."""
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

def calculate_hand_value(hand):
    """Calculates the value of the hand."""
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
              'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    value = sum(values[card.value] for card in hand)
    aces = sum(card.value == 'A' for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def print_hand(hand, title):
    """Prints the hand."""
    hand_string = ' '.join(str(card) for card in hand)
    print(f"{title}: [{hand_string}] Total: {calculate_hand_value(hand)}")

def ask_for_bet(balance):
    """Asks the player for a bet amount."""
    while True:
        try:
            bet = int(input(f"\nYou have ${balance}. How much do you want to bet? $"))
            if 0 < bet <= balance:
                return bet
            print("Bet must be within your available balance.")
        except ValueError:
            print("Please enter a valid number.")

def player_turn(deck, player_hand, balance):
    """Manages the player's turn."""
    double_down = False
    if calculate_hand_value(player_hand) in [10, 11]:
        double_down = input("You have 10 or 11. Do you want to double down? (y/n): ").lower() == 'y'
        if double_down:
            return 'double'
    if player_hand[0].value == player_hand[1].value:
        split = input(f"You have two {player_hand[0].value}s. Do you want to split? (y/n): ").lower() == 'y'
        if split:
            return 'split'

    while True:
        action = input("\nDo you want to (h)it or (s)tand? ").lower()
        if action == 'h':
            player_hand.append(deck.deal_card())
            print(f"\nYou drew: {player_hand[-1]}")
            if calculate_hand_value(player_hand) > 21:
                print("\nYou bust! 😢")
                return 'bust'
            print_hand(player_hand, "Your hand")
        elif action == 's':
            return 'stand'

def dealer_turn(deck, dealer_hand):
    """Manages the dealer's turn."""
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.deal_card())
        print(f"Dealer draws: {dealer_hand[-1]}")
        print_hand(dealer_hand, "Dealer's hand")

def play_blackjack():
    balance = 1000
    while balance > 0:
        deck = Deck()
        player_hand = [deck.deal_card(), deck.deal_card()]
        dealer_hand = [deck.deal_card(), deck.deal_card()]
        bet = ask_for_bet(balance)

        print_hand(player_hand, "Your hand")
        print_hand(dealer_hand[:1], "Dealer's hand")

        player_action = player_turn(deck, player_hand, balance)
        if player_action == 'double' and balance >= bet:
            bet *= 2
            balance -= bet  # Additional bet for doubling down
            player_hand.append(deck.deal_card())
            print_hand(player_hand, "Your final hand after doubling down")
        elif player_action == 'split':
            # Implement split logic here (not provided in this snippet)
            pass

        if player_action != 'bust':
            dealer_turn(deck, dealer_hand)

        player_total = calculate_hand_value(player_hand)
        dealer_total = calculate_hand_value(dealer_hand)

        if player_total == 21 and len(player_hand) == 2:
            print("Blackjack! 🃏")
            winnings = int(bet * 2.5)
            balance += winnings
            print(f"You win ${winnings}!")
        elif dealer_total > 21 or (player_total <= 21 and player_total > dealer_total):
            balance += bet
            print(f"You won ${bet}! Your balance is now ${balance}. 🎉")
        elif player_total < dealer_total <= 21:
            balance -= bet
            print(f"You lost ${bet}. Your balance is now ${balance}. 😭")
        elif player_total == dealer_total:
            print("It's a push! 😐")
        else:
            balance -= bet
            print(f"You bust! 😢 Your balance is now ${balance}.")

        if balance == 0:
            print("You're out of money! Game over. 😔")
            break

        if input("Play again? (y/n): ").lower() != 'y':
            break

    print("\nThank you for playing! Goodbye.")

if __name__ == "__main__":
    play_blackjack()


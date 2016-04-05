import random

class Deck(object):
    # A deck contains the cards. It's interacted with by the player(s)
    def __init__(self):
        self.contents = ['2 of Diamonds', '2 of Hearts', '2 of Clubs', '2 of Spades', '3 of Diamonds', '3 of Hearts', '3 of Clubs', '3 of Spades', '4 of Diamonds', '4 of Hearts', '4 of Clubs', '4 of Spades', '5 of Diamonds', '5 of Hearts', '5 of Clubs', '5 of Spades', '6 of Diamonds', '6 of Hearts', '6 of Clubs', '6 of Spades', '7 of Diamonds', '7 of Hearts', '7 of Clubs', '7 of Spades', '8 of Diamonds', '8 of Hearts', '8 of Clubs', '8 of Spades', '9 of Diamonds', '9 of Hearts', '9 of Clubs', '9 of Spades', '10 of Diamonds', '10 of Hearts', '10 of Clubs', '10 of Spades', 'Jack of Diamonds', 'Jack of Hearts', 'Jack of Clubs', 'Jack of Spades', 'Queen of Diamonds', 'Queen of Hearts', 'Queen of Clubs', 'Queen of Spades', 'King of Diamonds', 'King of Hearts', 'King of Clubs', 'King of Spades', 'Ace of Diamonds', 'Ace of Hearts', 'Ace of Clubs', 'Ace of Spades']

    def shuffle(self):
        # Randomize the order of the cards in the deck
        random.shuffle(self.contents)

    def removeTopCard(self):
        # Remove the top card of the deck
        self.contents.pop(0)

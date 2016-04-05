from deck import Deck

class Player(object):
    #A player has a hand and a name. Interacts with the deck

    def __init__(self, playerName):
        self.hand = []
        self.name = playerName
        self.points = 0

    def draw(self, deck):
        #Draw a card from deck and tell the deck to remove its top card
        self.hand.append(deck.contents[0])
        deck.removeTopCard()

    def calculatePoints(self):
        #Figures out how many points the player's hand is worth
        points = 0
        numberOfAces = 0
        for card in self.hand:
            temp = card.split()
            if temp[0].isdigit():
                points += int(temp[0])
            elif temp[0] == 'Ace':
                points += 11
                numberOfAces += 1
            else:
                points += 10

        while numberOfAces > 0 and points > 21:
            numberOfAces -= 1
            points -= 10

        return points

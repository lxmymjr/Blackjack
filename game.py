from player import Player
from deck import Deck

class Game:
    def __init__(self):
        self.terminal = False
        self.player1 = Player('play1')
        self.player2 = Player('play2')
        self.playerList = [self.player1, self.player2]
        self.dealer = Player('dealer')
        self.playerList.append(self.dealer)
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.playerList:
            player.draw(self.deck)
            player.draw(self.deck)
        self.player1points = self.player1.calculatePoints()
        self.player2points = self.player2.calculatePoints()
        self.dealerpoints = self.dealer.calculatePoints()

    def step(game, player1points, player2points, dealerpoints, action1, action2, reward1, reward2):
        """ Returns the next game state and reward, given current state and actions.
        :param state: current state of the game
        :param action: 0 or 1, corresponding to hit or stick, respectively
        :return: a tuple (next game state, rewards)
        """

        # play1 turn
        if action1 == 0:
            game.player1.draw(game.deck)
            player1points = game.player1.calculatePoints()
            # if player1 is bust turn to player2
            if player1points > 21:
                reward1 = -1
        # play2 and dealer turn
        elif action1 == 1:
            if player1points > 21:
                reward1 = -1
            if action2 == 0:
                game.player2.draw(game.deck)
                player2points = game.player2.calculatePoints()
                # if player2 is bust terminate game
                if player2points > 21:
                    reward2 = -1
                    game.terminal = True
                    # dealer sticks on 17 or greater
                    while dealerpoints < 17:
                        game.dealer.draw(game.deck)
                        dealerpoints = game.dealer.calculatePoints()
                    # find a winner
                    if dealerpoints > 21:
                        if player1points <= 21:
                            reward1 = 1
                    else:
                        if player1points <= 21:
                            if player1points < dealerpoints:
                                reward1 = -1
                            elif player1points == dealerpoints:
                                reward1 = 0
                            elif player1points > dealerpoints:
                                reward1 = 1
            elif action2 == 1:
                game.terminal = True
                # dealer sticks on 17 or greater
                while dealerpoints < 17:
                    game.dealer.draw(game.deck)
                    dealerpoints = game.dealer.calculatePoints()
                # find a winner
                if dealerpoints > 21:
                    if player1points <= 21:
                        reward1 = 1
                    if player2points <= 21:
                        reward2 =1
                else:
                    if player1points <= 21:
                        if player1points < dealerpoints:
                            reward1 = -1
                        elif player1points == dealerpoints:
                            reward1 = 0
                        elif player1points > dealerpoints:
                            reward1 = 1
                    if player2points <= 21:
                        if player2points < dealerpoints:
                            reward2 = -1
                        elif player2points == dealerpoints:
                            reward2 = 0
                        elif player2points > dealerpoints:
                            reward2 = 1
        return player1points, player2points, dealerpoints, reward1, reward2

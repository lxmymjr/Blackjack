import numpy as np
import csv
from collections import defaultdict
import random
from player import Player
from deck import Deck
from game import Game
# import plot

def random_policy():
    return 0 if random.random() < 0.5 else 1

def epsilon_greedy_policy(epsilon, value_function, player, dealer):
    # exploration
    if random.random() < epsilon:
        return random_policy()
    # exploitation
    else:
        return best_policy(value_function, player, dealer)

def best_policy(value_function, player, dealer):
    value_HIT = value_function[(player, dealer, 0)]
    value_STICK = value_function[(player, dealer, 1)]

    if value_HIT > value_STICK:
        return 0
    elif value_STICK > value_HIT:
        return 1
    else:
        return random_policy()

def iteration(iterations, update, Name, policy, n_zero=100):

    # (player, dealer, action) key
    value_function = defaultdict(float)
    # (player, dealer) key
    counter_state = defaultdict(int)
    # (player, dealer, action) key
    counter_state_action = defaultdict(int)
    # number of wins
    wins1 = 0
    wins2 = 0
    winrecord1 = []
    winrecord2 = []

    for j in xrange(iterations):
        # create a new random starting state
        game = Game()
        player1 = game.player1points
        player2 = game.player2points
        dealer = game.dealerpoints
        action1 = None
        action2 = None
        reward1 = None
        reward2 = None
        # play a round
        observed_keys1 = []
        observed_keys2 = []
        while not game.terminal:

            if len(game.deck.contents) < 52 * 0.6:
                game.deck = Deck()
                game.deck.shuffle()
            # find an action defined by the policy
            if action1 is not 1 and reward1 is not -1:
                epsilon = n_zero / float(n_zero + counter_state[(player1, dealer)])
                action1 = policy(epsilon, value_function, player1, dealer)

            else:
                action1 = 1
                action2 = random_policy()

            if (player1, dealer, action1) not in observed_keys1 and player1 <=21:
                observed_keys1.append((player1, dealer, action1))
            if (player2, dealer, action2) not in observed_keys2 and action2 is not None:
                observed_keys2.append((player2, dealer, action2))

            # take a step
            [player1, player2, dealer, reward1, reward2] = Game.step(game, player1, player2, dealer, action1, action2, reward1, reward2)

        # we have reached an end of episode
        update(reward1, reward2, observed_keys1, observed_keys2, counter_state, counter_state_action, value_function)

        if j > iterations * 0.8:
            if reward1 == 1:
                wins1 += 1
            if reward2 == 1:
                wins2 += 1

        winrecord1.append(reward1)
        winrecord2.append(reward2)

    print(Name + 'Wins: %.4f%%' % ((float(wins1) / (iterations * 0.2)) * 100))

def MC(reward1, reward2, observed_keys1, observed_keys2, counter_state, counter_state_action, value_function):
    if reward1 is not None:
        # update over all keys
        for key in observed_keys1:
            # update counts
            counter_state[key[:-1]] += 1
            counter_state_action[key] += 1

            # update value function
            alpha = 1.0 / counter_state_action[key]
            value_function[key] += alpha * (reward1 - value_function[key])

    if reward2 is not None:
        # update over all keys
        for key in observed_keys2:
            # update counts
            counter_state[key[:-1]] += 1
            counter_state_action[key] += 1

            # update value function
            alpha = 1.0 / counter_state_action[key]
            value_function[key] += alpha * (reward2 - value_function[key])

def QL(reward1, reward2, observed_keys1, observed_keys2, counter_state, counter_state_action, value_function):
    if reward1 is not None:
        # update over all keys
        for i in range(len(observed_keys1)):
            # update counts
            counter_state[observed_keys1[i][:-1]] += 1
            counter_state_action[observed_keys1[i]] += 1

            # update value function
            alpha = 1.0 / counter_state_action[observed_keys1[i]]
            old = value_function[observed_keys1[i]]
            if i < len(observed_keys1) - 1:
                hit = observed_keys1[i+1][:2] + (1, )
                stick = observed_keys1[i+1][:2] + (0, )
                maxvalue = max(value_function[hit],value_function[stick])
                new = 0.8 * maxvalue
            else:
                new = 0
            value_function[observed_keys1[i]] = (1-alpha) * old + alpha * (reward1 + new)

    if reward2 is not None:
        # update over all keys
        for i in range(len(observed_keys2)):
            # update counts
            counter_state[observed_keys2[i][:-1]] += 1
            counter_state_action[observed_keys2[i]] += 1

            # update value function
            alpha = 1.0 / counter_state_action[observed_keys2[i]]
            old = value_function[observed_keys2[i]]
            if i < len(observed_keys2) - 1:
                hit = observed_keys2[i+1][:2] + (1, )
                stick = observed_keys2[i+1][:2] + (0, )
                maxvalue = max(value_function[hit],value_function[stick])
                new = 0.8 * maxvalue
            else:
                new = 0
            value_function[observed_keys2[i]] = (1-alpha) * old + alpha * (reward2 + new)

def TD(reward1, reward2, observed_keys1, observed_keys2, counter_state, counter_state_action, value_function):
    if reward1 is not None:
        # update over all keys
        for i in range(len(observed_keys1)):
            # update counts
            counter_state[observed_keys1[i][:-1]] += 1
            counter_state_action[observed_keys1[i]] += 1

            # update value function
            alpha = 1.0 / counter_state_action[observed_keys1[i]]
            old = value_function[observed_keys1[i]]
            if i < len(observed_keys1) - 1:
                new = 0.8 * value_function[observed_keys1[i+1]]
            else:
                new = 0
            value_function[observed_keys1[i]] = (1-alpha) * old + alpha * (reward1 + new)

    if reward2 is not None:
        # update over all keys
        for i in range(len(observed_keys2)):
            # update counts
            counter_state[observed_keys2[i][:-1]] += 1
            counter_state_action[observed_keys2[i]] += 1

            # update value function
            alpha = 1.0 / counter_state_action[observed_keys2[i]]
            old = value_function[observed_keys2[i]]
            if i < len(observed_keys2) - 1:
                new = 0.8 * value_function[observed_keys2[i+1]]
            else:
                new = 0
            value_function[observed_keys2[i]] = (1-alpha) * old + alpha * (reward2 + new)

winrecord_MC_epsilon = iteration(1000000000, MC, 'MC-epsilon', epsilon_greedy_policy)
winrecord_QL_epsilon = iteration(1000000000, QL, 'QL-epsilon', epsilon_greedy_policy)
winrecord_TD_epsilon = iteration(1000000000, TD, 'TD-epsilon', epsilon_greedy_policy)
winrecord_MC_best = iteration(1000000000, MC, 'MC-best', best_policy)
winrecord_QL_best = iteration(1000000000, QL, 'QL-best', best_policy)
winrecord_TD_best = iteration(1000000000, TD, 'TD-best', best_policy)

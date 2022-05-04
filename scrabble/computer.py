from simple import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
        Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
        This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    best = ['', 0]
    for i in range(1, HAND_SIZE + 1):
        perms = get_perms(hand, i)
        for perm in perms:
            score = get_word_score(perm, i)
            if is_valid_word(perm, hand, word_list) and score > best[1]:
                best = [perm, score]

    return best[0]


#
# Problem #6B: Computer plays a hand
#


def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    total_score = 0
    while True:
        print('Remaining in hand: ')
        display_hand(hand)
        word = comp_choose_word(hand, word_list)

        if word == '':
            print("\nComputer's hand finished. ")
            print("Total points: ", total_score)
            return None

        word_score = get_word_score(word, calculate_handlen(hand))
        total_score += word_score
        hand = update_hand(hand, word)
        print("\nPoints for : {0}".format(word), word_score)


#
# Problem #6C: Playing a game
#
#


def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    while True:
        cmd = ''
        while True:
            if isFirstHand:
                isFirstHand = not isFirstHand
                break

            print("'n' = play new hand")
            print("'r' = last hand")
            print("'e' = exit the game")

            cmd = input("Please enter 'n', 'r', or 'e': ")
            if cmd not in ['n', 'r', 'e']:
                print('Please try again...\n')
                continue

            if cmd == 'e':
                print('\nGame over. Goodbye!\n')
                return None
            break

        turn = ''
        while True:
            print("'u' = user plays first")
            print("'c' = computer plays first")

            user_input = input("Please enter 'u', or 'c': ")
            if user_input not in ['u', 'c']:
                print('Please try again...\n')
                continue

            break

        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)

        if turn == 'u':
            play_hand(hand.copy(), word_list)
        else:
            comp_play_hand(hand.copy(), word_list)


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    comp_play_hand(deal_hand(5), load_words())
    play_game(word_list)

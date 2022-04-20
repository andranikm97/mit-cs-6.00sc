import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = str.split(line)
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()

def str2dict(word):
    d = {}
    for c in word:
        d[c] = False
    return d

def displayGuessed(word, letters_guessed):
    guessed = ''
    for c in word:
        if letters_guessed[c]:
            guessed += ' {0} '.format(c)
        else:
            guessed += ' _ '
    return guessed

def checkAllGuessed(letters_guessed):
    for key in letters_guessed:
        if not letters_guessed[key]:
            return False
    return True

def game(word):
    tries = 0
    max_tries = 2 * len(word)
    letters_guessed = str2dict(word)
    total_guessed = 0
    print('\nLet\'s play Hangman!\n')
    print('I am thinking of word that is {0} letters long.\n'.format(len(word)))
    print('-----------------------------------------------\n')
    
    while not checkAllGuessed(letters_guessed) and tries <= max_tries:
        while True:
            guess = input('Please enter a guess: ')
            if (not guess.isalpha() or len(guess) != 1):
                print('Input is incorrect, please try again...\n')
            else:
                break
        
        guess = guess.lower()
        
        if (guess in letters_guessed):
            print('You guessed correctly!\n')
            if (letters_guessed[guess]):
                print('But...You have already guessed this letter, continue!\n')
                tries -= 1
            else:
                letters_guessed[guess] = True
                total_guessed += 1
        else:
            print('You guessed incorrectly...\n')

        print('Current guess:', displayGuessed(word, letters_guessed), '\n')
        print('You have {0} guesses left.\n'.format(max_tries - tries))
        tries += 1
    
    if (checkAllGuessed(letters_guessed)):
        print('Nice job! You guessed "{0}" correctly :)\n'.format(word))
    else:
        print('Too bad, so close! The word was "{0}" Next time :)\n'.format(word))
    
    while True:
        ans = input('Would you like to play again? (y/n)')
        if ans == 'y':
            print('Okay!\n\n')
            game(choose_word(wordlist))
            break
        elif ans == 'n':
            print('Goodbye!\n\n')
            break
        else:
            print('I did\'t get that, please try again')
            
game(choose_word(wordlist))
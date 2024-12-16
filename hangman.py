# This game will play hangman in the console with the user and keep a
# cumulative score for as many rounds as the user wants to play. It will use a
# list of a few thousand common english words between 6 and 12 letters from
# which to pick random words. If you want to use a different list, you can use
# the included listfix.py script to get rid of any words with fewer than six or
# more than 12 letters, or keep em, it's your game.
import random
import sys
import os

# In this case I think these globals are fine, They're needed in the display functions and the gameplay function
# The users cumulative score over however many games played.
score = 0
# The points value ( + or - ) of the current game
stakes = 0
# The list of words to be played
words = []
# The list of states the hangman board can be in
stages = [
    """
        -----
        |   |
            |
            |
            |
            |
            |
       ---------
    """,
    """
        -----
        |   |
        O   |
            |
            |
            |
            |
       ---------
    """,
    """
        -----
        |   |
        O   |
        |   |
        |   |
            |
            |
       ---------
    """,
    """
        -----
        |   |
        O   |
       /|   |
        |   |
            |
            |
       ---------
    """,
    """
        -----
        |   |
        O   |
       /|\  |
        |   |
            |
            |
       ---------
    """,
    """
        -----
        |   |
        O   |
       /|\  |
        |   |
       /    |
            |
       ---------
    """,
    """
        -----
        |   |
        O   |
       /|\  |
        |   |
       / \  |
            |
       ---------
    """
]

def clear_screen():
    # Should work on most platforms to clear the screen
    if sys.platform == 'win32':
        # Windows
        os.system('cls')
    else:
        # Linux, Mac, and anything else
        print('\033[H\033[2J', end='')

def get_random_word():
    # Get the word for this game
    global words
    global stakes
    
    # A temp holder for the chosen word
    wordchoice = ""

    # If there are no words already on the list, meaning it has not yet been
    # loaded, load the list from the data file words.txt
    if(len(words) < 1):
        script_path = os.path.dirname(__file__)
        with open(script_path + '/words.txt', 'r') as file:
            words = [word.strip().lower() for word in file]
    # Choose a random word from the list
    wordchoice = random.choice(words)
    # Update the stakes value for this game
    stakes = len(wordchoice)
    # Return the choosen word
    return wordchoice

def display_hangman(tries):
    global stages

    # Determin which on the list of stages should be used
    num_stages = len(stages) - 1
    # Then return it
    return stages[num_stages - tries]

def draw_game(word,message,mistakes_remaining,guessed_letters):
    # To keep everything consistent, this function draws the game state
    # wherever it is needed
    global score
    # Just a list of all letters for use in displaying the remainning letters
    all_letters = sorted(set("abcdefghijklmnopqrstuvwxyz")) # ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    # Draw the current state of the game
    # Clear the screen
    clear_screen()
    # Show the name of the game
    print("\n\n **** Hangman **** \n")
    # Show the score
    print("Score: ",score,"\n")
    # Draw the game board
    print(display_hangman(mistakes_remaining))
    # Show which letters are still available
    print("Remaining Letters:")
    print("".join([letter for letter in all_letters if letter not in guessed_letters]))
    #Show which letters have already been used
    print("Used Letters:")
    print("".join(map(str,sorted(guessed_letters))))
    # Display any status messages
    print(message)
    # Show progress on the solution and show the stakes
    print("The secret word: ", ' '.join([letter if letter in guessed_letters else '_' for letter in word])," (stakes: +/- ",stakes,"pts.)")


def play_hangman():
    global stages
    global stakes
    global score

    # Get the word for this game at random
    word = get_random_word()
    # Split out the word into its component letters
    word_letters = set(word)
    # Initialize the set to track guessed letters
    guessed_letters = set()
    # Initialize the status message variable
    message = "\n"
    # Set up the countdown until game over
    mistakes_remaining = len(stages) - 1

    # The game play loop
    while len(word_letters) > 0 and mistakes_remaining > 0:
        # Draw the current game state
        draw_game(word,message,mistakes_remaining,guessed_letters)
        # Get player's guess
        guess = input("Guess a letter: ").lower()
        # Validate the guess and update the game stats accordingly
        # Did you submit a single letter?
        if len(guess) == 1 and guess.isalpha():
            # Have you already guessed that one?
            if guess in guessed_letters:
                # Tell the user they've already used that letter
                message = "\nYou already guessed that letter. Try again."
            # Is the guessed letter not in the word?
            elif guess not in word_letters:
                # Tell the user the letter's not in the word
                message = "\nThat letter is not in the word."
                # Decrement the mistake counter    
                mistakes_remaining -= 1
                # Update the set of guessed letters
                guessed_letters.add(guess)
            # It is in the word
            else:
                # Congratulate the user
                message = "\nGood guess!"
                # Update the set of guessed letters
                guessed_letters.add(guess)
                # Remove it from the set of letters we're trying to guess
                word_letters.remove(guess)
        # Remind the user they can only enter a single letter
        else:
            message = "\nInvalid input. Please enter a single letter."

    # Display final result
    if mistakes_remaining == 0:
        # Update the score
        score = score - stakes
        # Draw the current game state
        draw_game(word,message,mistakes_remaining,guessed_letters)
        # Tell the user they lost
        print("Sorry, you've run out of guesses. The word was", word)
    else:
        # Update the score
        score = score + stakes
        # Draw the current game state
        draw_game(word,message,mistakes_remaining,guessed_letters)
        # Tell the user they won
        print("Congratulations! You guessed the word:", word)

if __name__ == "__main__":
    #def main():
    # Set the initial state of the play again variable to true for the first
    # trip through the loop
    again = True
    # As long as again = True continue looping
    while again:
        # play the game
        play_hangman()
        # Ask the user if they want to play again
        response = input("Would you like to play again? (y/n): ")
        # If the anser is not y or yes we set the again variable to false and
        # end the program. Otherwise it remains true and we repeat the loop
        # again
        if response.lower() not in ['y', 'yes']:
            again = False
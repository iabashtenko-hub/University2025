import random


WORDS = ['python', 'java', 'javascript', 'php']


def choose_word():
    return random.choice(WORDS)


def print_hidden(hidden):
    print(''.join(hidden))


def reveal_letter(word, hidden, letter):
    opened = 0
    for i in range(len(word)):
        if word[i] == letter and hidden[i] == '-':
            hidden[i] = letter
            opened += 1
    return opened


def process_letter_input(letter, guessed):
    if len(letter) != 1:
        print("You should input a single letter")
        return False

    if not letter.isalpha() or not letter.islower():
        print("Please enter a lowercase English letter")
        return False

    if letter in guessed:
        print("You've already guessed this letter")
        return False

    return True


def play_one_game():
    word = choose_word()
    hidden = ['-' for _ in word]
    attempts = 8
    guessed_letters = set()

    while attempts > 0:
        print()
        print_hidden(hidden)
        letter = input("Input a letter: > ").strip()

        if not process_letter_input(letter, guessed_letters):
            continue

        guessed_letters.add(letter)

        if letter not in word:
            print("That letter doesn't appear in the word")
            attempts -= 1
            continue

        opened_now = reveal_letter(word, hidden, letter)

        if opened_now == 0:
            print("No improvements")
            attempts -= 1

        if '-' not in hidden:
            print(f"You guessed the word {word}!")
            print("You survived!")
            return

    print("You lost!")


def main_menu():
    print("HANGMAN")
    while True:
        command = input('Type "play" to play the game, "exit" to quit: > ').strip()
        if command == "play":
            play_one_game()
        elif command == "exit":
            break


if __name__ == "__main__":
    main_menu()

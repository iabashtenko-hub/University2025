import random

def play_game():
    words = ['python', 'java', 'javascript', 'php']
    word = random.choice(words)
    hidden_word = ['-' for _ in word]
    attempts = 8
    guessed_letters = set()

    while attempts > 0:
        print()
        print(''.join(hidden_word))
        letter = input('Input a letter: > ').strip()

        if len(letter) != 1:
            print('You should input a single letter')
            continue
        if not letter.isalpha() or not letter.islower():
            print('Please enter a lowercase English letter')
            continue
        if letter in guessed_letters:
            print("You've already guessed this letter")
            continue

        guessed_letters.add(letter)

        if letter in word:
            if letter in hidden_word:
                print('No improvements')
            else:
                for i in range(len(word)):
                    if word[i] == letter:
                        hidden_word[i] = letter
        else:
            print("That letter doesn't appear in the word")
            attempts -= 1

        if '-' not in hidden_word:
            print(f'You guessed the word {word}!')
            print('You survived!')
            return

    print('You lost!')


def main():
    print('HANGMAN')
    while True:
        command = input('Type "play" to play the game, "exit" to quit: > ').strip()
        if command == 'play':
            play_game()
        elif command == 'exit':
            break
        else:
            continue


if __name__ == '__main__':
    main()
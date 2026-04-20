import random

def set_total_sticks():
    while True:
        qty = input("How many pencils would you like to use:\n> ")
        if not qty.isdigit():
            print("The number of pencils should be numeric")
            continue

        qty = int(qty)
        if qty <= 0:
            print("The number of pencils should be positive")
            continue

        return qty

def select_starter(users):
    while True:
        pick = input(f"Who will be the first ({', '.join(users)})?\n> ")
        if pick not in users:
            print(f"Choose between {', '.join(users)}")
            continue
        return pick

def ai_logic(remains):
    if remains % 4 == 0:
        return 3
    elif remains % 4 == 3:
        return 2
    elif remains % 4 == 2:
        return 1
    else:
        return random.randint(1, 3)

def human_logic(remains):
    while True:
        val = input("> ")
        if val not in ('1', '2', '3'):
            print("Possible values: '1', '2' or '3'")
            continue

        val = int(val)
        if val > remains:
            print("Too many pencils were taken")
            continue

        return val

def start_session():
    contestants = ["John", "Jack"]
    count = set_total_sticks()
    active_user = select_starter(contestants)

    print("|" * count)
    while count > 0:
        print(f"{active_user}'s turn!")

        if active_user == "Jack":
            step = ai_logic(count)
            print(step)
        else:
            step = human_logic(count)

        count -= step
        if count == 0:
            victor = contestants[1] if active_user == contestants[0] else contestants[0]
            print(f"{victor} won!")
            break

        print("|" * count)
        active_user = contestants[1] if active_user == contestants[0] else contestants[0]

if __name__ == "__main__":
    start_session()
import random

print("Welcome to the Dinner Party Bill Splitter!")

try:
    num_people = int(input("Enter the number of friends joining (including you):\n> "))
except ValueError:
    print("No one is joining for the party")
    exit()

if num_people <= 0:
    print("No one is joining for the party")
    exit()

friends = {}
print("Enter the name of every friend (including you), each on a new line:")
for _ in range(num_people):
    name = input("> ")
    friends[name] = 0

try:
    total_amount = float(input("Enter the total amount:\n> "))
except ValueError:
    print("Invalid amount!")
    exit()

lucky_choice = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ').strip()

if lucky_choice.lower() == "yes":
    lucky_person = random.choice(list(friends.keys()))
    print(f"{lucky_person} is the lucky one!")
else:
    lucky_person = None
    print("No one is going to be lucky")

num_to_pay = num_people - 1 if lucky_person else num_people
if num_to_pay > 0:
    share = round(total_amount / num_to_pay, 2)
else:
    share = 0

for person in friends:
    if person == lucky_person:
        friends[person] = 0
    else:
        friends[person] = share

print(friends)

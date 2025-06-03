"""Script to make a weighted random selection for the next lab meeting
presenter.

How to use:

    1. Update the MC.
    2. Update the list of current members.
    3. Add the most recent presentations to presentations.json (mind the name spelling).
    4. Run ``python whosnext.py``

Dependencies:

    - python >= 3
    - pyfiglet

Either ``pip install pyfiglet`` or ``conda install -c conda-forge pyfiglet``

"""
import collections
import datetime
import random
import time
import json

from pyfiglet import figlet_format

ROULETTE = True

presenters_per_meeting = 2

current_mc = 'Looka Schoneveld'
current_members = {
    "Bart de Vries": "2024-01-01",
    "Benjamin Gonzalez": "2024-09-01",
    "Christoph Konrad": "2022-10-01",
    "Eloy Vazquez": "2024-09-01",
    "Jason Moore": "2019-09-01",
    "Jules Ronné": "2023-10-01",
    "Looka Schoneveld": "2024-11-01",
    "Neville Nieman": "2024-08-01",
    "Ruben Terwint": "2025-03-01",
    "Yuke Huang": "2025-02-01",
	"Dana van der Pol": "2025-06-03"
}
with open("presentations.json", "r", encoding="utf-8") as file:
    presentations = json.load(file)

# the longer time since you've presented the higher your chance of being chosen
# the fewer times you've presented the higher chance of being chosen
# if you aren't a current member, no chance you are chosen
# if you gave one last week you don't have to go next
# if you are a new member, don't choose in first month after joining

# Parse presentation history
weights = {}
counts = collections.defaultdict(int)
last_pres_date = list(presentations.keys())[-1]
for date, presenters in presentations.items():

    pres_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    days_since_pres = (datetime.datetime.now() - pres_date).days
    weeks_since_pres = days_since_pres/7

    for presenter in presenters:

        # Set initial weights
        if presenter not in current_members:  # no longer in lab
            pass
        elif presenter == current_mc:  # current MC doesn't speak
            weights[presenter] = 0
        elif date == last_pres_date:  # presented at last meeting
            weights[presenter] = 0
        else:  # 6*30 = 180 if not presented in six months, otherwise scaled
            weights[presenter] = min(180, days_since_pres)

        # Count all presentations done in the last year
        if weeks_since_pres < 52:
            if presenter in current_members:
                counts[presenter] += 1

print('Initial weights and counts')
print('Weights:', weights)
print('Counts:', dict(counts))
print('\n')

# If a member hasn't presented at all set weight to 180, same as not presented
# in 6 months.
for member, date in current_members.items():
    join_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    days_since_join = (datetime.datetime.today() - join_date).days
    weeks_since_join = days_since_join/7
    if member not in weights.keys():
        if weeks_since_join <=4:
            weights[member] = 0
        else:
            weights[member] = 180

print("After adding members that haven't presented")
print(weights)
print('\n')

# Lower the weighting if you've presented alot in the last year Only way to
# have 0 is if you presented last week or are MC.
for person, count in counts.items():
    if weights[person] > 0:
        adjusted = weights[person] - count*2
        weights[person] = max(14, adjusted)

print("After lowering weight for lots of presentations")
print(weights)
print('\n')

# Select primary presenter(s) for next meeting!
choice = []
for i in range(presenters_per_meeting):
    chosen = random.choices(list(weights.keys()),
                            weights=list(weights.values()), k=1)[0]
    choice.append(chosen)
    # random.choices() is with replacement so you have to drop the chosen
    # before second choice
    del weights[chosen]

# Print the roulette to the screen!
if ROULETTE:
    for speed in range(6):
        current_members_list = list(current_members.keys())
        random.shuffle(current_members_list)
        for name in current_members_list:
            print(figlet_format(name, font='starwars', width=500))
            time.sleep(speed/20)

print(figlet_format('='*20, font='starwars', width=500))
print(figlet_format('Winner is!:', font='starwars', width=500))
for winner in choice:
    print(figlet_format(winner, font='starwars', width=500))
    if winner != choice[-1]:
        print(figlet_format(' '*20+'&', font='starwars', width=500))
print(figlet_format('='*20, font='starwars', width=500))


# Add chosen presenters to presentations.json
_ = input("")
add = input("Add presenters to memory? (y/n) ").strip()
if add == "y" or add == "yes":
    next_date = datetime.datetime.today() + datetime.timedelta(weeks=2)
    next_pres_date = next_date.strftime("%Y-%m-%d")
    presentations[next_pres_date] = choice
    print(f"Added '{list(presentations.keys())[-1]}: {list(presentations.values())[-1]}' to memory.")
else:
    print("Presenters not added")
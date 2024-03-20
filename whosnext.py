"""Script to make a weighted random selection for the next lab meeting
presenter.

How to use:

    1. Update the MC.
    2. Update the list of current members.
    3. Add the most recent presentations.
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

from pyfiglet import figlet_format

current_mc = 'Kenneth Pasma'

current_members = [
    'Christoph Schmidt',
    'Jason Moore',
    'Kenneth Pasma',
    'Rado Dukalski',
    'Thomas Habing',
    'Sietse Soethout',
    'Bart de Vries',
    'Anna Marbus',
    'Sara Youngbloud',
    'Neville Nieman',
]

# NOTE : Make sure spellings match current_members exactly! This should be
# sorted oldest (top) to newest (bottom).
presentations = {
    '2020-11-19': ['Jan Groenhuis', 'Marco Reijne'],
    '2020-12-03': ['Tim Huiskens', 'Jason Moore'],
    '2020-12-17': ['Jelle Haasnoot', 'Rado Dukalski'],
    '2021-01-14': ['Joris Kuiper', 'Marco Reijne'],
    '2021-01-28': ['Julie van Vlerken', 'Jason Moore'],
    '2021-02-11': ['Leila Alizadehsaravi', 'Rado Dukalski', 'Marco Reijne'],
    '2021-03-11': ['Jelle Haasnoot', 'Shannon van de Velde'],
    '2021-03-25': ['Eline van der Kruk', 'Jan Groenhuis', 'Jason Moore'],
    '2021-04-07': ['Eline van der Kruk'],
    '2021-04-22': ['Leila Alizadehsaravi'],
    '2021-05-06': ['Jason Moore', 'Joris Ravenhorst', 'Jan Groenhuis'],
    '2021-05-20': ['Marco Reijne', 'Joris Kuiper'],
    '2021-06-03': ['Arend Schwab'],
    '2021-06-17': ['Koen Jongbloed'],
    '2021-09-14': ['Rado Dukalski'],
    '2021-09-28': ['Tim Huiskens'],
    '2021-10-12': ['Leila Alizadehsaravi'],
    '2021-10-26': ['Jan Heinen'],
    '2021-11-09': ['Marco Reijne'],
    '2021-12-07': ['Dorus de Boer'],
    '2022-01-18': ['Jason Moore'],
    '2022-02-01': ['Leila Alizadehsaravi'],
    '2022-02-15': ['Jan Heinen'],
    '2022-03-01': ['Rado Dukalski'],
    '2022-03-15': ['Marco Reijne'],
    '2022-03-29': ['Leila Alizadehsaravi'],
    '2022-04-12': ['Francesca Andretta'],
    '2022-04-26': ['Jeswin Koshy Cherian'],
    '2022-05-10': ['Ajaypal Singh'],
    '2022-05-24': ['Evelijn Verboom'],
    '2022-06-07': ['Dorus de Boer'],
    '2022-06-21': ['Simonas Drauksas'],
    '2022-06-05': ['Andrew Dressel'],
    '2022-09-13': ['Jason Moore'],
    '2022-09-26': ['Rado Dukalski'],
    '2022-10-11': ['Jens Keijser'],
    '2022-10-25': ['Julie van Vlerken'],
    '2022-11-08': ['Jan van der Schot'],
    '2022-11-22': ['Timo Stienstra'],
    '2022-12-06': ['Christoph Schmidt'],
    '2022-12-20': ['Kenneth Pasma'],
    '2023-01-17': ['Floris van Willigen'],
    '2023-01-31': ['Sam Brockie'],
    '2023-02-14': ['Rado Dukalski'],
    '2023-02-28': ['Marten Haitjema'],
    '2023-03-14': ['Leila Alizadehsaravi'],
    '2023-03-28': ['Andrew Dressel'],
    '2023-04-11': ['Jason Moore'],
    '2023-04-25': ['Julie van Vlerken'],
    '2023-05-09': ['Jan van der Schot'],
    '2023-05-23': ['Gabriele Dell Orto'],
    '2023-06-06': ['Kirsten Dijkman'],
    '2023-06-20': ['Christoph Schmidt'],
    '2023-07-04': ['Sam Brockie'],
    '2023-10-10': ['Christoph Schmidt', 'Kenneth Pasma'],
    '2023-10-24': ['Leila Alizadehsaravi', 'Rado Dukalski'],
    '2023-11-07': ['Jules Ronne'],
    '2023-11-21': ['Marten Haitjema','Thomas Habing'],
    '2024-01-16': ['Kenneth Pasma','Christoph Schmidt'],
    '2024-01-30': ['Gabriele Dell Orto','Sietse Soethout'],
    '2024-02-13': ['Marten Haitjema'],
    '2024-02-27': ['Thomas Habing'],
    '2024-03-12': ['Anna Marbus','Sara Youngbloud'],
}

# the longer time since you've presented the higher your chance of being chosen
# the fewer times you've presented the higher chance of being chosen
# if you aren't a current member, no chance you are chosen
# if you gave one last week you don't have to go next
# TODO : if you are a new member, don't choose in first month after joining

weights = {}

for date, presenters in presentations.items():

    pres_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    days_since_pres = (datetime.datetime.now() - pres_date).days

    for presenter in presenters:

        if presenter not in current_members:  # no longer in lab
            weights[presenter] = 0
        elif presenter == current_mc:  # current MC doesn't speak
            weights[presenter] = 0
        elif days_since_pres < 63:  # presented recently (within 2 months)
            weights[presenter] = 0
        else:  # 150 if not presented in six months, otherwise scaled
            weights[presenter] = min(150, days_since_pres*6/7)

# If a member hasn't presented at all set weight to 150.
for member in current_members:
    if member not in weights.keys():
        weights[member] = 150

# Count all presentations done in the last year
counts = collections.defaultdict(int)
for date, presenters in presentations.items():
    pres_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    weeks_since_pres = (datetime.datetime.now() - pres_date).days/7
    if weeks_since_pres < 52:
        for presenter in presenters:
            counts[presenter] += 1

# Lower the weighting if you've presented alot in the last year
for person, count in counts.items():
    adjusted = weights[person] - count*10
    weights[person] = max(0, adjusted)

# Select a primary presenter for next week!
choice = random.choices(current_members,
                        weights=[weights[k] for k in current_members])

# Print the roulette to the screen!
for speed in range(6):
    random.shuffle(current_members)
    for name in current_members:
        print(figlet_format(name, font='starwars', width=500))
        time.sleep(speed/60)

print(figlet_format('='*30, font='starwars', width=500))
print(figlet_format('Winner is!:', font='starwars', width=500))
print(figlet_format(choice[0], font='starwars', width=500))
print(figlet_format('='*30, font='starwars', width=500))

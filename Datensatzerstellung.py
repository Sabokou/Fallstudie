# import sqlite3 as sql
import pandas as pd
from random import randint

# connection = sql.connect("Kundendaten.db")
# cursor = connection.cursor()

age_list = [[18,29], [30,55], [56,65], [65, 100]]
age_per = [0, 30, 70, 90, 101]

gender_list = ["M", "W", "D"]
gender_per = [50, 99, 101]

ges = list()

for i in range(10000):
    eintrag = []
    distro = randint(1,100)

    for i in range(len(age_per)):
        if distro < age_per[i]:
            age = randint(age_list[i-1][0], age_list[i-1][1])
            break
    eintrag.append(age)

    distro = randint(1,100)
    for i in range(len(gender_per)):
        if distro <= gender_per[i]:
            gender = gender_list[i]
            break
    eintrag.append(gender)

    ges.append(eintrag)

print(ges)



marital = ["ledig", "verheiratet", "aufgelöste Beziehung"]


child = ["ja", "nein"]



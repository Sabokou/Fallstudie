# import sqlite3 as sql
import pandas as pd
import numpy as np
from random import randint, choice

# connection = sql.connect("Kundendaten.db")
# cursor = connection.cursor()

age_list = [[18,29,"j"], [30,55, "je"], [56,65, "ae"], [65, 100, "a"]]
age_per = [0, 30, 70, 90, 101]

gender_list = ["M", "W", "D"]
gender_per = [50, 99, 101]

job_list = ["Administrativ", "Handwerk", "Management", "Öffentlicher Dienst", "Handel", "Ingenieurswesen", "Informatik", "Studium", "Arbeitslos", "Rente"]

m_job_j = [10, 25, 0, 30, 55, 60, 75, 99, 101, 0]
w_job_j = [30, 35, 0, 50, 70, 72, 78, 98, 101, 0]

m_job_je = [20, 40, 45, 55, 65, 85, 95, 97, 101, 0]
w_job_je = [30, 35, 37, 55, 75, 83, 93, 94, 101, 0]

m_job_ae = [15, 25, 35, 45, 55, 75, 85, 88, 93, 101]
w_job_ae = [25, 27, 32, 52, 77, 83, 87, 90, 95, 101]

m_job_a = [5, 7, 10, 13, 15, 17, 0, 19, 0, 101]
w_job_a = [3, 0, 4, 7, 12, 0, 0, 14, 0, 101]

job_dic = {"m_job_j" : m_job_j, "m_job_je": m_job_je, "m_job_ae": m_job_ae, "m_job_a": m_job_a,
     "w_job_j" : w_job_j, "w_job_je": w_job_je, "w_job_ae": w_job_ae, "w_job_a": w_job_a }

ges = list()

for i in range(10000):
    eintrag = []
    distro = randint(1,100)

    #Alter bestimmen
    for i in range(len(age_per)):
        if distro < age_per[i]:
            age = randint(age_list[i-1][0], age_list[i-1][1])
            alter_ident = age_list[i-1][2]
            break
    eintrag.append(age)

    #Geschlecht bestimmen
    distro = randint(1,100)
    for i in range(len(gender_per)):
        if distro <= gender_per[i]:
            gender = gender_list[i]
            geschlecht_ident = gender_list[i].lower()
            break
    eintrag.append(gender)

    #Job finden
    if geschlecht_ident != "d":
        job_query = geschlecht_ident + "_job_" + alter_ident
        job_prozente = job_dic.get(job_query)
        
        distro = randint(1,100)
        for i in range(len(job_prozente)):
            if distro <= job_prozente[i]:
                job = job_list[i]
                eintrag.append(job)
                break

    else:
        eintrag.append(choice(job_list))

    ges.append(eintrag)

print(ges)



marital = ["ledig", "verheiratet", "aufgelöste Beziehung"]


child = ["ja", "nein"]



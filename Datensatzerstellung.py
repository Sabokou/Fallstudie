# import sqlite3 as sql
import pandas as pd
import numpy as np
from random import randint, choice, uniform

# connection = sql.connect("Kundendaten.db")
# cursor = connection.cursor()

age_list = [[18,29,"j"], [30,55, "je"], [56,65, "ae"], [65, 85, "a"]]
age_per = [0, 30, 70, 90, 101]

gender_list = ["M", "W", "D"]
gender_per = [50, 99, 101]

#region Definition Kinder-Verteilung
child_list = ["ja", "nein"]

m_child_j = [15, 101]
w_child_j =  [25, 101]

m_child_je = [40, 101]
w_child_je =  [45, 101]

m_child_ae = [26, 101]
w_child_ae = [32, 101]

m_child_a = [0, 101]
w_child_a = [0, 101]

child_dic = {"m_child_j" : m_child_j, "m_child_je": m_child_je, "m_child_ae": m_child_ae, "m_child_a": m_child_a,
     "w_child_j" : w_child_j, "w_child_je": w_child_je, "w_child_ae": w_child_ae, "w_child_a": w_child_a }
#endregion

#region Definition Job-Verteilung
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
#endregion

#region Definition Heiratsstatus-Verteilung
marital_list = ["ledig", "verheiratet", "aufgelöste Beziehung"]
m_marital_j = [90, 99, 101]
w_marital_j =  [88, 99, 101]

m_marital_je = [40, 99, 101]
w_marital_je =  [45, 99, 101]

m_marital_ae = [10, 85, 101]
w_marital_ae = [10, 83, 101]

m_marital_a = [5, 66, 101]
w_marital_a = [5, 57, 101]

marital_dic = {"m_marital_j" : m_marital_j, "m_marital_je": m_marital_je, "m_marital_ae": m_marital_ae, "m_marital_a": m_marital_a,
     "w_marital_j" : w_marital_j, "w_marital_je": w_marital_je, "w_marital_ae": w_marital_ae, "w_marital_a": w_marital_a }

#endregion

#region Definition Gehalts-Merkmale
income_list = [[0, 15000, "very low"], [15001, 30000, "low"], [30001, 50000, "low mid"],[50001, 80000, "high mid"],[80001, 100000, "high"], [100001, 180000, "very high"]]
income_job_base = {"Verwaltung":25000, "Handwerk":20000, "Management":38000, "Öffentlicher Dienst":20000, "Handel/Logistik":25000, "Ingenieurswesen":35000, "Informatik":35000, "Studium":2000, "Arbeitslos":400, "Rente":300}
income_age_factors = {"j":1, "je":2, "ae":2.5, "a":2}
#endregion

#region Definition Produktwahrscheinlichkeiten
product_list = ["Girokonto", "Kredit", "Tagesgeldkonto", "Depotkonto", "Altersvorsorge", "Versicherung", "Bausparvertrag"]

product_chance_age = {"j": [70, 10, 5, 60, 20, 5, 5], \
                        "je": [60, 50, 5, 40, 70, 65, 85], \
                        "ae": [30, 50, 30, 10, 70, 60, 40], \
                        "a": [10, 35, 20, 5, 5, 80, 5]}

product_chance_gender = {"m": [-5, 10, 0, 20, -5, -15, 15], \
                            "w": [5, 0, -5, -20, 20, 30, 10], \
                            "d": [-10, 0, 15, -15, 5, 15, 0]}
                        
product_chance_marital = {"ledig": [0, 0, 0, 10, 0, 0, -10], \
                            "verheiratet": [10, 30, 0, -20, 5, 15, 15], \
                            "aufgelöste Beziehung": [-5, 0, 5, 0 , 0, 0, -15]}

product_chance_age = {"very low": [0, 20, -20, -40, -5, -5, -20], \
                        "low": [-5, 10, -10, -30, 70, 65, 85], \
                        "low mid": [30, 50, 30, 10, 70, 60, 40], \
                        "high mid": [10, 35, 20, 5, 5, 80, 5], \
                        "high": [60, 50, 5, 40, 70, 65, 85], \
                        "very high": [60, 50, 5, 40, 70, 65, 85]}

product_chance_child = {True: [-5, 10, 0, 20, -5, -15, 15], \
                        False: [5, 0, -5, -20, 20, 30, 10]}

ges = list()

#region Generation der Einträge
for i in range(100000):
    eintrag = []
    distro = randint(1,100)

#Generation Alter
    for i in range(len(age_per)):
        if distro < age_per[i]:
            age = randint(age_list[i-1][0], age_list[i-1][1])
            alter_ident = age_list[i-1][2]
            break
    eintrag.append(age)

#Generation Geschlecht
    distro = randint(1,100)
    for i in range(len(gender_per)):
        if distro <= gender_per[i]:
            gender = gender_list[i]
            geschlecht_ident = gender_list[i].lower()
            break
    eintrag.append(gender)

#Generation Job
    if geschlecht_ident != "d":
        job_query = geschlecht_ident + "_job_" + alter_ident
        job_prozente = job_dic.get(job_query)
        
        distro = randint(1,100)
        for i in range(len(job_prozente)):
            if age >= 70:
                job = "Rente"
                eintrag.append(job)
                break
            if distro <= job_prozente[i]:
                job = job_list[i]
                eintrag.append(job)
                break
    
    else:
        eintrag.append(choice(job_list))
    
#Generation Heiratsstatus
    if geschlecht_ident != "d":
        marital_query = geschlecht_ident + "_marital_" + alter_ident
        marital_prozente = marital_dic.get(marital_query)
        
        distro = randint(1,100)
        for i in range(len(marital_prozente)):
            if distro <= marital_prozente[i]:
                marital = marital_list[i]
                eintrag.append(marital)
                break

    else:
        eintrag.append(choice(marital_list))

#Generation Kind-Merkmal
    if geschlecht_ident != "d":
        child_query = geschlecht_ident + "_child_" + alter_ident
        child_prozente = child_dic.get(child_query)
        
        if marital == "ledig":
            child_prozente[0] -= 15

        distro = randint(1,100)
        for i in range(len(child_prozente)):
            if distro <= child_prozente[i]:
                child = child_list[i]
                eintrag.append(child)
                kinderbonus = 5000
                break
            
    else:
        eintrag.append(choice(child_list))
    
    #Generation Gehalt
    Zufallsfaktor = uniform(0.7, 1.3)
    income_base = income_job_base.get(job, 20000)
    age_factor = income_age_factors.get(alter_ident, 1)
    income = round(Zufallsfaktor * (income_base * age_factor) + kinderbonus,0)

    for i in income_list:
        if int(income) in range(i[0], i[1]):
            income = round(randint(i[0], i[1]), -3)
            gehalt = i[2]
            break
    
    eintrag.append(income)

    produkt = choice(product_list)
    eintrag.append(produkt)

    gekauft = True
    eintrag.append(gekauft)


    ges.append(eintrag)
#endregion

df = pd.DataFrame(ges, columns=["Alter", "Geschlecht", "Job", "Familienstand", "Kinder", "Gehalt", "Angebotenes Produkt", "Gekauft"]) #, "Angebotenes Produkt", "Gekauft"
print(df)

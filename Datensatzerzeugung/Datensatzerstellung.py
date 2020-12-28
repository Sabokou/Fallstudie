import pandas as pd
import numpy as np
from random import randint, choice, uniform
from datetime import date

#region Datenbank aufrufen
from sqlalchemy import create_engine
import datetime
e = create_engine('sqlite:///Kundendaten.db')

#endregion

#region Definition Alter-Verteilung
age_list = [[18,29,"j"], [30,55, "je"], [56,65, "ae"], [65, 85, "a"]]
age_per = [0, 30, 70, 90, 101]
#endregion

#region Definition Geschlechter-Verteilung
gender_list = ["M", "W", "D"]
gender_per = [50, 99, 101]

#endregion

#region Definition Kinder-Verteilung
child_list = ["ja", "nein"]

m_child_j = [15, 101]
w_child_j =  [25, 101]

m_child_je = [55, 101]
w_child_je =  [59, 101]

m_child_ae = [56, 101]
w_child_ae = [62, 101]

m_child_a = [40, 101]
w_child_a = [50, 101]

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

#TODO:Anpassung Berechnung mit Multiplizieren
#region Definition Produktwahrscheinlichkeiten
product_list = ["Girokonto", "Kredit", "Tagesgeldkonto", "Depotkonto", "Altersvorsorge", "Versicherung", "Bausparvertrag"]

product_winnings = {"Girokonto" : 0.4, "Kredit": 0.35, "Tagesgeldkonto": 2.31, "Depotkonto": 2.33, \
                    "Altersvorsorge": 9.37, "Versicherung": 8.51, "Bausparvertrag":1.39}

product_prozente = [15, 71, 76, 82, 84, 87, 100]

product_chance_age = {"j":  [70, 10, 5,  60, 10,  5,  5], \
                      "je": [60, 50, 5,  50, 45, 65, 85], \
                      "ae": [30, 50, 30, 10, 70, 60, 40], \
                      "a":  [10, 35, 20, 5,   5, 80,  5]}

product_chance_gender = {"m": [0.90,   1.2,   1,     1.2,   0.90,   0.70,  1], \
                         "w": [1.05,     1,   0.85,   0.7,   1.2,    1.3,  1.1], \
                         "d": [0.8,   1,   1.2,   0.5,    1.1,    1.15,   1]}
                        
product_chance_marital = {"ledig":                  [1,     1,  1,   1.1,     0,       0,      0.7], \
                          "verheiratet":            [1.2,    1.3, 0.8,  0.67,     1.1,      1.25,       1.5], \
                          "aufgelöste Beziehung":   [0.8,    1,  1.05,    1.0,     1.0,       1.0,      0.8]}

product_chance_income = {"very low":    [1,     1.3,     0.8,    0.6,    0.7,     0.95,     0.7], \
                        "low":          [1,     1.1,     0.9,    0.7,    0.95,    0.9,      0.95], \
                        "low mid":      [1,     1.15,    1,      0.8,    1,       1,        1.05], \
                        "high mid":     [1,     1.35,    1.20,   1.1,    1.05,    1.1,      1.15], \
                        "high":         [1,     0.9,     1,      1.4,    1.1,     1.3,      1.1], \
                        "very high":    [1 ,    0.7,     1.10,   1.3,    1.15,    1.25,     1]}

product_chance_child = {"ja":   [1.25,    1.1, 0.9, 0.7,     0.9,  1.15,  1.25], \
                        "nein": [1,       1,   1.1, 1.2,     1.2,  1,     1.1]}

#endregion

ges = list()

#region Generation der Einträge
for jahr in range(2016,2021):
    for monat in range(1,13):
        for i in range(int(60000 + (jahr%2014) * uniform(0.7,1.2) * 10000)): #add back one 0
            
            #Simulation Wirtschaftscrash während Corona
            if jahr == 2020 and monat == 3:
                if i == int(60000 + (jahr%2014) * 0.7 * 10000):
                    break 
            elif jahr == 2020 and monat == 4:
                if i == int(60000 + (jahr%2014) * 0.8 * 10000):
                    break
            elif jahr == 2020 and monat == 5:
                if i == int(60000 + (jahr%2014) * 0.85 * 10000):
                    break
        
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
                        break
                    if distro <= job_prozente[i]:
                        job = job_list[i]
                        break
            
            else:
                job = choice(job_list)

            eintrag.append(job)
        #Generation Heiratsstatus
            if geschlecht_ident != "d":
                marital_query = geschlecht_ident + "_marital_" + alter_ident
                marital_prozente = marital_dic.get(marital_query)
                
                distro = randint(1,100)
                for i in range(len(marital_prozente)):
                    if distro <= marital_prozente[i]:
                        marital_ident = marital_list[i]
                        break

            else:
                marital_ident = choice(marital_list)

            eintrag.append(marital_ident)

        #Generation Kind-Merkmal
            if geschlecht_ident != "d":
                child_query = geschlecht_ident + "_child_" + alter_ident
                child_prozente = child_dic.get(child_query)
                
                local_child_prozente = child_prozente.copy()
                if marital_ident == "ledig":
                    local_child_prozente[0] -= 15

                distro = randint(1,100) 
                for i in range(len(local_child_prozente)):
                    if distro <= local_child_prozente[i]:
                        child_ident = child_list[i]
                        break
                    
            else:
                child_ident = choice(child_list)
            
            if child_ident == "ja":
                kinderbonus = 5000
            else:
                kinderbonus = 0
                    
            eintrag.append(child_ident)
            
            #Generation Gehalt
            Zufallsfaktor = uniform(0.7, 1.3)
            income_base = income_job_base.get(job, 20000)
            age_factor = income_age_factors.get(alter_ident, 1)
            income = round(Zufallsfaktor * (income_base * age_factor) + kinderbonus,0)

            for i in income_list:
                if int(income) in range(i[0], i[1]):
                    income = round(randint(i[0], i[1]), -3)
                    gehalt_ident = i[2]
                    break
            
            eintrag.append(income)

                       

            #Verteilung Produkte berücksichtigen
            distro = randint(1,100)
            for i in range(len(product_prozente)):
                if distro <= product_prozente[i]:
                    produkt = product_list[i]
                    break
            
            #Produkt hinzufügen
            produkt_index = product_list.index(produkt)
            eintrag.append(produkt)


            #Bestimmen, ob Produkt angenommen oder abgelehnt wurde
            chance = (product_chance_age.get(alter_ident)[produkt_index] // 2) * product_chance_child.get(child_ident)[produkt_index] * \
                    product_chance_gender.get(geschlecht_ident)[produkt_index] * product_chance_income.get(gehalt_ident)[produkt_index] * \
                    product_chance_marital.get(marital_ident)[produkt_index] 

            if chance >= 90:
                chance = uniform(0.8 ,1.1) * 88
            elif chance <= 10:
                chance = uniform(0.8, 1.1) * 12
            
            distro = randint(0,100)
            if distro <= chance:
                gekauft = "ja"
                anzahl = 1
            else:
                gekauft = "nein"
                anzahl = 0
            eintrag.append(gekauft)

            if gekauft == "ja":
                gewinn = product_winnings.get(produkt)
            else:
                gewinn = 0

            eintrag.append(gewinn)

            #Datum erzeugen
            eintrag.append(jahr)
            eintrag.append(monat)
            tag = randint(1,28)
            eintrag.append(tag)
            
            date = datetime.date(year=jahr, month=monat, day=tag)
            eintrag.append(str(date.year) + '-' + str(date.month))

            eintrag.append(anzahl)
            ges.append(eintrag)
        #endregion
    
        print(f"Monat {monat} | Jahr {jahr} | done")

df = pd.DataFrame(ges, columns=["Alter", "Geschlecht", "Job", "Familienstand", "Kinder", "Gehalt",\
                                 "Angebotenes Produkt", "Gekauft", "Gewinn",\
                                 "Jahr", "Monat", "Tag", "Datum", "Anzahl"]) 
print("Converted to Dataframe")
df.to_sql(name="allgemeine_daten", con=e, if_exists="replace")
print("Transfer complete")
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

code_matiere={'FRANCAIS': "50",
              "E.P.S.": "51",
              "E.M.C.": "1002",
              "ENSEIGNEMENT SCIENTIFIQUE": "138",
              "HIST-GEO O.I.B. FR": "11",
              "HIST-GEO, GEOPO. ET SC. PO.":"1062",
              "MATHEMATIQUES SPE": "700",
              "PHYSIQUE-CHIMIE": "701",
              "PHYSIQUE-CHIMIE SPE": "701",
              "HIST-GEO O.I.B. AR": "1034",
              "LV1 ARABE O.I.B.": "992",
              "LV2 ANGLAIS": "8",
              "LV3 ESPAGNOL": "9",
              "MATH EXPERTES": "1068",
              "PHILOSOPHIE": "6"}
donnees_bulletins={"50":[], "51":[] , "1002":[], "138":[], "11":[], "1062":[], "700":[], "701":[], "1034":[], "992":[], "8":[], "9":[],"1068":[], "6":[], "app_gnl":""}


ES_notes = [[],[]]
driver = webdriver.Firefox()
driver.get("https://3500057k.index-education.net/pronote/eleve.html")
sleep(10)
username = driver.find_element(By.ID, 'id_23')
username.send_keys('mamar')
password_box = driver.find_element(By.ID, 'id_24')
password_box.send_keys("wafaa2005")
submit_button = driver.find_element(By.ID, 'id_12')
submit_button.click()
sleep(10)
notes = driver.find_element(By.ID, 'GInterface.Instances[0].Instances[1]_Combo2')
notes.click()
trimestre_liste = driver.find_element(By.ID, 'GInterface.Instances[2].Instances[0].bouton_Edit')
trimestre_liste.click()
trimestre = driver.find_element(By.ID, 'GInterface.Instances[2].Instances[0]_0')
trimestre.click()
sleep(5)
matieres = driver.find_elements(By.CLASS_NAME, 'Gras')
print(matieres)
count = 0
es = 0
for matiere in matieres:
    if count == 0 or count == 1:
        count += 1
        continue
    if "Moyenne générale" in matiere.text:
        break
    matiere.click()
    bloc_matiere = driver.find_element(By.CLASS_NAME, 'BlocDevoirEvaluation_Contenu')
    notes = bloc_matiere.find_elements(By.CLASS_NAME, "Gras")
    entete_matiere = driver.find_element(By.CLASS_NAME, 'BlocUneLigne')
    nom_matiere = entete_matiere.find_element(By.CLASS_NAME, 'Gras')
    try:
        code_mat_association_temporaire = code_matiere[nom_matiere.text]
    except:
        print(" ")
    counter_note = 1
    for note in notes:
        if "ENSEIGNEMENT SCIENTIFIQUE" in nom_matiere.text:
            if counter_note == 3:
                max = note.text
            elif counter_note == 4:
                ES_notes[es].append(max)
                ES_notes[es].append(note.text)
            else:
                ES_notes[es].append(note.text)
        else:
            if counter_note == 3:
                max = note.text
            elif counter_note == 4:
                donnees_bulletins[code_mat_association_temporaire].append(max)
                donnees_bulletins[code_mat_association_temporaire].append(note.text)
            else:
                donnees_bulletins[code_mat_association_temporaire].append(note.text)
        counter_note += 1
    if "ENSEIGNEMENT SCIENTIFIQUE" in nom_matiere.text:
        es+=1

for i in range(4):
    ES_notes[0][i] = ES_notes[0][i].replace(',','.')
    ES_notes[1][i] = ES_notes[1][i].replace(',', '.')
    donnees_bulletins["138"].append((float(ES_notes[0][i])+float(ES_notes[1][i]))/2)
print(donnees_bulletins)

bulletin = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[4]/div[1]/ul/li[3]/div/div")
bulletin.click()

sleep(5)
cellules = driver.find_elements(By.CLASS_NAME, 'liste_celluleGrid')
matieres = []
appreciation = []
for cellule in cellules:
    print(cellule.value_of_css_property("background-color"))
    if str(cellule.value_of_css_property("background-color")) == "rgb(255, 255, 255)":
        appreciation.append(cellule.text)
    elif str(cellule.value_of_css_property("background-color")) == 'rgb(226, 226, 226)':
        titre_matiere = cellule.find_elements(By.CLASS_NAME, 'ie-ellipsis')
        if titre_matiere[0].text != 'PHYS-CHI' and titre_matiere[0].text != 'SVT':
            matieres.append(titre_matiere[0].text)

iterations = len(matieres)
for i in range(iterations):
    code_mat_association_temporaire = code_matiere[matieres[i]]
    donnees_bulletins[code_mat_association_temporaire].append(appreciation[i])


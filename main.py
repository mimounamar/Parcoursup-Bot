from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#Association matières et ParcourSup
code_matiere={'FRANCAIS': "50",
              "E.P.S.": "51",
              "E.M.C.": "1002",
              "ENSEIGNEMENT SCIENTIFIQUE": "138",
              "HIST-GEO O.I.B. FR": "11",
              "HIST-GEO, GEOPO. ET SC. PO.":"1062",
              "MATHEMATIQUES SPE": "700",
              "PHYSIQUE-CHIMIE SPE": "701",
              "HIST-GEO O.I.B. AR": "1034",
              "LV1 ARABE O.I.B.": "992",
              "LV1 ARABE": "7",
              "LV2 ANGLAIS": "8",
              "LV3 ESPAGNOL": "9",
              "MATH EXPERTES": "1068",
              "PHILOSOPHIE": "6",
              "SCIENCES DE LA VIE ET DE LA TERRE.": "702",
              "ARTS PLASTIQUES OPTION": "183"}
donnees_bulletins={"7":[],"183":[],"702":[], "50":[], "51":[] , "1002":[], "138":[], "11":[], "1062":[], "700":[], "701":[], "1034":[], "992":[], "8":[], "9":[],"1068":[], "6":[], "app_gnl":""}

#Initialisation du programme et invité de commande
document = ''
identifiant_prnt = ''
mot_de_passe_prnt = ''
identifiant_prcrsup = ''
mot_de_passe_prcrsup = ''
trimestre_remontee = ''
print("A. Choisir votre mode de remontée.")
print("Pour importer vos notes depuis un fichier PDF, saisissez 1.")
print("Pour importer vos notes depuis Pronote, saisissez 2.")
mode = int(input("Votre réponse > "))
if mode == 1:
    print("A.1. Donnez le nom de votre document.")
    document = str(input("Votre réponse > "))
elif mode == 2:
    print("A.1. Donnez votre identifiant Pronote.")
    identifiant_prnt = str(input("Votre réponse > "))
    print("A.2. Donnez votre mot de passe Pronote.")
    mot_de_passe_prnt = str(input("Votre réponse > "))
    print("A.3. Pour remonter le 1e trimestre de Terminale, saisir 0, pour le 2e trimestre, saisir 1.")
    trimestre_remontee = str(input("Votre réponse > "))
else:
    print("Vous n'avez saisi aucune des options possibles.")
    exit()
print("B.1. Donnez votre identifiant Parcoursup.")
identifiant_prcrsup = str(input("Votre réponse > "))
print("B.2. Donnez votre mot de passe Parcoursup.")
mot_de_passe_prcrsup = str(input("Votre réponse > "))

#Traitement des données des bulletins format PDF
def pdf():
    print("Étape 1 - Lecture des données du bulletin par l'algorithme")
    HTMLFile = open("bulletins/"+document)
    index = HTMLFile.read()
    soup = BeautifulSoup(index, 'html.parser')
    table = soup.find("table")
    row_count = 0
    transcript_data = []
    for row in table.find_all("tr"):
        if row_count != 0 and row_count != 1:
            cells = row.find_all("td")
            cell_count = 0
            code_mat_association_temporaire = ""
            for cell in cells:
                cell_components = cell.find_all("p")
                for cell_component in cell_components:
                    temp = cell_component.text
                    if cell_count == 0:
                        if cell_component.text == 'PHYSIQUE-CHIMIE':
                            temp = 'PHYSIQUE-CHIMIE SPE'
                        code_mat_association_temporaire = code_matiere[temp]
                    elif cell_count != 1:
                        donnees_bulletins[code_mat_association_temporaire].append(temp)
                    cell_count += 1
        row_count += 1
    span = soup.find_all("span")
    app = span[-1]
    donnees_bulletins['app_gnl'] = app.text
    print("Étape 1 - Terminée avec succès")

#Traitement des données des bulletins via Pronote
#Remarque: pour 1e trimestre, mettre GInterface.Instances[2].Instances[0]_0
#Remarque: pour 2e trimestre, mettre GInterface.Instances[2].Instances[0]_1
def pronote():
    print("Étape 1.a - Identification sur Pronote")
    ES_notes = [[], []]
    driver = webdriver.Firefox()
    driver.get("https://3500057k.index-education.net/pronote/eleve.html")
    sleep(10)
    username = driver.find_element(By.ID, 'id_23')
    username.send_keys(identifiant_prnt)
    password_box = driver.find_element(By.ID, 'id_24')
    password_box.send_keys(mot_de_passe_prnt)
    submit_button = driver.find_element(By.ID, 'id_12')
    submit_button.click()
    sleep(10)
    notes = driver.find_element(By.ID, 'GInterface.Instances[0].Instances[1]_Combo2')
    notes.click()
    driver.execute_script("""
    var element = document.querySelector("#id_1_bloquer");
    if (element)
        element.parentNode.removeChild(element);
    """)
    trimestre_liste = driver.find_element(By.ID, 'GInterface.Instances[2].Instances[0].bouton_Edit')
    trimestre_liste.click()
    trimestre = driver.find_element(By.ID, 'GInterface.Instances[2].Instances[0]_'+trimestre_remontee)
    trimestre.click()
    sleep(5)
    matieres = driver.find_elements(By.CLASS_NAME, 'Gras')
    count = 0
    es = 0
    print("Étape 1.b - Import des notes via Pronote.")
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
            o = 0
        counter_note = 1
        for note in notes:
            if "ENSEIGNEMENT SCIENTIFIQUE" in nom_matiere.text:
                if counter_note == 3:
                    max = note.text
                elif counter_note == 4:
                    ES_notes[es].append(note.text)
                    ES_notes[es].append(max)
                else:
                    ES_notes[es].append(note.text)
            else:
                if counter_note == 3:
                    max = note.text
                elif counter_note == 4:
                    donnees_bulletins[code_mat_association_temporaire].append(note.text)
                    donnees_bulletins[code_mat_association_temporaire].append(max)
                else:
                    donnees_bulletins[code_mat_association_temporaire].append(note.text)
            counter_note += 1
        if "ENSEIGNEMENT SCIENTIFIQUE" in nom_matiere.text:
            es += 1

    #Gestion des moyennes d'enseignement scientifique
    for i in range(4):
        ES_notes[0][i] = ES_notes[0][i].replace(',', '.')
        ES_notes[1][i] = ES_notes[1][i].replace(',', '.')
        donnees_bulletins["138"].append((float(ES_notes[0][i]) + float(ES_notes[1][i])) / 2)

    bulletin = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[4]/div[1]/ul/li[3]/div/div")
    bulletin.click()

    sleep(5)
    print("Étape 1.c - Import des appréciations via Pronote.")
    cellules = driver.find_elements(By.CLASS_NAME, 'liste_celluleGrid')
    matieres = []
    appreciation = []
    for cellule in cellules:
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
    app_gnl_contnr = driver.find_element(By.XPATH, "//div[contains(@id,'_consult')]")
    app_gnl_ctnt = app_gnl_contnr.find_element(By.CLASS_NAME, 'Gras')
    donnees_bulletins['app_gnl'] = app_gnl_ctnt.text
    print("Étape 1 - Terminée avev succès")

#Choisir le mode d'action
if mode == 1:
    pdf()
elif mode == 2:
    pronote()
donnees_bulletins['7'] = donnees_bulletins['992']

#Initialisation du robot
print("Étape 2.a - Identification sur Parcoursup")
driver = webdriver.Firefox()
driver.get("https://dossier.parcoursup.fr/Candidat/authentification")

#Authentification ParcourSup
file_box = driver.find_element(By.NAME, 'g_cn_cod')
file_box.send_keys(identifiant_prcrsup)
password_box = driver.find_element(By.NAME, 'g_cn_mot_pas')
password_box.send_keys(mot_de_passe_prcrsup)
submit_button = driver.find_element(By.ID, 'btnConnexion').find_element(By.CLASS_NAME, "btn-bordure-orange")
submit_button.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "MA SCOLARITE"))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Bulletins scolaires"))).click()
sleep(5)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "tarteaucitronPersonalize2"))).click()
driver.switch_to.frame("iframeBulletin")

#Saisie des données sur l'espace candidat
print("Étape 2.b - Import des notes et appréciations sur Parcoursup.")
for matiere in code_matiere:
    id_matiere = code_matiere[matiere]
    try:
        moyenne_candidat = driver.find_element(By.ID, ("cdt_" + id_matiere))
        moyenne_classe = driver.find_element(By.ID, ("cla_" + id_matiere))
        moyenne_max = driver.find_element(By.ID, ("hau_" + id_matiere))
        moyenne_min = driver.find_element(By.ID, ("bas_" + id_matiere))
        appr = driver.find_element(By.ID, ("app_" + id_matiere))
    except:
        continue
    try:
        moyenne_candidat.send_keys(donnees_bulletins[id_matiere][0])
        moyenne_classe.send_keys(donnees_bulletins[id_matiere][1])
        moyenne_max.send_keys(donnees_bulletins[id_matiere][3])
        moyenne_min.send_keys(donnees_bulletins[id_matiere][2])
        appr.send_keys(donnees_bulletins[id_matiere][4])
    except IndexError:
        moyenne_candidat.send_keys("N")
        moyenne_classe.send_keys("N")
        moyenne_max.send_keys("N")
        moyenne_min.send_keys("N")
        appr.send_keys(" ")

app_gnl = driver.find_element(By.ID, "app_999")
app_gnl.send_keys(donnees_bulletins['app_gnl'])
print("Étape 2 - Terminée avec succès.")


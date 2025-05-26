import sqlite3

conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    age INTEGER,
    maladies TEXT,
    traitements TEXT
)
''')
conn.commit()

def ajouter_patient():
    nom = input("Nom du patient : ")
    age = input("Âge : ")
    maladies = input("Maladie(s) : ")
    traitements = input("Traitement(s) : ")
    cursor.execute('INSERT INTO patients (nom, age, maladies, traitements) VALUES (?, ?, ?, ?)',
                   (nom, age, maladies, traitements))
    conn.commit()
    print(f"Patient {nom} ajouté.\n")

def rechercher_patient():
    nom = input("Nom du patient à rechercher : ")
    cursor.execute('SELECT * FROM patients WHERE nom LIKE ?', ('%' + nom + '%',))
    resultats = cursor.fetchall()
    if resultats:
        for patient in resultats:
            print(patient)
    else:
        print("Aucun patient trouvé avec ce nom.\n")

def modifier_patient():
    id_patient = input("ID du patient à modifier : ")
    cursor.execute('SELECT * FROM patients WHERE id = ?', (id_patient,))
    patient = cursor.fetchone()
    if not patient:
        print("Patient non trouvé.\n")
        return
    print(f"Patient actuel : {patient}")
    nom = input("Nouveau nom (appuyez sur Entrée pour garder l'ancien) : ")
    age = input("Nouvel âge (Entrée pour garder) : ")
    maladies = input("Nouvelles maladie(s) (Entrée pour garder) : ")
    traitements = input("Nouveau(x) traitement(s) (Entrée pour garder) : ")
    
    nom = nom if nom else patient[1]
    age = age if age else patient[2]
    maladies = maladies if maladies else patient[3]
    traitements = traitements if traitements else patient[4]

    cursor.execute('''
    UPDATE patients
    SET nom = ?, age = ?, maladies = ?, traitements = ?
    WHERE id = ?
    ''', (nom, age, maladies, traitements, id_patient))
    conn.commit()
    print(f"Patient {id_patient} modifié.\n")

def supprimer_patient():
    id_patient = input("ID du patient à supprimer : ")
    cursor.execute('SELECT * FROM patients WHERE id = ?', (id_patient,))
    patient = cursor.fetchone()
    if not patient:
        print("Patient non trouvé.\n")
        return
    cursor.execute('DELETE FROM patients WHERE id = ?', (id_patient,))
    conn.commit()
    print(f"Patient {id_patient} supprimé.\n")

def lister_patients():
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    if not patients:
        print("Aucun patient enregistré.\n")
    else:
        for p in patients:
            print(p)
    print()

def menu():
    while True:
        print("----- Gestion des patients -----")
        print("1 - Ajouter un patient")
        print("2 - Rechercher un patient")
        print("3 - Modifier un patient")
        print("4 - Supprimer un patient")
        print("5 - Lister tous les patients")
        print("6 - Quitter")
        choix = input("Choisissez une option : ")
        print()
        if choix == "1":
            ajouter_patient()
        elif choix == "2":
            rechercher_patient()
        elif choix == "3":
            modifier_patient()
        elif choix == "4":
            supprimer_patient()
        elif choix == "5":
            lister_patients()
        elif choix == "6":
            print("Au revoir !")
            break
        else:
            print("Option invalide, réessayez.\n")

if __name__ == "__main__":
    menu()

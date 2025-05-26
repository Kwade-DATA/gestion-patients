import sqlite3
import matplotlib.pyplot as plt

def connexion():
    return sqlite3.connect('patients.db')

def creer_table():
    with connexion() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')

def ajouter_patient():
    nom = input("Nom du patient : ")
    age = int(input("Âge du patient : "))
    with connexion() as conn:
        conn.execute("INSERT INTO patients (nom, age) VALUES (?, ?)", (nom, age))
    print("Patient ajouté.")

def rechercher_patient():
    nom = input("Nom à rechercher : ")
    with connexion() as conn:
        cursor = conn.execute("SELECT * FROM patients WHERE nom LIKE ?", ('%' + nom + '%',))
        resultats = cursor.fetchall()
    if resultats:
        for patient in resultats:
            print(patient)
    else:
        print("Aucun patient trouvé.")

def modifier_patient():
    id_patient = int(input("ID du patient à modifier : "))
    nom = input("Nouveau nom : ")
    age = int(input("Nouvel âge : "))
    with connexion() as conn:
        conn.execute("UPDATE patients SET nom = ?, age = ? WHERE id = ?", (nom, age, id_patient))
    print("Patient modifié.")

def supprimer_patient():
    id_patient = int(input("ID du patient à supprimer : "))
    with connexion() as conn:
        conn.execute("DELETE FROM patients WHERE id = ?", (id_patient,))
    print("Patient supprimé.")

def lister_patients():
    with connexion() as conn:
        cursor = conn.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
    if patients:
        for p in patients:
            print(p)
    else:
        print("Aucun patient enregistré.")

def afficher_graphique():
    with connexion() as conn:
        cursor = conn.execute("SELECT age, COUNT(*) FROM patients GROUP BY age")
        data = cursor.fetchall()
    if data:
        ages = [row[0] for row in data]
        counts = [row[1] for row in data]
        plt.bar(ages, counts)
        plt.xlabel('Âge')
        plt.ylabel('Nombre de patients')
        plt.title('Répartition des patients par âge')
        plt.show()
    else:
        print("Aucune donnée pour afficher le graphique.")

def menu():
    while True:
        print("\n----- Gestion des patients -----")
        print("1 - Ajouter un patient")
        print("2 - Rechercher un patient")
        print("3 - Modifier un patient")
        print("4 - Supprimer un patient")
        print("5 - Lister tous les patients")
        print("6 - Afficher graphique des âges")
        print("7 - Quitter")
        choix = input("Choisissez une option : ")
        if choix == '1':
            ajouter_patient()
        elif choix == '2':
            rechercher_patient()
        elif choix == '3':
            modifier_patient()
        elif choix == '4':
            supprimer_patient()
        elif choix == '5':
            lister_patients()
        elif choix == '6':
            afficher_graphique()
        elif choix == '7':
            print("Au revoir!")
            break
        else:
            print("Option invalide.")

if __name__ == "__main__":
    creer_table()
    menu()

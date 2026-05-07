import sqlite3
import json
import subprocess
import datetime
import os

BDD = "monitoring.db"

def init_bd():
    """Crée les tables si elles n'existent pas"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS mesures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine TEXT,
            sonde TEXT,
            timestamp DATETIME,
            donnees JSON
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS alertes_cert (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_recuperation DATETIME,
            titre TEXT,
            lien TEXT,
            date_publication TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Base de données prête")

def execute_sonde(script):
    """Lance une sonde locale et récupère son JSON"""
    print(f"> Exécution de {script}")
    try:
        if script.endswith(".py"):
            resultat = subprocess.run(
                ["python3", script],
                capture_output=True,
                text=True,
                timeout=5
            )
        else:
            resultat = subprocess.run(
                ["./" + script],
                capture_output=True,
                text=True,
                timeout=5
            )

        if resultat.returncode == 0:
            return json.loads(resultat.stdout)
        else:
            print(f"Erreur: {resultat.stderr}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def sauvegarder_mesure(machine, sonde, donnees):
    """Sauvegarde une mesure dans SQLite"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    c.execute("""
        INSERT INTO mesures (machine, sonde, timestamp, donnees)
        VALUES (?, ?, ?, ?)
    """, (machine, sonde, datetime.datetime.now(), json.dumps(donnees)))

    conn.commit()
    conn.close()
    print(f"Mesure sauvegardée : machine={machine}, sonde={sonde}")

def sauvegarder_alerte_cert(titre, lien, date_publication):
    """Sauvegarde une alerte CERT dans SQLite"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM alertes_cert WHERE titre = ?",
        (titre,)
    )
    existe_deja = c.fetchone()[0]

    if existe_deja == 0:
        c.execute("""
            INSERT INTO alertes_cert (date_recuperation, titre, lien, date_publication)
            VALUES (?, ?, ?, ?)
        """, (datetime.datetime.now(), titre, lien, date_publication))
        conn.commit()
        print("Alerte CERT sauvegardée")
    else:
        print("Alerte déjà présente")

    conn.close()

def nettoyer():
    """Supprime les mesures de plus de 30 jours"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    date_limite = datetime.datetime.now() - datetime.timedelta(days=30)
    c.execute("DELETE FROM mesures WHERE timestamp < ?", (date_limite,))
    nb = c.rowcount

    conn.commit()
    conn.close()
    print(f"{nb} anciennes mesures supprimées")

def nettoyer_alertes_cert():
    """Supprime les alertes CERT de plus de 30 jours"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    date_limite = datetime.datetime.now() - datetime.timedelta(days=30)
    c.execute("DELETE FROM alertes_cert WHERE date_recuperation < ?", (date_limite,))
    nb = c.rowcount

    conn.commit()
    conn.close()
    print(f"{nb} anciennes alertes supprimées")

if __name__ == "__main__":
    print("\n=== MOTEUR DE STOCKAGE ===")

    init_bd()

    sondes = [
        ("bash", "sonde_bash.sh"),
        ("python", "sonde_bash.py"),
        ("processus", "sonde_processus.sh"),
    ]

    for nom, script in sondes:
        if os.path.exists(script):
            donnees = execute_sonde(script)
            if donnees:
                sauvegarder_mesure("yb", nom, donnees)
        else:
            print(f"Fichier {script} non trouvé")

    print("\n=== NETTOYAGE ===")
    nettoyer()
    nettoyer_alertes_cert()

    print("\n=== RESUME ===")
    conn = sqlite3.connect(BDD)
    c = conn.cursor()
    c.execute("SELECT machine, sonde, COUNT(*) FROM mesures GROUP BY machine, sonde")
    for machine, sonde, count in c.fetchall():
        print(f"{machine} - {sonde}: {count} mesures")
    conn.close()
                           

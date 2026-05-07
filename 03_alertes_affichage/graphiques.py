import sqlite3
import json
import pygal
import os

BDD = os.path.expanduser("~/scripts/monitoring.db")
DOSSIER_SORTIE = os.path.expanduser("~/scripts")

def nettoyer_cles(obj):
    """Nettoie les espaces inutiles dans les clés du JSON"""
    if isinstance(obj, dict):
        return {k.strip(): nettoyer_cles(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [nettoyer_cles(v) for v in obj]
    else:
        return obj

def recuperer_mesures():
    """Récupère toutes les mesures depuis la base"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    c.execute("""
        SELECT sonde, timestamp, donnees
        FROM mesures
        ORDER BY timestamp ASC
    """)

    lignes = c.fetchall()
    conn.close()
    return lignes

def extraire_donnees(lignes):
    """Extrait les valeurs utiles pour chaque sonde"""
    bash_labels = []
    bash_memory = []

    python_labels = []
    python_cpu = []

    processus_labels = []
    processus_total = []

    for sonde, timestamp, donnees_json in lignes:
        try:
            donnees = json.loads(donnees_json)
            donnees = nettoyer_cles(donnees)

            if sonde == "bash":
                valeur = donnees["sondes"]["bash"]["memory_percent"]
                bash_labels.append(timestamp[11:16])   # heure:minute
                bash_memory.append(valeur)

            elif sonde == "python":
                valeur = donnees["sondes"]["python"]["cpu_percent"]
                python_labels.append(timestamp[11:16])
                python_cpu.append(valeur)

            elif sonde == "processus":
                valeur = donnees["sonde"]["processus"]["total_processus"]
                processus_labels.append(timestamp[11:16])
                processus_total.append(valeur)

        except Exception as e:
            print(f"Erreur de lecture pour {sonde} à {timestamp} : {e}")

    return {
        "bash_labels": bash_labels,
        "bash_memory": bash_memory,
        "python_labels": python_labels,
        "python_cpu": python_cpu,
        "processus_labels": processus_labels,
        "processus_total": processus_total,
    }

def creer_graphique_bash(labels, valeurs):
    chart = pygal.Line()
    chart.title = "Evolution de la mémoire (%) - Sonde bash"
    chart.x_labels = labels
    chart.add("Mémoire %", valeurs)
    chemin = os.path.join(DOSSIER_SORTIE, "graph_bash_memory.svg")
    chart.render_to_file(chemin)
    print(f"Graphique créé : {chemin}")

def creer_graphique_python(labels, valeurs):
    chart = pygal.Line()
    chart.title = "Evolution du CPU (%) - Sonde python"
    chart.x_labels = labels
    chart.add("CPU %", valeurs)
    chemin = os.path.join(DOSSIER_SORTIE, "graph_python_cpu.svg")
    chart.render_to_file(chemin)
    print(f"Graphique créé : {chemin}")

def creer_graphique_processus(labels, valeurs):
    chart = pygal.Line()
    chart.title = "Evolution du nombre total de processus"
    chart.x_labels = labels
    chart.add("Total processus", valeurs)
    chemin = os.path.join(DOSSIER_SORTIE, "graph_processus_total.svg")
    chart.render_to_file(chemin)
    print(f"Graphique créé : {chemin}")

if __name__ == "__main__":
    print("\n=== GENERATION DES GRAPHIQUES ===")

    lignes = recuperer_mesures()
    donnees = extraire_donnees(lignes)

    if donnees["bash_memory"]:
        creer_graphique_bash(donnees["bash_labels"], donnees["bash_memory"])
    else:
        print("Aucune donnée exploitable pour la sonde bash")

    if donnees["python_cpu"]:
        creer_graphique_python(donnees["python_labels"], donnees["python_cpu"])
    else:
        print("Aucune donnée exploitable pour la sonde python")

    if donnees["processus_total"]:
        creer_graphique_processus(donnees["processus_labels"], donnees["processus_total"])
    else:
        print("Aucune donnée exploitable pour la sonde processus")

    print("\n=== FIN ===")

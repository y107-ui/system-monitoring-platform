import sqlite3
import json
import pygal

BDD = "monitoring.db"

def recuperer_mesures_python():
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    c.execute("""
        SELECT machine, donnees
        FROM mesures
        WHERE sonde = 'python'
          AND machine IS NOT NULL
        ORDER BY id ASC
    """)

    lignes = c.fetchall()
    conn.close()
    return lignes

def extraire_donnees(lignes):
    donnees_par_machine = {}

    for machine, donnees_json in lignes:
        try:
            data = json.loads(donnees_json)

            bloc_python = data["sondes "]["python "]
            cpu = bloc_python["cpu_percent "]
            mem = bloc_python["memory_percent"]

            if machine not in donnees_par_machine:
                donnees_par_machine[machine] = {
                    "cpu": [],
                    "mem": []
                }

            donnees_par_machine[machine]["cpu"].append(cpu)
            donnees_par_machine[machine]["mem"].append(mem)

        except Exception as e:
            print(f"Erreur pour la machine {machine} : {e}")

    return donnees_par_machine

def creer_graphe_cpu(donnees_par_machine):
    line_chart = pygal.Line()
    line_chart.title = "Utilisation CPU par machine"
    line_chart.x_title = "Mesures"
    line_chart.y_title = "CPU (%)"

    for machine, valeurs in donnees_par_machine.items():
        line_chart.add(machine, valeurs["cpu"])

    line_chart.render_to_file("graph_parc_cpu.svg")
    print("Graphe CPU créé : graph_parc_cpu.svg")

def creer_graphe_memoire(donnees_par_machine):
    line_chart = pygal.Line()
    line_chart.title = "Utilisation mémoire par machine"
    line_chart.x_title = "Mesures"
    line_chart.y_title = "Mémoire (%)"

    for machine, valeurs in donnees_par_machine.items():
        line_chart.add(machine, valeurs["mem"])

    line_chart.render_to_file("graph_parc_memoire.svg")
    print("Graphe mémoire créé : graph_parc_memoire.svg")

if __name__ == "__main__":
    print("=== GRAPHIQUES MULTI-MACHINES ===")

    lignes = recuperer_mesures_python()
    donnees = extraire_donnees(lignes)

    for machine, valeurs in donnees.items():
        print(f"{machine} : {len(valeurs['cpu'])} mesures CPU, {len(valeurs['mem'])} mesures mémoire")

    creer_graphe_cpu(donnees)
    creer_graphe_memoire(donnees)

    print("Fin.")

import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

BDD = BASE_DIR / "data" / "monitoring.db"
CONFIG = BASE_DIR / "config" / "config_crise.example.json"

def charger_config():
    """Charge les seuils de crise depuis le fichier JSON"""
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def nettoyer_cles(obj):
    """Supprime les espaces inutiles dans les clés JSON"""
    if isinstance(obj, dict):
        return {k.strip(): nettoyer_cles(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [nettoyer_cles(v) for v in obj]
    else:
        return obj

def recuperer_derniere_mesure(sonde):
    """Récupère la dernière mesure d'une sonde"""
    conn = sqlite3.connect(BDD)
    c = conn.cursor()

    c.execute("""
        SELECT timestamp, donnees
        FROM mesures
        WHERE sonde = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (sonde,))

    ligne = c.fetchone()
    conn.close()
    return ligne

def verifier_bash(seuils):
    ligne = recuperer_derniere_mesure("bash")
    if not ligne:
        return []

    timestamp, donnees_json = ligne
    donnees = nettoyer_cles(json.loads(donnees_json))

    alertes = []

    try:
        memoire = donnees["sondes"]["bash"]["memory_percent"]
        if memoire > seuils["memoire"]:
            alertes.append(f"[CRISE] bash - mémoire à {memoire}% (seuil {seuils['memoire']}%)")
        else:
            print(f"[OK] bash - mémoire à {memoire}%")
    except Exception as e:
        print(f"Erreur bash : {e}")

    return alertes

def verifier_python(seuils):
    ligne = recuperer_derniere_mesure("python")
    if not ligne:
        return []

    timestamp, donnees_json = ligne
    donnees = nettoyer_cles(json.loads(donnees_json))

    alertes = []

    try:
        infos = donnees["sondes"]["python"]

        cpu = infos["cpu_percent"]
        memoire = infos["memory_percent"]
        disque = infos["disk_percent"]

        if cpu > seuils["cpu"]:
            alertes.append(f"[CRISE] python - CPU à {cpu}% (seuil {seuils['cpu']}%)")
        else:
            print(f"[OK] python - CPU à {cpu}%")

        if memoire > seuils["memoire"]:
            alertes.append(f"[CRISE] python - mémoire à {memoire}% (seuil {seuils['memoire']}%)")
        else:
            print(f"[OK] python - mémoire à {memoire}%")

        if disque > seuils["disque"]:
            alertes.append(f"[CRISE] python - disque à {disque}% (seuil {seuils['disque']}%)")
        else:
            print(f"[OK] python - disque à {disque}%")

    except Exception as e:
        print(f"Erreur python : {e}")

    return alertes

def verifier_processus(seuils):
    ligne = recuperer_derniere_mesure("processus")
    if not ligne:
        return []

    timestamp, donnees_json = ligne
    donnees = nettoyer_cles(json.loads(donnees_json))

    alertes = []

    try:
        total = donnees["sonde"]["processus"]["total_processus"]
        if total > seuils["processus"]:
            alertes.append(f"[CRISE] processus - total à {total} (seuil {seuils['processus']})")
        else:
            print(f"[OK] processus - total à {total}")
    except Exception as e:
        print(f"Erreur processus : {e}")

    return alertes

if __name__ == "__main__":
    print("\n=== DETECTION DE CRISE ===")

    seuils = charger_config()

    alertes = []
    alertes.extend(verifier_bash(seuils))
    alertes.extend(verifier_python(seuils))
    alertes.extend(verifier_processus(seuils))

    print("\n=== RESULTAT ===")
    if alertes:
        print("Situation de crise détectée :")
        for alerte in alertes:
            print(alerte)
    else:
        print("Aucune situation de crise détectée.")

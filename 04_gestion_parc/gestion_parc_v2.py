import json
import subprocess
from stockage__v2 import init_bd, sauvegarder_mesure

HOST_DISTANT = "192.168.100.11"
USER_DISTANT = "younesbaz"

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout.strip()
    else:
        print(f"Erreur locale pour [{cmd}] : {r.stderr.strip()}")
        return None

def ssh(host, cmd):
    r = subprocess.run(
        f'ssh {USER_DISTANT}@{host} "{cmd}"',
        shell=True,
        capture_output=True,
        text=True
    )
    if r.returncode == 0:
        return r.stdout.strip()
    else:
        print(f"Erreur SSH pour [{cmd}] : {r.stderr.strip()}")
        return None

def collect_local():
    commandes = {
        "bash": "./sonde_bash.sh",
        "processus": "./sonde_processus.sh",
        "python": "python3 sonde_bash.py"
    }

    for sonde, cmd in commandes.items():
        sortie = run(cmd)
        if sortie:
            try:
                data = json.loads(sortie)
                sauvegarder_mesure("yb", sonde, data)
                print(f"{sonde} sauvegardée pour yb")
            except json.JSONDecodeError:
                print(f"Sortie invalide pour {sonde}")

def collect_remote():
    data = {
        "hostname": ssh(HOST_DISTANT, "hostname"),
        "uptime": ssh(HOST_DISTANT, "uptime"),
        "memory": ssh(HOST_DISTANT, "free -m | grep '^Mem:'"),
        "disk": ssh(HOST_DISTANT, "df -h / | awk 'NR==2 {print $5}'"),
        "processus": ssh(HOST_DISTANT, "ps -e --no-headers | wc -l")
    }

    if all(value is not None for value in data.values()):
        sauvegarder_mesure("partieiv", "distance", data)
        print("distance sauvegardée pour partieiv")
    else:
        print("Impossible de récupérer toutes les informations distantes")

if __name__ == "__main__":
    print("=== GESTION DU PARC ===")
    init_bd()
    collect_local()
    collect_remote()
    print("Fin.")

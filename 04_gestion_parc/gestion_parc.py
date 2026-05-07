import json
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
COLLECTE_DIR = BASE_DIR / "01_collecte"

sys.path.insert(0, str(BASE_DIR / "02_stockage"))
from stockage import init_bd, sauvegarder_mesure


HOST_DISTANT = os.getenv("REMOTE_HOST", "192.168.100.11")
USER_DISTANT = os.getenv("REMOTE_USER", "younesbaz")
PORT_DISTANT = os.getenv("REMOTE_PORT", "22")


def run(cmd):
    """Exécute une commande locale et retourne sa sortie."""
    r = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=10
    )

    if r.returncode == 0:
        return r.stdout.strip()

    print(f"Erreur locale pour [{cmd}] : {r.stderr.strip()}")
    return None


def ssh(host, cmd):
    """Exécute une commande sur une machine distante via SSH."""
    r = subprocess.run(
        [
            "ssh",
            "-p",
            PORT_DISTANT,
            f"{USER_DISTANT}@{host}",
            cmd
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    if r.returncode == 0:
        return r.stdout.strip()

    print(f"Erreur SSH pour [{cmd}] : {r.stderr.strip()}")
    return None


def collect_local():
    """Collecte les informations de la machine locale avec les sondes du projet."""
    commandes = {
        "bash": ["bash", str(COLLECTE_DIR / "sonde_bash.sh")],
        "processus": ["bash", str(COLLECTE_DIR / "sonde_processus.sh")],
        "python": ["python3", str(COLLECTE_DIR / "sonde_bash.py")]
    }

    for sonde, cmd in commandes.items():
        sortie = run(cmd)

        if sortie:
            try:
                data = json.loads(sortie)
                sauvegarder_mesure("local", sonde, data)
                print(f"{sonde} sauvegardée pour local")
            except json.JSONDecodeError:
                print(f"Sortie invalide pour {sonde}")


def collect_remote():
    """Récupère des informations système depuis une machine distante via SSH."""
    print(f"Connexion SSH vers {USER_DISTANT}@{HOST_DISTANT}:{PORT_DISTANT}")

    data = {
        "hostname": ssh(HOST_DISTANT, "hostname"),
        "uptime": ssh(HOST_DISTANT, "uptime"),
        "memory": ssh(HOST_DISTANT, "free -m | grep '^Mem:'"),
        "disk": ssh(HOST_DISTANT, "df -h / | awk 'NR==2 {print $5}'"),
        "processus": ssh(HOST_DISTANT, "ps -e --no-headers | wc -l")
    }

    if all(value is not None for value in data.values()):
        sauvegarder_mesure(HOST_DISTANT, "distance", data)
        print(f"données distantes sauvegardées pour {HOST_DISTANT}")
    else:
        print("Impossible de récupérer toutes les informations distantes")


if __name__ == "__main__":
    print("=== GESTION DU PARC ===")
    init_bd()
    collect_local()
    collect_remote()
    print("Fin.")

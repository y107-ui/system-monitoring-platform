import sqlite3
import json
import subprocess
import datetime

BDD = "monitoring.db"
HOST_DISTANT = "192.168.100.11"
def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout.strip()
    return None
def ssh(host, cmd):
    r = subprocess.run(
        f'ssh younesbaz@{host} "{cmd}"',
        shell=True, capture_output=True, text=True
    )
    return r.stdout.strip()

def save(machine, sonde, data):
    conn = sqlite3.connect(BDD)
    c = conn.cursor()
    c.execute(
        "INSERT INTO mesures (sonde, timestamp, donnees, machine) VALUES (?, ?, ?, ?)",
        (sonde, datetime.datetime.now().isoformat(), json.dumps(data), machine)
    )
    conn.commit()
    conn.close()

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
                save("yb", sonde, data)
                print(f"{sonde} sauvegardée pour yb")
            except json.JSONDecodeError:
                print(f"Sortie invalide pour {sonde}")

def collect_remote():
    data = {
        "hostname": ssh(HOST_DISTANT, "hostname"),
        "uptime": ssh(HOST_DISTANT, "uptime"),
        "memory": ssh(HOST_DISTANT, "free -m | awk 'NR==2 {print $3 \"/\" $2 \" MB\"}'"),
        "disk": ssh(HOST_DISTANT, "df -h / | awk 'NR==2 {print $5}'"),
        "processus": ssh(HOST_DISTANT, "ps -e --no-headers | wc -l")
    }

    save("partieiv", "distance", data)
    print("distance sauvegardée pour partieiv")

if __name__ == "__main__":
    print("=== GESTION DU PARC ===")
    collect_local()
    collect_remote()
    print("Fin.")
    

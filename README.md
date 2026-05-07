# System Monitoring Platform

Plateforme de monitoring système développée en **Bash** et **Python** dans le cadre d’un mini-projet d’administration des systèmes.

Le projet permet de collecter des informations système, de les stocker, de détecter des situations de crise, de générer des graphiques et de visualiser les résultats via une interface web.

---

## Objectifs

- Surveiller l’état d’une machine ou d’un parc de machines.
- Collecter des métriques système à l’aide de sondes Bash et Python.
- Stocker les mesures dans une base SQLite.
- Détecter des situations critiques à partir de seuils configurables.
- Générer des graphiques d’évolution.
- Proposer une interface web de consultation.
- Récupérer des informations depuis une machine distante via SSH.

---

## Étapes du projet

### Étape 1 — Collecte d’informations

Mise en place de sondes système permettant de récupérer des informations sur la machine surveillée :

- CPU
- mémoire
- disque
- processus
- utilisateurs connectés

Dossier concerné :

```txt
01_collecte/
```

---

### Étape 2 — Stockage et archivage

Stockage des mesures collectées dans une base SQLite.

Le moteur de stockage initialise automatiquement la base et conserve un historique des mesures.

Dossier concerné :

```txt
02_stockage/
```

Base générée localement :

```txt
data/monitoring.db
```

---

### Étape 3 — Alertes et visualisation

Détection des situations de crise à partir de seuils configurables.

Le projet permet aussi de générer des graphiques SVG à partir des mesures stockées.

Dossier concerné :

```txt
03_alertes_affichage/
```

Configuration des seuils :

```txt
config/config_crise.example.json
```

---

### Étape 4 — Gestion du parc

Récupération d’informations système depuis une machine distante via SSH.

Dossier concerné :

```txt
04_gestion_parc/
```

Le module peut être adapté avec les variables suivantes :

```txt
REMOTE_HOST
REMOTE_USER
REMOTE_PORT
```

---

### Étape 5 — Interface web

Interface web développée avec Flask pour consulter les dernières mesures et les graphiques générés.

Dossier concerné :

```txt
05_interface_web/
```

---

## Structure

```txt
system-monitoring-platform/
├── 01_collecte/              # Sondes Bash et Python
├── 02_stockage/              # Stockage SQLite et parser CERT
├── 03_alertes_affichage/     # Alertes, crise et graphiques
├── 04_gestion_parc/          # Récupération distante via SSH
├── 05_interface_web/         # Interface web Flask
├── config/                   # Configuration
├── data/                     # Base SQLite générée localement
├── logs/                     # Logs locaux
├── requirements.txt
└── README.md
```

---

## Technologies utilisées

- Bash
- Python 3
- SQLite3
- Flask
- Pygal
- psutil
- Requests
- BeautifulSoup4
- SSH

---

## Lancement

Installation des dépendances :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Collecte et stockage :

```bash
python 02_stockage/stockage.py
```

Détection de crise :

```bash
python 03_alertes_affichage/crise.py
```

Génération des graphiques :

```bash
python 03_alertes_affichage/graphiques.py
```

Interface web :

```bash
python 05_interface_web/webapp.py
```

Gestion du parc via SSH :

```bash
REMOTE_HOST=127.0.0.1 REMOTE_USER=younesbaz REMOTE_PORT=2022 python 04_gestion_parc/gestion_parc.py
```

---

## Sécurité et fichiers générés

La base SQLite, les logs, les fichiers temporaires et l’environnement virtuel ne sont pas versionnés.

Le mot de passe utilisé pour l’envoi d’e-mails doit être fourni via une variable d’environnement :

```bash
export SMTP_PASSWORD="votre_mot_de_passe_ou_token"
```

---

## Améliorations possibles

- Automatisation complète avec cron.
- Configuration de plusieurs machines distantes dans un fichier JSON.
- Amélioration de l’interface web.
- Ajout d’un système plus avancé de notification.

---

## Auteur

Younes Baziz

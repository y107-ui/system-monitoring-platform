# System Monitoring Platform

Mini-projet d’administration système réalisé en **Bash** et **Python**.

Cette plateforme permet de collecter des informations système, de stocker les mesures, de détecter des situations de crise, de générer des graphiques et d’afficher les résultats via une interface web.

## Objectifs

- Collecter des métriques système
- Stocker les données avec SQLite3
- Détecter les situations de crise
- Générer des graphiques
- Afficher les résultats avec Flask
- Récupérer des informations depuis une machine distante via SSH

## Étapes

### Étape 1 — Collecte

Sondes Bash et Python :

```txt
01_collecte/
Étape 2 — Stockage

Stockage SQLite et parser CERT :

02_stockage/

La base est générée automatiquement :

data/monitoring.db

Puis colle ce deuxième morceau :

```bash
### Étape 3 — Alertes et graphiques

Détection de crise, envoi de mail et génération de graphiques :

```txt
03_alertes_affichage/
Étape 4 — Supervision distante

Récupération d’informations depuis une machine distante via SSH :

04_gestion_parc/
Étape 5 — Interface web

Interface Flask :

05_interface_web/
Technologies
Bash
Python 3
SQLite3
Flask
Pygal
psutil
Requests
BeautifulSoup4
SSH

Puis le dernier :

```bash
## Lancement

```bash
python 02_stockage/stockage.py
python 03_alertes_affichage/crise.py
python 03_alertes_affichage/graphiques.py
python 05_interface_web/webapp.py

Interface web :

http://127.0.0.1:5000
Cron

La collecte peut être automatisée avec cron.
Elle a été testée sur une VM Linux.

Auteur

Younes Baziz

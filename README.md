# System Monitoring Platform - Mini Projet AMS

## 🚀 Objectif du projet

Ce projet consiste à développer une plateforme de supervision système en Bash et Python. Il permet de :

- Collecter des métriques système à intervalles réguliers (CPU, RAM, processus)
- Les stocker dans une base de données SQLite3
- Détecter des situations de crise et envoyer des alertes par e-mail
- Visualiser les historiques sous forme de graphiques SVG
- Gérer et superviser un parc de machines
- Consulter les résultats depuis une interface web Flask

---

## 🧰 Technologies utilisées

- **Python 3** (collecte, stockage, analyse, interface web)
- **Bash** (sondes système)
- **SQLite3** (persistance des métriques dans `data/monitoring.db`)
- **Flask** (interface web)
- **Pygal** (génération de graphiques SVG)
- **psutil** (métriques système)
- **BeautifulSoup4 + Requests** (scraping CERT-FR)
- **SMTP** (envoi d'alertes e-mail)

---

## 🔎 Fonctionnalités réalisées

### ✅ Étape 1 : Collecte d'informations

- `sonde_bash.sh` — collecte mémoire via commandes Bash
- `sonde_bash.py` — collecte CPU/RAM via psutil (Python)
- `sonde_processus.sh` — collecte du nombre de processus actifs

### ✅ Étape 2 : Stockage et archivage

- `stockage.py` — insertion des métriques dans la base SQLite3
- `cert_parser.py` — récupération et stockage des bulletins CERT-FR

### ✅ Étape 3 : Alertes et affichage

- `crise.py` — détection automatique des crises (seuils configurables)
- `alerte_mail.py` — envoi d'un e-mail en cas de crise
- `graphiques.py` — génération des graphiques SVG CPU/mémoire
- `graphiques_parc.py` — génération des graphiques SVG pour le parc

### ✅ Étape 4 : Gestion du parc

- `gestion_parc.py` — supervision et collecte sur un parc de machines

### ✅ Étape 5 : Interface Web (Flask)

- `webapp.py` — dashboard Flask affichant les graphiques SVG
- Graphiques disponibles : CPU Python, mémoire Bash, processus, parc CPU, parc mémoire

---

## 🔧 Utilisation

### ⚡ Collecte des métriques :

    bash 01_collecte/sonde_bash.sh
    bash 01_collecte/sonde_processus.sh
    python3 01_collecte/sonde_bash.py

### 🗄️ Stockage en base :

    python3 02_stockage/stockage.py

### 📡 Parsing CERT-FR :

    python3 02_stockage/cert_parser.py

### 🚨 Détection de crise :

    python3 03_alertes_affichage/crise.py

### 📧 Envoi d'alerte mail :

    python3 03_alertes_affichage/alerte_mail.py

### 📈 Génération des graphiques :

    python3 03_alertes_affichage/graphiques.py
    python3 03_alertes_affichage/graphiques_parc.py

### 🖥️ Gestion du parc :

    python3 04_gestion_parc/gestion_parc.py

### 🌐 Interface Web :

    python3 05_interface_web/webapp.py

Puis accéder sur : http://127.0.0.1:5000

---

## ⚙️ Configuration

Copier et adapter le fichier de configuration :

    cp config/config_crise.example.json config/config_crise.json

Les seuils (CPU, RAM, disque) sont modifiables dans ce fichier.
Le template d'e-mail est personnalisable dans `config/template_mail.txt`.

---

## ⏱️ Automatisation avec Cron

    crontab -e

Exemple toutes les 5 minutes :

    */5 * * * * /usr/bin/python3 /chemin/vers/02_stockage/stockage.py >> /var/log/monitoring.log 2>&1

---

## 🛠️ Structure du projet

    ams-monitoring/
    ├── 01_collecte/
    │   ├── sonde_bash.sh
    │   ├── sonde_bash.py
    │   └── sonde_processus.sh
    ├── 02_stockage/
    │   ├── stockage.py
    │   └── cert_parser.py
    ├── 03_alertes_affichage/
    │   ├── crise.py
    │   ├── alerte_mail.py
    │   ├── graphiques.py
    │   └── graphiques_parc.py
    ├── 04_gestion_parc/
    │   └── gestion_parc.py
    ├── 05_interface_web/
    │   ├── static/
    │   ├── templates/index.html
    │   └── webapp.py
    ├── config/
    │   ├── config_crise.example.json
    │   └── template_mail.txt
    ├── data/
    │   └── monitoring.db
    └── requirements.txt

---

## 🏆 Remarques

- Tous les scripts ont été testés sur une VM Linux (Debian/Ubuntu)
- Les seuils de crise sont configurables via `config/config_crise.example.json`
- Le projet couvre la chaîne complète : collecte → stockage → alerte → visualisation

---

## 🎓 Auteur

- Younes Baziz - Informatique - CERI - 2025

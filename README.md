# System Monitoring Platform - Mini Projet AMS

## 🚀 Objectif du projet

Ce projet consiste à développer une plateforme de supervision système réalisée en Bash et Python. Il permet de :

- Collecter des métriques système à intervalles réguliers (CPU, RAM, disque, réseau)
- Les stocker dans une base de données SQLite3
- Détecter des situations de crise et envoyer des alertes par e-mail
- Afficher les historiques sous forme de graphiques
- Superviser des machines distantes via SSH
- Consulter les résultats via une interface web Flask

---

## 🧰 Technologies utilisées

- **Python 3** (collecte, stockage, analyse, interface web)
- **Bash** (sondes système légères)
- **SQLite3** (stockage des métriques)
- **Flask** (interface web)
- **Pygal** (génération de graphiques SVG)
- **psutil** (métriques système Python)
- **Paramiko / SSH** (supervision distante)
- **BeautifulSoup4 + Requests** (parsing bulletins CERT-FR)
- **SMTP** (envoi d'alertes e-mail)

---

## 🔎 Fonctionnalités réalisées

### ✅ Étape 1 : Collecte d'informations

- Sonde CPU, RAM, disque, réseau via **psutil** (Python)
- Sonde système complémentaire en **Bash**

### ✅ Étape 2 : Stockage et archivage

- Insertion des métriques dans une base **SQLite3**
- Parseur **CERT-FR** : récupération et stockage des bulletins de sécurité

### ✅ Étape 3 : Alertes et affichage

- Détection automatique des crises (seuils configurables sur CPU, RAM, disque)
- Envoi d'un e-mail à l'administrateur en cas de crise (avec horodatage et détails)
- Génération de graphiques **SVG** avec Pygal

### ✅ Étape 4 : Supervision distante

- Connexion **SSH** à une machine distante
- Récupération des métriques à distance

### ✅ Étape 5 : Interface Web (Flask)

- Dashboard web affichant les graphiques SVG
- Consultation des dernières métriques et alertes

---

## 🔧 Utilisation

### ⚡ Collecte et stockage :

    python3 02_stockage/stockage.py

### 📡 Parsing CERT-FR :

    python3 02_stockage/cert_parser.py

### 🚨 Détection de crise :

    python3 03_alertes_affichage/crise.py

### 📈 Génération des graphiques :

    python3 03_alertes_affichage/graphiques.py

### 🔐 Supervision SSH distante :

    python3 04_gestion_parc/supervision_ssh.py

### 🌐 Interface Web :

    python3 05_interface_web/webapp.py

Puis accéder sur : http://127.0.0.1:5000

---

## ⏱️ Automatisation avec Cron

La collecte peut être automatisée avec cron (testée sur VM Linux) :

    crontab -e

Exemple pour une collecte toutes les 5 minutes :

    */5 * * * * /usr/bin/python3 /chemin/vers/02_stockage/stockage.py >> /var/log/monitoring.log 2>&1

---

## 🛠️ Scripts principaux

- `01_collecte/` — sondes Bash et Python
- `02_stockage/stockage.py` — insertion SQLite
- `02_stockage/cert_parser.py` — parsing CERT-FR
- `03_alertes_affichage/crise.py` — détection de crise + envoi mail
- `03_alertes_affichage/graphiques.py` — génération graphiques
- `04_gestion_parc/supervision_ssh.py` — supervision distante
- `05_interface_web/webapp.py` — interface Flask

---

## 🏆 Remarques

- Tous les scripts ont été testés sur une VM Linux (Debian/Ubuntu)
- Les seuils de crise sont configurables directement dans `crise.py`
- Le projet couvre l'ensemble de la chaîne : collecte → stockage → alerte → visualisation

---

## 🎓 Auteur

- Younes Baziz - L2/L3 Informatique - 2025

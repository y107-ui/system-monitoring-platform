# System Monitoring Platform - Mini Projet AMS

## 🚀 Objectif du projet

Ce projet consiste à développer une plateforme de supervision système en Bash et Python. Il permet de :

- Collecter des métriques système à intervalles réguliers (CPU, RAM, disque, réseau)
- Les stocker dans une base de données SQLite3
- Détecter des situations de crise et envoyer des alertes par e-mail
- Visualiser les historiques sous forme de graphiques SVG
- Superviser des machines distantes via SSH
- Consulter les résultats depuis une interface web Flask

---

## 🧰 Technologies utilisées

- **Python 3** (collecte, stockage, analyse, interface web)
- **Bash** (sondes système légères)
- **SQLite3** (persistance des métriques)
- **Flask** (interface web)
- **Pygal** (génération de graphiques SVG)
- **psutil** (métriques système)
- **Paramiko** (connexion SSH distante)
- **BeautifulSoup4 + Requests** (scraping CERT-FR)
- **SMTP** (envoi d'alertes e-mail)

---

## 🔎 Fonctionnalités réalisées

### ✅ Étape 1 : Collecte d'informations

- Sonde CPU, RAM, disque, réseau via psutil (Python)
- Sonde complémentaire en Bash

### ✅ Étape 2 : Stockage et archivage

- Insertion des métriques dans une base SQLite3
- Parseur CERT-FR : récupération et stockage des bulletins de sécurité

**Options choisies :**
- Format SQLite3 pour les requêtes et l'historique
- Historique consultable depuis l'interface web

### ✅ Étape 3 : Alertes et affichage

- Détection automatique des crises (seuils configurables : CPU, RAM, disque)
- Envoi d'un e-mail à l'administrateur en cas de crise (horodatage + détails)
- Génération automatique de graphiques SVG avec Pygal

**Options choisies :**
- Seuils de crise configurables dans `crise.py`

### ✅ Étape 4 : Supervision distante

- Connexion SSH à une machine distante via Paramiko
- Récupération des métriques à distance et stockage en base

### ✅ Étape 5 : Interface Web (Flask)

- Dashboard affichant les graphiques SVG
- Consultation des dernières métriques collectées

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

La collecte est automatisable via cron (testé sur VM Linux) :

    crontab -e

Exemple pour une collecte toutes les 5 minutes :

    */5 * * * * /usr/bin/python3 /chemin/vers/02_stockage/stockage.py >> /var/log/monitoring.log 2>&1

---

## 🛠️ Scripts principaux

- `01_collecte/` — sondes Bash et Python
- `02_stockage/stockage.py` — insertion SQLite
- `02_stockage/cert_parser.py` — parsing CERT-FR
- `03_alertes_affichage/crise.py` — détection de crise + envoi mail
- `03_alertes_affichage/graphiques.py` — génération graphiques SVG
- `04_gestion_parc/supervision_ssh.py` — supervision SSH distante
- `05_interface_web/webapp.py` — dashboard Flask

---

## 🏆 Remarques

- Tous les scripts ont été testés sur une VM Linux (Debian/Ubuntu)
- Les seuils de crise sont configurables directement dans `crise.py`
- Le projet couvre la chaîne complète : collecte → stockage → alerte → visualisation

---

## 🎓 Auteur

- Younes Baziz - Informatique - CERI - 2025

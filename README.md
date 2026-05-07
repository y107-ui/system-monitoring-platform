# 🖥️ System Monitoring Platform

> Plateforme de supervision système développée en **Bash** et **Python** — collecte de métriques, stockage SQLite, détection de crise, supervision SSH et interface web Flask.


---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Architecture du projet](#-architecture-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Automatisation avec Cron](#-automatisation-avec-cron)
- [Structure des fichiers](#-structure-des-fichiers)
- [Technologies](#-technologies)
- [Auteur](#-auteur)

---

## 📌 Présentation

Cette plateforme est un mini-projet d'administration système conçu pour superviser des machines Linux locales ou distantes. Elle est divisée en cinq modules indépendants et progressifs : collecte de données brutes, persistance en base, détection d'anomalies, supervision à distance via SSH, et restitution via une interface web.

Elle a été développée et testée sur une **machine virtuelle Linux (Debian/Ubuntu)**.

---

## 🏗️ Architecture du projet

'''
system-monitoring-platform/
│
├── 01_collecte/             # Sondes système (Bash + Python)
│   ├── sonde.sh             # Collecte via commandes système Bash
│   └── sonde.py             # Collecte via psutil (CPU, RAM, disque, réseau)
│
├── 02_stockage/             # Persistance des données
│   ├── stockage.py          # Insertion des métriques dans SQLite
│   └── cert_parser.py       # Parsing des bulletins de sécurité CERT-FR
│
├── 03_alertes_affichage/    # Détection de crise et visualisation
│   ├── crise.py             # Seuils d'alerte + envoi d'e-mail
│   └── graphiques.py        # Génération de graphiques SVG avec Pygal
│
├── 04_gestion_parc/         # Supervision distante
│   └── supervision_ssh.py   # Connexion SSH et récupération de métriques distantes
│
├── 05_interface_web/        # Dashboard web
│   └── webapp.py            # Application Flask (routes + affichage)
│
├── config/                  # Fichiers de configuration
├── requirements.txt         # Dépendances Python
├── .gitignore
└── README.md
'''

---

## ✅ Fonctionnalités

| Module | Fonctionnalité |
|---|---|
| 🔍 Collecte | Métriques CPU, RAM, disque, réseau via Bash et psutil |
| 🗄️ Stockage | Base SQLite3 — insertion et requêtage des données |
| 📡 CERT-FR | Scraping et parsing des bulletins de sécurité CERT-FR |
| 🚨 Alertes | Détection de seuils critiques + notification par e-mail |
| 📊 Graphiques | Génération automatique de graphiques SVG (Pygal) |
| 🔐 SSH | Supervision de machines distantes via Paramiko/SSH |
| 🌐 Interface web | Dashboard Flask consultable via navigateur |

---

## 🔧 Prérequis

- **Python 3.8+**
- **pip**
- **SQLite3** (inclus dans Python standard)
- Accès SSH à une machine distante (optionnel, pour le module 04)
- Un serveur SMTP configuré (optionnel, pour les alertes mail)
- Système : **Linux** (testé sur VM Debian/Ubuntu)

---

## 🚀 Installation

### 1. Cloner le dépôt

'''bash
git clone https://github.com/y107-ui/system-monitoring-platform.git
cd system-monitoring-platform
'''

### 2. Créer un environnement virtuel (recommandé)

'''bash
python3 -m venv venv
source venv/bin/activate
'''

### 3. Installer les dépendances

'''bash
pip install -r requirements.txt
'''

---

## ▶️ Utilisation

### Étape 1 — Collecte et stockage des métriques

Lance la sonde et insère les données en base :

'''bash
python3 02_stockage/stockage.py
'''

### Étape 2 — Parsing CERT-FR (optionnel)

Récupère et stocke les derniers bulletins de sécurité :

'''bash
python3 02_stockage/cert_parser.py
'''

### Étape 3 — Détection de crise

Analyse les métriques stockées et envoie une alerte si un seuil est dépassé :

'''bash
python3 03_alertes_affichage/crise.py
'''

### Étape 4 — Génération des graphiques

Produit les graphiques SVG à partir des données en base :

'''bash
python3 03_alertes_affichage/graphiques.py
'''

### Étape 5 — Supervision SSH distante (optionnel)

Récupère les métriques d'une machine distante via SSH :

'''bash
python3 04_gestion_parc/supervision_ssh.py
'''

### Étape 6 — Lancement de l'interface web

'''bash
python3 05_interface_web/webapp.py
'''

Accès via navigateur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⏱️ Automatisation avec Cron

Pour automatiser la collecte toutes les 5 minutes, ajoute cette entrée dans ta crontab :

'''bash
crontab -e
'''

Puis ajoute la ligne suivante :

'''
*/5 * * * * /usr/bin/python3 /chemin/vers/system-monitoring-platform/02_stockage/stockage.py >> /var/log/monitoring.log 2>&1
'''

---

## 🧰 Technologies

| Outil | Usage |
|---|---|
| **Python 3** | Logique principale, collecte, traitement |
| **Bash** | Sondes système légères |
| **SQLite3** | Stockage local des métriques |
| **Flask** | Serveur web et dashboard |
| **Pygal** | Génération de graphiques SVG |
| **psutil** | Collecte de métriques système |
| **Paramiko / SSH** | Supervision distante |
| **BeautifulSoup4** | Scraping des bulletins CERT-FR |
| **Requests** | Requêtes HTTP pour le parsing CERT |

---

## 👤 Auteur

**Younes Baziz**
Projet réalisé dans le cadre d'un cursus d'administration système.

---

> *Ce projet est à vocation pédagogique. Il illustre une chaîne complète de supervision système : de la collecte brute à la restitution web, en passant par la persistance et la détection d'anomalies.*

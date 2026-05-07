# System Monitoring Platform

Mini-projet d'administration systeme realise en Bash et Python.

Cette plateforme permet de collecter des informations systeme, de stocker les mesures, de detecter des situations de crise, de generer des graphiques et d'afficher les resultats via une interface web.

## Objectifs

- Collecter des metriques systeme
- Stocker les donnees avec SQLite3
- Detecter les situations de crise
- Generer des graphiques
- Afficher les resultats avec Flask
- Recuperer des informations depuis une machine distante via SSH

## Etapes

1. Collecte : sondes Bash et Python dans 01_collecte/
2. Stockage : base SQLite et parser CERT dans 02_stockage/
3. Alertes et graphiques : detection de crise, mail et graphiques dans 03_alertes_affichage/
4. Supervision distante : recuperation via SSH dans 04_gestion_parc/
5. Interface web : application Flask dans 05_interface_web/

## Technologies

Bash, Python 3, SQLite3, Flask, Pygal, psutil, Requests, BeautifulSoup4, SSH.

## Lancement

Collecte et stockage :
python 02_stockage/stockage.py

Detection de crise :
python 03_alertes_affichage/crise.py

Generation des graphiques :
python 03_alertes_affichage/graphiques.py

Interface web :
python 05_interface_web/webapp.py

Adresse web locale :
http://127.0.0.1:5000

## Cron

La collecte peut etre automatisee avec cron.
Elle a ete testee sur une VM Linux.

## Auteur

Younes Baziz

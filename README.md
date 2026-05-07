# AMS Monitoring

Plateforme de monitoring d’un parc informatique réalisée en Bash et Python.

## Fonctionnalités

- Collecte d’informations système
- Stockage des mesures avec SQLite3
- Détection de situations de crise
- Alertes par e-mail
- Génération de graphiques
- Gestion de plusieurs machines
- Interface web Flask

## Structure

- `01_collecte/` : sondes Bash et Python pour récupérer les informations système
- `02_stockage/` : stockage SQLite3 et récupération des alertes CERT
- `03_alertes_affichage/` : détection de crise, e-mail et graphiques
- `04_gestion_parc/` : récupération des données de plusieurs machines
- `05_interface_web/` : interface web Flask
- `config/` : fichiers de configuration et template mail
- `data/` : données générées localement
- `logs/` : fichiers de logs générés localement

## Base de données

Le projet utilise SQLite3.

La base `monitoring.db` n’est pas versionnée sur GitHub.
Elle est créée automatiquement au lancement du module de stockage.

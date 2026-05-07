
import sqlite3
import json 
import subprocess
import datetime
import os


BDD = "monitoring.db"
DOSSIER_SONDES = "..."

def init_bd():
   """Cée la table si elle n'existe pas """
   conn = sqlite3.connect(BDD)
   c = conn.cursor()
   c.execute('''CREATE TABLE IF NOT EXISTS mesures
               (id INTEGER PRIMARY KEY,
                sonde TEXT,
                timestamp DATETIME,
                donnees JSON)''')
   conn.commit()
   c.execute("""
       CREATE TABLE IF NOT EXISTS alertes_cert(
           id INTEGER PRIMARY KEY  AUTOINCREMENT,
           date_recuperation DATETIME,
           titre TEXT,
           lien  TEXT,
           date_publication TEXT
      )
   """)
   conn.close()
   print(" Base de données prete")
def execute_sonde(script):
  """Lancer une sonde et récupère son JSON"""
  print(f"   > Exécution de {script}")
  try:
       resultat = subprocess.run(['./' + script],
                                capture_output=True,  
                                text=True,
                                timeout=5)
       if resultat.returncode == 0:
             return json.loads(resultat.stdout)
       else:
           print (f"  Erreur: {resultat.stderr}")
           return  None
  except Exception as e:
           print (f"  Exception: {e}")
           return None

def sauvgarder(sonde,donnees):
   """Sauvgarder dans SQLite"""
   conn = sqlite3.connect(BDD)
   c = conn.cursor()
   c.execute("INSERT INTO mesures (sonde, timestamp, donnees, machine) VALUES (?, ?, ?, ?)",
          (sonde, datetime.datetime.now(), json.dumps(donnees), "yb"))
   conn.commit()
   conn.close()
   print (f"   Sauvegardé dans SQLite")
def sauvgarder_alerte_cert(titre, lien ,date_publication):
    """ Sauvgarder une alerte dans sqlLite"""
    conn  =  sqlite3.connect(BDD)
    c = conn.cursor()
    c.execute(
           "SELECT COUNT(*) FROM alertes_cert  WHERE titre = ?",
            (titre,)
    )
    existe_deja = c.fetchone()[0]
    if existe_deja ==0:
         c.execute("""
             INSERT INTO alertes_cert (date_recuperation, titre, lien, date_publication)
             VALUES(?, ?, ?, ?)
         """, (datetime.datetime.now(), titre, lien , date_publication))
         conn.commit()
         print (" Alerte CERT sauvgardée")
    else:
        print("Alerte deja présente")
    conn.close()
def nettoyer():
      """Supprime les données de plus de  30 jours"""
      conn = sqlite3.connect(BDD)
      c = conn.cursor()
      date_limite = datetime.datetime.now() - datetime.timedelta(days=30) 
      c.execute("DELETE FROM mesures WHERE timestamp < ?", (date_limite,))
      nb = c.rowcount
      conn.commit()
      conn.close()
      print (f"   {nb} anciennes mesures supprimées")

def nettoyer_alertes_cert():
       """supprimer les alertes cert de plus de 30 jouirs"""
       conn=sqlite3.connect(BDD)
       c = conn.cursor()
       date_limite = datetime.datetime.now() - datetime.timedelta(days=30)
       c.execute("DELETE FROM alertes_cert WHERE date_recuperation < ?",(date_limite,))
       nb=c.rowcount
       conn.commit()
       conn.close()
       print (f"{nb} anciennes alertes supprimées")
if __name__=="__main__":
   print("\n=== MOTEUR DE STOCKAGE ===")

   init_bd()
   sondes = [
     ("bash", "sonde_bash.sh"),
     ("python" , "sonde_bash.py"),
     ("processus", "sonde_processus.sh"),
   ]
   for nom, script in sondes:
       if os.path.exists(script):
           donnees = execute_sonde(script)
           if donnees: 
            sauvgarder(nom, donnees)
       else:
          print ( f"   Fichier {script} non trouvé")

   print ("\n===NETTOYAGE ===")
   nettoyer()
   nettoyer_alertes_cert()

   print ("\n===RESUME ===")
   conn = sqlite3.connect(BDD)
   c = conn.cursor()
   c.execute("SELECT sonde, COUNT(*) FROM mesures GROUP BY sonde")
   for sonde, count in c.fetchall():
           print (f"  {sonde}: {count} mesures")
   conn.close()         

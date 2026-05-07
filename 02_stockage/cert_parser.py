#!/usr/bin/env  python3
import urllib.request
import datetime
import  xml.etree.ElementTree  as ET
from stockage import init_bd, sauvegarder_alerte_cert
URL_CERT = "https://www.cert.ssi.gouv.fr/alerte/feed/"


print ("\n" + "="*50)
print ("   PARSEUR CERT - ALERTES DE SÉCURITÉ")
print ("="*50 + "\n")


print ("Recupiration du flux RSS")
try:
        with urllib.request.urlopen(URL_CERT, timeout=10) as responses:
           contenu = responses.read()
        print ( " FLux récupérer avec succès   !\n")
        print ("Extraction du la  dernier alerte...")
        try:

            racine = ET.fromstring(contenu)
            print("Tag racine  :", racine.tag)
            for enfant in racine:
                 print ("Enfant racine :", enfant.tag)
                 for sous_enfant in enfant[:5]:
                     print("->", sous_enfant.tag)
        except ET.ParserError as e:
            print ("Ereur XML:", e)
            print ("le contenu récupéré n'est pas un  flux RSS/XML valide")
            print (contenu.decode(errors="ignore")[ :500])
            exit()

        derniere_alerte = racine.find(".//item")
        if  derniere_alerte is not None :
             titre_elem = derniere_alerte.find("title")
             lien_elem = derniere_alerte.find("link")
             date_elem = derniere_alerte.find("pubDate")
             titre = titre_elem.text.strip() if titre_elem is not None and  titre_elem.text  else "Titre inconnu"
             lien = lien_elem.text.strip() if lien_elem is not None and lien_elem.text else " lien inconnue"
             date_publication = date_elem.text.strip() if date_elem is not None and date_elem.text else "Date inconnu"

             print (" Alert trouvée !\n")
             print (" Dernier alerte :")
             print (" titre :", titre[:80] + "..." if len(titre) >80 else titre)
             print ("   Date :", date_publication)
             print ("   lien", lien)
             print ()
             print (" Envoie au moteur de stockage  ")
             init_bd()
             sauvegarder_alerte_cert(titre, lien, date_publication)
        else:
               print("Aucun alerte est trouvé dans le flux") 



except Exception as e:
         print("Erreur :",e)
print ("\n" + "="*50)
print (" Parseur terminé")
print ("="*50)


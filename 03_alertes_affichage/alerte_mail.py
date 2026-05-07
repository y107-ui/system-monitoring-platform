import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from crise import charger_config, verifier_bash, verifier_python, verifier_processus

TEMPLATE = os.path.expanduser("~/scripts/template_mail.txt")

# À adapter
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EXPEDITEUR = "younes.baziz@alumni.univ-avignon.fr"   # ou @univ-avignon.fr
MOT_DE_PASSE = "HFo-JSa-ZGJ-QVu"
DESTINATAIRE = "younes.baziz@alumni.univ-avignon.fr"
SUJET = "Alerte supervision - situation de crise"

def charger_template():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        return f.read()

def recuperer_alertes():
    seuils = charger_config()
    alertes = []
    alertes.extend(verifier_bash(seuils))
    alertes.extend(verifier_python(seuils))
    alertes.extend(verifier_processus(seuils))
    return alertes

def envoyer_mail(alertes):
    contenu_template = charger_template()
    contenu = contenu_template.replace("{alertes}", "\n".join(alertes))

    message = MIMEMultipart()
    message["From"] = EXPEDITEUR
    message["To"] = DESTINATAIRE
    message["Subject"] = SUJET

    message.attach(MIMEText(contenu, "plain", "utf-8"))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as serveur:
      serveur.login(EXPEDITEUR, MOT_DE_PASSE)
      serveur.send_message(message)

    print("E-mail envoyé avec succès.")

if __name__ == "__main__":
    print("\n=== ENVOI D'ALERTE MAIL ===")

    alertes = recuperer_alertes()

    if alertes:
        print("Crise détectée, préparation du mail...")
        envoyer_mail(alertes)
    else:
        print("Aucune crise détectée, aucun mail envoyé.")

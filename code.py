from flask import Flask, request, render_template, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "hernox"  # Nécessaire pour utiliser flash messages

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "vlzderoblox@gmail.com"  # Votre adresse e-mail
EMAIL_PASSWORD = "owms keas qyfn wnfj"  # Ce mot de passe généré automatiquement par Google.

# Liste des e-mails blacklistés
BLACKLISTED_EMAILS = {"gabix380@gmail.com", "chevalieralex49@gmail.com"}

def envoyer_email(destinataire, sujet, contenu):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = destinataire
        msg['Subject'] = sujet
        msg.attach(MIMEText(contenu, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"E-mail envoyé à {destinataire}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        nombre = int(request.form['nombre'])
        message = request.form['message']

        # Vérifier si l'email est dans la blacklist
        if email in BLACKLISTED_EMAILS:
            flash(f"L'adresse {email} est blacklistée. Aucun e-mail ne sera envoyé.", "danger")
            return redirect(url_for('index'))

        # Envoi des e-mails
        for i in range(nombre):
            envoyer_email(email, f"Message {i+1}", message)

        flash(f"{nombre} e-mails ont été envoyés à {email}.", "success")
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

import smtplib, uuid, ssl
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail(to, sub, body):
    frm = "sah.abesec"
    password = "tnyvlbbomcygibwm"
    mail = MIMEMultipart("alternative")
    mail["From"] = frm
    mail["To"] = to
    mail["Subject"] = sub
    mail.attach(MIMEText(body, "html", "utf-8"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context= context) as server:
        server.login(frm, password)
        try:
            server.sendmail(frm, to, mail.as_string().encode())
        except:
            print("failed to send to", to)
            raise


a = datetime.now()
b = timedelta(hours=2)
print(a - b)
import smtplib, ssl
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# PUT YOUR EMAIL AND APP-PASSWORD HERE
sender_email = os.getenv('MY_MAIL')
hashed_password = os.getenv('HASH')
google_password = os.getenv('APP_PASSWORD')

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import hashlib

hkdf = HKDF(
    algorithm=hashes.SHA256(), 
    length=32,
    salt=None,  
    info=None,  
    backend=default_backend()
)

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import easygui
from os.path import basename

subject = "Default Subject"
body = "Defaault content"

def read_mail():
    subject = input("What is the subject of the mail? ")
    content_file = None
    while content_file is None:
        content_file = easygui.fileopenbox("Select the content of the message")
    f = open(content_file, "r")
    body = f.read() 
    return subject,body

def read_csv(recipients):
    csv_file = easygui.fileopenbox("Select the csv file")
    if csv_file is None:
        return False
    with open('mails.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                recipients.append(row[0])
            line_count += 1
        #print(f'Processed {line_count - 1} lines.')
    return True

def send_email(subject, body, sender, receiver, cc_recipients, bcc_recipients, password, attachments):
    # msg = MIMEText(body)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] =  receiver
    msg['Cc'] = ', '.join(cc_recipients)
    msg['Bcc'] = ', '.join(bcc_recipients)
    msg.attach(MIMEText(body))
    if len(attachments) > 0:
        for f in attachments:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.send_message(msg,sender_email)
    print("Message sent!")

def check_password(inserted_pw):
    hasher = hashlib.sha256()
    hasher.update(inserted_pw.encode())
    pw_hash = str(hasher.hexdigest())
    return pw_hash == hashed_password

def get_google_app_pw(user_password):
    fernet_secret_string = user_password + user_password
    fernet_key = base64.urlsafe_b64encode(hkdf.derive(fernet_secret_string.encode()))
    fernet = Fernet(fernet_key)
    result= fernet.decrypt(google_password.encode()).decode()
    return result

if __name__ == "__main__":
    if not os.path.exists(".env"):
        print("No \".env\" file found. Please set up your \".env\" file by running the \"setup.py\" file or by starting the main app if you prefer to use the gui.")
    inserted_pw = input("Insert your password to log into the client: ")
    if not check_password(inserted_pw):
        print("Incorrect password")
        quit(0)
    google_app_pw = get_google_app_pw(inserted_pw)
    recipients = []
    subject,body = read_mail()
    read_csv(recipients)
    print(f"""
From: {sender_email}
Bcc: {', '.join(recipients)}
Subject:{subject}

{body}
""")
    confirm = input("Confirm? [y/n]: ")
    if(confirm == 'y' or confirm == 'Y'):
        attachments=[]
        wants_to_attach = input("Would you like to add some attachments? [y/n]: ")
        while(wants_to_attach == 'y' or wants_to_attach == 'Y'):
            new_attachment = easygui.fileopenbox("Select the file to attach")
            if(new_attachment is None):
                print("You did not select any file")
            if(new_attachment in attachments):
                print("You alreasy attached this file.")
            else:
                attachments.append(new_attachment)
            print("Current attachments: ")
            for att in attachments:
                print(att)
            wants_to_attach = input("Would you like to add some more attachments? [y/n]: ")
        if len(attachments) > 0:
            print("Attachments: ")
            for att in attachments:
                print(att)
        confirm = input("Confirm sending? [y/n]: ")
        if(confirm == 'y' or confirm == 'Y'):
            send_email(subject, body, sender_email, sender_email, recipients, [], google_app_pw, attachments)
        else:
            print("Operation cancelled...")
    else:
        print("Operation cancelled...")
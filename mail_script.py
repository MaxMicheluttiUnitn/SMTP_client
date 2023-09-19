import smtplib, ssl
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# PUT YOUR EMAIL AND APP-PASSWORD HERE
sender_email = os.getenv('MY_MAIL')
password = os.getenv('APP_PASSWORD')

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import easygui
from os.path import basename

subject = "Default Subject"
body = "Defaault content"

def read_mail():
    subject = input("What is the subject of the mail? ")
    content_file = easygui.fileopenbox("Select the content of the message")
    f = open(content_file, "r")
    body = f.read() 
    return subject,body

def read_csv(recipients):
    csv_file = easygui.fileopenbox("Select the csv file")
    with open('mails.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                recipients.append(row[0])
            line_count += 1
        print(f'Processed {line_count - 1} lines.')

def send_email(subject, body, sender, recipients, password, attachments):
    # msg = MIMEText(body)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] =  sender
    msg['Bcc'] = ', '.join(recipients)
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

if __name__ == "__main__":
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
            if(new_attachment in attachments):
                print("You alreasy attached this file.")
            else:
                attachments.append(new_attachment)
            print("Current attachments: ")
            for att in attachments:
                print(att)
            wants_to_attach = input("Would you like to add some more attachments? [y/n]: ")
        print("Attachments: ")
        for att in attachments:
            print(att)
        confirm = input("Confirm? [y/n]: ")
        if(confirm == 'y' or confirm == 'Y'):
            send_email(subject, body, sender_email, recipients, password, attachments)
        else:
            print("Operation cancelled...")
    else:
        print("Operation cancelled...")
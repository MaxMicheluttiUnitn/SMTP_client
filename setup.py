from getpass import getpass
import re
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import hashlib
import tkinter as tk
import window

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def check(email):
    global regex
    if(re.fullmatch(regex, email)):
        return True
    return False

hkdf = HKDF(
    algorithm=hashes.SHA256(), 
    length=32,
    salt=None,  
    info=None,  
    backend=default_backend()
)

def terminal_setup():
    global hkdf
    try:
        f = open(".env", "x") 
    except:
        print(".env file already generated. Delete old file to restart the setup.")
        return
    mail="no"
    while not check(mail):
        mail = input("Please insert the Gmail compatible e-mail that you want to use: ")
    password = "yes"
    password_repeat = "no"
    already_once = False
    print("\n\nTo use this application you need an APP PASSWORD for Gmail.\nIf you do not have one, you can generate it from your GOOGLE ACCOUNT.\nYour password will be encrypted and saved on this device and will only be used to send emails through this client.")
    while password != password_repeat or password == "":
        if not already_once:
            already_once = True
        else:
            print("Gmail App Passwords did not match.")
        password = getpass(prompt="Insert the Gmail App Password: ")
        password_repeat = getpass(prompt="Repeat the Gmail App Password: ")
    application_password = "yes"
    application_password_copy = "no"
    already_once = False
    print("\n\nSelect a password for the mail client, the password must be at least 5 character long.\nIt will be used to encode and ecrypt your app password, as well as giving you access to the client.")
    while application_password != application_password_copy or application_password=="" or len(application_password)<5:
        if not already_once:
            already_once = True
        else:
            if application_password == "" or len(application_password)<5:
                print("The password must be at least 5 characters long.")
            else:
                print("Client passwords did not match.")
        application_password = getpass(prompt="Insert client password: ")
        application_password_copy = getpass(prompt="Repeat client password: ")
    fernet_secret_string = application_password + application_password_copy
    fernet_key = base64.urlsafe_b64encode(hkdf.derive(fernet_secret_string.encode()))
    fernet = Fernet(fernet_key)
    encripted_password = fernet.encrypt(password.encode())
    hasher = hashlib.sha256()
    hasher.update(application_password.encode())
    hashed_value = hasher.hexdigest()
    content = f"""MY_MAIL = \"{mail}\"
    APP_PASSWORD = \"{encripted_password.decode()}\"
    HASH = \"{hashed_value}\""""
    f.write(content)
    print("\n\nSetup completed, you can now use the mail client")

if __name__ == "__main__":
    terminal_setup()

interactable_elements={}
display_window = None
google_pw = None
user_mail = None

def on_client_pw_enter(event):
    global interactable_elements
    global display_window
    global google_pw
    inserted_client_pw = interactable_elements["Client_pw_ent"].get()
    inserted_client_pw_repeat = interactable_elements["Client_pw_repeat_ent"].get()
    if inserted_client_pw != inserted_client_pw_repeat:
        interactable_elements["Client_pw_error_lbl"].config(text="Passwords do not match")
        interactable_elements["Client_pw_ent"].delete(0,tk.END)
        interactable_elements["Client_pw_repeat_ent"].delete(0,tk.END)
    elif inserted_client_pw == "":
        interactable_elements["Client_pw_error_lbl"].config(text="Please insert a password")
        interactable_elements["Client_pw_ent"].delete(0,tk.END)
        interactable_elements["Client_pw_repeat_ent"].delete(0,tk.END)
    elif len(inserted_client_pw)<5:
        interactable_elements["Client_pw_error_lbl"].config(text="Passwords must be at least 5 character long")
        interactable_elements["Client_pw_ent"].delete(0,tk.END)
        interactable_elements["Client_pw_repeat_ent"].delete(0,tk.END)
    else:
        fernet_secret_string = inserted_client_pw + inserted_client_pw
        fernet_key = base64.urlsafe_b64encode(hkdf.derive(fernet_secret_string.encode()))
        fernet = Fernet(fernet_key)
        encripted_password = fernet.encrypt(google_pw.encode())
        hasher = hashlib.sha256()
        hasher.update(inserted_client_pw.encode())
        hashed_value = hasher.hexdigest()
        content = f"""MY_MAIL = \"{user_mail}\"
APP_PASSWORD = \"{encripted_password.decode()}\"
HASH = \"{hashed_value}\""""
        try:
            f = open(".env", "x") 
            f.write(content)
            window.clean_window(display_window)
            window.display_final_setup_window(display_window)
        except:
            print("An error occured when trying to write the .env file")

def on_google_pw_enter(event):
    global interactable_elements
    global display_window
    global google_pw
    inserted_google_pw = interactable_elements["Google_pw_ent"].get()
    inserted_google_pw_repeat = interactable_elements["Google_pw_repeat_ent"].get()
    if inserted_google_pw != inserted_google_pw_repeat or inserted_google_pw == "":
        if inserted_google_pw == "":
            interactable_elements["Google_pw_error_lbl"].config(text="Please insert a password")
        else:
            interactable_elements["Google_pw_error_lbl"].config(text="Passwords do not match")
        interactable_elements["Google_pw_ent"].delete(0,tk.END)
        interactable_elements["Google_pw_repeat_ent"].delete(0,tk.END)
    else:
        google_pw = inserted_google_pw
        window.clean_window(display_window)
        interactable_elements = window.display_ask_client_password_window(display_window)
        interactable_elements["Client_pw_btn"].bind("<Button-1>",on_client_pw_enter)

def on_mail_return(event):
    global interactable_elements
    global display_window
    global user_mail
    mail_text = interactable_elements["Mail_ent"].get()
    if check(mail_text):
        user_mail = mail_text
        window.clean_window(display_window)
        interactable_elements = window.display_ask_google_password_window(display_window)
        interactable_elements["Google_pw_btn"].bind("<Button-1>",on_google_pw_enter)
    else:
        interactable_elements["Mail_ent"].delete(0,tk.END)
        interactable_elements["Mail_error_lbl"].config(text="Please insert a valid email")

def gui_setup(gui_window):
    global interactable_elements
    global display_window
    display_window = gui_window
    interactable_elements = window.display_ask_email_window(display_window)
    interactable_elements["Mail_ent"].bind("<Return>",on_mail_return)
    display_window.mainloop()
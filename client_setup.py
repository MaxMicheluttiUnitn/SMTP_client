from getpass import getpass
import security
import tkinter as tk
import window
import os
import regex_checks

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def terminal_setup():
    global hkdf
    try:
        f = open(os.path.join(BASEDIR, '.env'), "x") 
    except:
        print(".env file already generated. Delete old file to restart the setup.")
        return
    mail="no"
    while not regex_checks.check_mail(mail):
        mail = input("Please insert the Gmail compatible e-mail that you want to use: ")
    password = "yes"
    password_repeat = "no"
    already_once = False
    print("\n\nTo use this application you need an APP PASSWORD for Gmail.\nIf you do not have one, you can generate it from your GOOGLE ACCOUNT.\nYour password will be encrypted and saved on this device and will only be used to send emails through this client.")
    while password != password_repeat or not regex_checks.check_password_regex(password):
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
    while application_password != application_password_copy or not regex_checks.check_password_regex(application_password):
        if not already_once:
            already_once = True
        else:
            if application_password == "" or len(application_password)<5:
                print("The password must be at least 5 characters long.")
            else:
                print("Client passwords did not match.")
        application_password = getpass(prompt="Insert client password: ")
        application_password_copy = getpass(prompt="Repeat client password: ")
    encripted_password=security.encrypt_pw(password,application_password)
    hashed_value= security.digestion(application_password)
    content = f"""MY_MAIL = \"{mail}\"
APP_PASSWORD = \"{encripted_password.decode()}\"
HASH = \"{hashed_value}\""""
    f.write(content)
    print("\n\nSetup completed, you can now use the mail client")

def main():
    terminal_setup()

interactable_elements={}
display_window = None
google_pw = None
user_mail = None
data_path = None

def close_window(event):
    global display_window
    display_window.destroy()

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
        encripted_password = security.encrypt_pw(google_pw,inserted_client_pw)
        hashed_value = security.digestion(inserted_client_pw)
        content = f"""MY_MAIL = \"{user_mail}\"
APP_PASSWORD = \"{encripted_password.decode()}\"
HASH = \"{hashed_value}\""""
        try:
            f = open(os.path.join(BASEDIR, '.env'), "x") 
            f.write(content)
            window.clean_window(display_window)
            interactable_elements = window.display_final_setup_window(display_window)
            interactable_elements["Finished_setup_btn"].bind("<Button-1>",close_window)
        except:
            print("An error occured when trying to write the .env file")

def focus_second_client_pw(event):
    interactable_elements["Client_pw_repeat_ent"].focus_set()

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
        interactable_elements["Client_pw_ent"].bind("<Return>",focus_second_client_pw)
        interactable_elements["Client_pw_repeat_ent"].bind("<Return>",on_client_pw_enter)
        interactable_elements["Client_pw_ent"].focus_set()

def focus_second_google_pw(event):
    interactable_elements["Google_pw_repeat_ent"].focus_set()

def on_mail_return(event):
    global interactable_elements
    global display_window
    global user_mail
    mail_text = interactable_elements["Mail_ent"].get()
    if regex_checks.check_mail(mail_text):
        user_mail = mail_text
        window.clean_window(display_window)
        interactable_elements = window.display_ask_google_password_window(display_window)
        interactable_elements["Google_pw_btn"].bind("<Button-1>",on_google_pw_enter)
        interactable_elements["Google_pw_ent"].bind("<Return>",focus_second_google_pw)
        interactable_elements["Google_pw_repeat_ent"].bind("<Return>",on_google_pw_enter)
        interactable_elements["Google_pw_ent"].focus_set()
    else:
        interactable_elements["Mail_ent"].delete(0,tk.END)
        interactable_elements["Mail_error_lbl"].config(text="Please insert a valid email")

def gui_setup(gui_window, path):
    global interactable_elements
    global display_window
    global data_path
    data_path = path
    display_window = gui_window
    interactable_elements = window.display_ask_email_window(display_window)
    interactable_elements["Mail_ent"].bind("<Return>",on_mail_return)
    interactable_elements["Mail_ent"].focus_set()
    display_window.mainloop()

if __name__ == "__main__":
    main()
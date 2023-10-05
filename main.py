import tkinter as tk
from dotenv import load_dotenv
import os
import window
import client_setup
import mail_script
import re
from tkinter.messagebox import showinfo,askyesno
import easygui
from os.path import basename
import security

load_dotenv()

# PUT YOUR EMAIL AND APP-PASSWORD HERE
sender_email = os.getenv('MY_MAIL')
google_password = os.getenv('APP_PASSWORD')
hash_value = os.getenv('HASH')

display_window = tk.Tk()
interactable_elements = {}
attachments = {}

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def check(email):
    global regex
    if(re.fullmatch(regex, email)):
        return True
    return False

def error_pop_up(error_string):
    showinfo("Error!",error_string)

def confirm_popup(subject,text,receiver,cc_receivers,bcc_receivers):
    global attachments
    answer = askyesno(title='Confirm',
                    message='Are you sure that you want to send the email?')
    if answer:
        mail_script.send_email(subject,text,sender_email,receiver,cc_receivers,bcc_receivers,google_password,attachments.keys())
        reset(None)

def attach(event):
    global attachments
    global interactable_elements
    new_attachment = easygui.fileopenbox("Select the file to attach")
    if new_attachment is None:
        return
    if(new_attachment in attachments):
        return
    attachment_name = basename(new_attachment)
    attachment_frame,attachment_button = window.add_attachment(attachment_name, interactable_elements["Attachments_frm"])
    attachments[new_attachment]={
        "frame": attachment_frame,
        "button": attachment_button
    }
    attachment_button.configure(command=lambda:[remove_attachment(new_attachment)])
    attachment_button.bind("<Button-1>",remove_attachment)
    if len(attachments.keys()) == 1:
        interactable_elements["Attach_lbl"].config(text = "Attachments: ")

def remove_attachment(key):
    global attachments
    global interactable_elements
    to_remove = attachments.get(key)
    if to_remove is None:
        return
    to_remove["frame"].destroy()
    attachments.pop(key)
    if len(attachments.keys()) == 0:
        interactable_elements["Attach_lbl"].config(text = "No attachments")

def reset(event):
    global interactable_elements
    interactable_elements["Editor"].delete("1.0",tk.END)
    interactable_elements["Subject"].delete(0,tk.END)
    interactable_elements["Cc_ent"].delete(0,tk.END)
    interactable_elements["Bcc_ent"].delete(0,tk.END)
    interactable_elements["To"].delete(0,tk.END)
    interactable_elements["To"].insert(0,sender_email)
    global attachments
    attachments = {}
    interactable_elements["Attach_lbl"].config(text = "No attachments")
    for child in interactable_elements["Attachments_frm"].winfo_children():
        child.destroy()

def send(event):
    global interactable_elements
    subject = interactable_elements["Subject"].get()
    if len(subject) < 1:
        error_pop_up("Remember to add a subject!")
        return
    text = interactable_elements["Editor"].get("1.0",tk.END)
    if """
""".__eq__(text):
        error_pop_up("Remember to add content to the mail!")
        return
    receiver = interactable_elements["To"].get()
    if len(receiver) < 2:
        error_pop_up("Remember to add a receiver!")
        return
    if not check(receiver):
        error_pop_up("The receiver is invalid, check the adress!")
        return
    cc_receivers = get_cc_receivers()
    cc_receivers = list(filter(check,cc_receivers))
    bcc_receivers = get_bcc_receivers()
    bcc_receivers = list(filter(check,bcc_receivers))
    confirm_popup(subject,text,receiver,cc_receivers,bcc_receivers)

def get_cc_receivers():
    global interactable_elements
    return get_receivers_list(interactable_elements["Cc_ent"].get())

def get_bcc_receivers():
    global interactable_elements
    return get_receivers_list(interactable_elements["Bcc_ent"].get())

def get_receivers_list(input):
    return input.split("; ")

def load_csv_cc(event):
    global interactable_elements
    cc_receivers = []
    mail_script.read_csv(cc_receivers) 
    interactable_elements["Cc_ent"].delete(0,tk.END)
    interactable_elements["Cc_ent"].insert(0,"; ".join(cc_receivers))

def load_csv_bcc(event):
    global interactable_elements
    bcc_receivers = []
    result = mail_script.read_csv(bcc_receivers)
    if result:
        interactable_elements["Bcc_ent"].delete(0,tk.END)
        interactable_elements["Bcc_ent"].insert(0,"; ".join(bcc_receivers))

def add_bindings():
    global interactable_elements
    interactable_elements["Cancel_btn"].bind("<Button-1>",reset)
    interactable_elements["Send_btn"].bind("<Button-1>",send)
    interactable_elements["Attach_btn"].bind("<Button-1>",attach)
    interactable_elements["Cc_btn"].bind("<Button-1>",load_csv_cc)
    interactable_elements["Bcc_btn"].bind("<Button-1>",load_csv_bcc)

def on_login_enter(event):
    global interactable_elements
    global hash_value
    inserted_pw = interactable_elements["Auth_ent"].get()
    if not security.check_password(inserted_pw):
        # incorrect password
        interactable_elements["Auth_ent"].delete(0,tk.END)
        if len(interactable_elements["Auth_frm"].winfo_children()) == 2:
            window.add_wrong_password_label(interactable_elements["Auth_frm"])
        return
    global google_password
    google_password = security.get_google_app_pw(inserted_pw)
    print(google_password)
    window.clean_window(display_window)
    setup_main_app()
    
def setup_main_app():
    global interactable_elements
    interactable_elements = window.display_editor_window(display_window)
    add_bindings()

def setup_login():
    global interactable_elements
    interactable_elements = window.display_authentication_window(display_window)
    interactable_elements["Auth_ent"].bind('<Return>', on_login_enter)

def main():
    global display_window
    if not os.path.exists(".env"):
        client_setup.gui_setup(display_window)
    else:
        window.initialize_window(display_window)
        setup_login()
        display_window.mainloop()

if __name__ == "__main__":
    main()
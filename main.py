import tkinter as tk
from dotenv import load_dotenv
import os
import window
import mail_script
import re
from tkinter.messagebox import showinfo,askyesno

load_dotenv()

# PUT YOUR EMAIL AND APP-PASSWORD HERE
sender_email = os.getenv('MY_MAIL')
password = os.getenv('APP_PASSWORD')

display_window = tk.Tk()
interactable_elements = {}

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def check(email):
    global regex
    if(re.fullmatch(regex, email)):
        return True
    return False

def error_pop_up(error_string):
    showinfo("Error!",error_string)

def confirm_popup(subject,text,receiver,cc_receivers,bcc_receivers):
    answer = askyesno(title='Confirm',
                    message='Are you sure that you want to send the email?')
    if answer:
        mail_script.send_email(subject,text,receiver,cc_receivers,bcc_receivers,password,[])
        reset(None)

    

def reset(event):
    interactable_elements["Editor"].delete("1.0",tk.END)
    interactable_elements["Subject"].delete(0,tk.END)
    interactable_elements["Cc_ent"].delete(0,tk.END)
    interactable_elements["Bcc_ent"].delete(0,tk.END)
    interactable_elements["To"].delete(0,tk.END)
    interactable_elements["To"].insert(0,sender_email)

def send(event):
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
    return get_receivers_list(interactable_elements["Cc_ent"].get())

def get_bcc_receivers():
    return get_receivers_list(interactable_elements["Bcc_ent"].get())

def get_receivers_list(input):
    return input.split("; ")

def load_csv_cc(event):
    cc_receivers = []
    mail_script.read_csv(cc_receivers) 
    interactable_elements["Cc_ent"].delete(0,tk.END)
    interactable_elements["Cc_ent"].insert(0,"; ".join(cc_receivers))

def load_csv_bcc(event):
    bcc_receivers = []
    mail_script.read_csv(bcc_receivers)
    interactable_elements["Bcc_ent"].delete(0,tk.END)
    interactable_elements["Bcc_ent"].insert(0,"; ".join(bcc_receivers))

def add_bindings():
    interactable_elements["Cancel_btn"].bind("<Button-1>",reset)
    interactable_elements["Send_btn"].bind("<Button-1>",send)
    interactable_elements["Cc_btn"].bind("<Button-1>",load_csv_cc)
    interactable_elements["Bcc_btn"].bind("<Button-1>",load_csv_bcc)

if __name__ == "__main__":
    interactable_elements = window.display_editor_window(display_window)
    add_bindings()
    display_window.mainloop()

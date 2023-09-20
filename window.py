import tkinter as tk
from dotenv import load_dotenv
import os

load_dotenv()

# PUT YOUR EMAIL AND APP-PASSWORD HERE
sender_email = os.getenv('MY_MAIL')
password = os.getenv('APP_PASSWORD')

def display_top_entry_elem(name, has_button=False, btn_text="Press here", default_entry=None):
    frm_elem = tk.Frame(pady=3, height=15)
    lbl_elem = tk.Label(text=name,master=frm_elem,width=10, anchor=tk.W)
    lbl_elem.pack(side=tk.LEFT,fill=tk.Y)
    if(has_button):
        btn_elem=tk.Button(text=btn_text,relief=tk.RAISED,master=frm_elem)
        btn_elem.pack(side=tk.LEFT,fill=tk.Y)
    else:
        btn_elem = None
    ent_elem = tk.Entry(master=frm_elem) 
    if not default_entry is None:
        ent_elem.insert(0,default_entry)
    ent_elem.pack(fill=tk.X, expand=True)
    frm_elem.pack(fill=tk.X)
    return ent_elem,btn_elem

def display_email_elem(name, email):
    frm_elem = tk.Frame(pady=3, height=15)
    lbl_elem = tk.Label(text=name,master=frm_elem,width=10, anchor=tk.W)
    lbl_elem.pack(side=tk.LEFT,fill=tk.Y)
    lbl_elem_mail = tk.Label(text=email,master=frm_elem,anchor=tk.W)
    lbl_elem_mail.pack(fill=tk.X, expand=True)
    frm_elem.pack(fill=tk.X)
    return frm_elem

def display_text_editor():
    txt_mail_container = tk.Text()
    txt_mail_container.pack(fill=tk.BOTH, expand=True)
    return txt_mail_container

def display_bottom_menu():
    frm_bottom = tk.Frame(pady=3, height=15)
    btn_send = tk.Button(
        text="Send!",
        relief=tk.RAISED,
        master=frm_bottom,padx=30
    )
    btn_send.pack(side=tk.RIGHT)
    btn_cancel = tk.Button(
        text="Cancel",
        relief=tk.RAISED,
        master=frm_bottom,padx=30
    )
    btn_cancel.pack(side=tk.RIGHT)  
    frm_bottom.pack(fill=tk.X)
    return btn_send,btn_cancel


def display_editor_window(window):
    window.title("SMTP client")
    display_email_elem("From:",sender_email)
    ent_to,btn_to = display_top_entry_elem("To:",default_entry=sender_email)
    ent_cc,btn_cc = display_top_entry_elem("CC:", True, "From CSV")
    ent_bcc,btn_bcc = display_top_entry_elem("BCC:", True, "From CSV")
    ent_subject,btn_subject = display_top_entry_elem("Subject:")
    txt_editor = display_text_editor()
    btn_send,btn_cancel = display_bottom_menu()
    return {
        "To" : ent_to,
        "Cc_ent" : ent_cc,
        "Cc_btn": btn_cc,
        "Bcc_ent": ent_bcc,
        "Bcc_btn": btn_bcc,
        "Subject": ent_subject,
        "Editor": txt_editor,
        "Send_btn": btn_send,
        "Cancel_btn": btn_cancel
    }

if __name__ == "__main__":
    window = tk.Tk(baseName="app")
    display_editor_window(window)
    window.mainloop()
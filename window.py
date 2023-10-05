import tkinter as tk
from tkinter import PhotoImage
from dotenv import load_dotenv
import os

load_dotenv()

# PUT YOUR EMAIL AND APP-PASSWORD HERE
sender_email = os.getenv('MY_MAIL')
#password = os.getenv('APP_PASSWORD')

def clean_window(window):
    for child in window.winfo_children():
        child.destroy()

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
        text="Clear",
        relief=tk.RAISED,
        master=frm_bottom,padx=30
    )
    btn_cancel.pack(side=tk.RIGHT)  
    btn_attach = tk.Button(
        text="Add attachment",
        relief=tk.RAISED,
        master=frm_bottom,padx=30,
    )
    btn_attach.pack(side=tk.LEFT)  
    frm_bottom.pack(fill=tk.X)
    return btn_send,btn_cancel,btn_attach

def display_attachments_layer():
    frm_attach = tk.Frame(pady=3, height=15)
    lbl_attach=tk.Label(text="No attachments", anchor=tk.W, master=frm_attach)
    lbl_attach.pack(side=tk.LEFT,fill=tk.Y)
    frm_attachments=tk.Frame(master=frm_attach)
    frm_attachments.pack(side=tk.LEFT,fill=tk.Y)
    frm_attach.pack(fill=tk.X)
    return frm_attachments, lbl_attach

def initialize_window(window):
    img = PhotoImage(file='logo.png')
    window.iconphoto(False, img)
    window.title("SMTP client")

def add_attachment(name,frm_attachments):
    frm_elem=tk.Frame(master=frm_attachments)
    lbl_attachment=tk.Label(text=name,anchor=tk.W,master=frm_elem)
    lbl_attachment.pack(side=tk.LEFT)
    btn_attachment=tk.Button(
        text="X",
        relief=tk.RAISED,
        master=frm_elem
    )
    btn_attachment.pack(side=tk.LEFT)
    frm_elem.pack(side=tk.LEFT)
    return frm_elem, btn_attachment    

def display_editor_window(window):
    global sender_email
    window.minsize(500,638)
    display_email_elem("From:",sender_email)
    ent_to,btn_to = display_top_entry_elem("To:",default_entry=sender_email)
    ent_cc,btn_cc = display_top_entry_elem("CC:", True, "From CSV")
    ent_bcc,btn_bcc = display_top_entry_elem("BCC:", True, "From CSV")
    ent_subject,btn_subject = display_top_entry_elem("Subject:")
    txt_editor = display_text_editor()
    frm_attachments,lbl_attach = display_attachments_layer()
    btn_send,btn_cancel,btn_attach = display_bottom_menu()
    return {
        "To" : ent_to,
        "Cc_ent" : ent_cc,
        "Cc_btn": btn_cc,
        "Bcc_ent": ent_bcc,
        "Bcc_btn": btn_bcc,
        "Subject": ent_subject,
        "Editor": txt_editor,
        "Send_btn": btn_send,
        "Cancel_btn": btn_cancel,
        "Attach_btn": btn_attach,
        "Attach_lbl": lbl_attach,
        "Attachments_frm": frm_attachments
    }


def add_wrong_password_label(auth_frame):
    lbl_wrong_pw =tk.Label(text="Incorrect password!!!", anchor=tk.W, master=auth_frame)
    lbl_wrong_pw.pack(pady=8)

def display_authentication_window(window):
    window.minsize(300,150)
    frm_auth=tk.Frame(master=window)
    lbl_auth=tk.Label(text="Insert your password and press enter:", anchor=tk.W, master=frm_auth)
    lbl_auth.pack(pady=8)
    bullet = "\u2022"
    ent_auth=tk.Entry(width=35,master=frm_auth,show=bullet)
    ent_auth.pack(pady=8)
    frm_auth.place(relx=.5, rely=.5, anchor="c")
    return {
        "Auth_frm": frm_auth,
        "Auth_ent": ent_auth
    }


def display_ask_email_window(window):
    window.minsize(500,500)
    window.title("SMTP client Setup")
    frm_mail=tk.Frame(master=window)
    lbl_mail_1=tk.Label(text="Please insert the Gmail compatible e-mail that you want to use:", anchor=tk.W, master=frm_mail)
    lbl_mail_1.pack(pady=8)
    ent_mail=tk.Entry(width=35,master=frm_mail)
    ent_mail.pack(pady=8)
    lbl_mail_error=tk.Label(text="", anchor=tk.W, master=frm_mail)
    lbl_mail_error.pack(pady=8)
    frm_mail.place(relx=.5, rely=.5, anchor="c")
    return {
        "Mail_frm": frm_mail,
        "Mail_ent": ent_mail,
        "Mail_error_lbl":lbl_mail_error
    }



def display_ask_google_password_window(window):
    window.minsize(500,500)
    window.title("SMTP client Setup")
    frm_google_pw=tk.Frame(master=window)
    lbl_google_pw_1=tk.Label(text="To use this application you need an APP PASSWORD for Gmail. If you do not have one, you can generate it from your GOOGLE ACCOUNT. Your password will be encrypted and saved on this device and will only be used to send emails through this client.", anchor=tk.W, master=frm_google_pw, wraplength=400)
    lbl_google_pw_2=tk.Label(text="Insert password:", anchor=tk.W, master=frm_google_pw)
    lbl_google_pw_3=tk.Label(text="Repeat password:", anchor=tk.W, master=frm_google_pw)
    lbl_google_pw_1.pack(pady=8)
    lbl_google_pw_2.pack(pady=8)
    bullet = "\u2022"
    ent_google_pw=tk.Entry(width=35,master=frm_google_pw,show=bullet)
    ent_google_pw.pack(pady=8)
    lbl_google_pw_3.pack(pady=8)
    ent_google_pw_repeat=tk.Entry(width=35,master=frm_google_pw,show=bullet)
    ent_google_pw_repeat.pack(pady=8)
    btn_google_pw=tk.Button(
        text="Confirm Password",
        relief=tk.RAISED,
        master=frm_google_pw
    )
    lbl_google_pw_error=tk.Label(text="", anchor=tk.W, master=frm_google_pw)
    lbl_google_pw_error.pack()
    btn_google_pw.pack()
    frm_google_pw.place(relx=.5, rely=.5, anchor="c")
    return {
        "Google_pw_frm": frm_google_pw,
        "Google_pw_ent": ent_google_pw,
        "Google_pw_repeat_ent": ent_google_pw_repeat,
        "Google_pw_btn": btn_google_pw,
        "Google_pw_error_lbl":lbl_google_pw_error
    }

def display_ask_client_password_window(window):
    window.minsize(500,500)
    window.title("SMTP client Setup")
    frm_client_pw=tk.Frame(master=window)
    lbl_client_pw_1=tk.Label(text="Select a password for the mail client, the password must be at least 5 character long. It will be used to encode and ecrypt your app password, as well as giving you access to the client.", anchor=tk.W, master=frm_client_pw, wraplength=400)
    lbl_client_pw_2=tk.Label(text="Insert password:", anchor=tk.W, master=frm_client_pw)
    lbl_client_pw_3=tk.Label(text="Repeat password:", anchor=tk.W, master=frm_client_pw)
    lbl_client_pw_1.pack(pady=8)
    lbl_client_pw_2.pack(pady=8)
    bullet = "\u2022"
    ent_client_pw=tk.Entry(width=35,master=frm_client_pw,show=bullet)
    ent_client_pw.pack(pady=8)
    lbl_client_pw_3.pack(pady=8)
    ent_client_pw_repeat=tk.Entry(width=35,master=frm_client_pw,show=bullet)
    ent_client_pw_repeat.pack(pady=8)
    btn_client_pw=tk.Button(
        text="Confirm Password",
        relief=tk.RAISED,
        master=frm_client_pw
    )
    lbl_client_pw_error=tk.Label(text="", anchor=tk.W, master=frm_client_pw)
    lbl_client_pw_error.pack()
    btn_client_pw.pack()
    frm_client_pw.place(relx=.5, rely=.5, anchor="c")
    return {
        "Client_pw_frm": frm_client_pw,
        "Client_pw_ent": ent_client_pw,
        "Client_pw_repeat_ent": ent_client_pw_repeat,
        "Client_pw_btn": btn_client_pw,
        "Client_pw_error_lbl":lbl_client_pw_error
    }

def display_final_setup_window(window):
    frm_final=tk.Frame(master=window)
    lbl_final=tk.Label(text="You have completed the setup for the mail clinet. You can now close this window and start using the client.", anchor=tk.W, master=frm_final, wraplength=400)
    lbl_final.pack()
    frm_final.place(relx=.5, rely=.5, anchor="c")

if __name__ == "__main__":
    window = tk.Tk(baseName="app")
    display_ask_client_password_window(window)
    window.mainloop()
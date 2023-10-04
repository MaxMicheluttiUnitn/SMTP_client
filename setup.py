from getpass import getpass
import re
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import hashlib

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

try:
    f = open(".env", "x") 
except:
    print(".env file already generated. Delete old file to restart the setup.")
    quit(0)
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

import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

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

def encrypt_pw(password,key):
    fernet_secret_string = key + key
    fernet_key = base64.urlsafe_b64encode(hkdf.derive(fernet_secret_string.encode()))
    fernet = Fernet(fernet_key)
    return fernet.encrypt(password.encode())

def digestion(key):
    hasher = hashlib.sha256()
    hasher.update(key.encode())
    return hasher.hexdigest()
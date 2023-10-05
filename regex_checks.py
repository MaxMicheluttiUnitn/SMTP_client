import re

regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,9}\b'
regex_pw = r'[A-Za-z0-9@#$%^&+=]{5,}'
 
def check_mail(email):
    global regex_mail
    if(re.fullmatch(regex_mail, email)):
        return True
    return False

def check_password_regex(password):
    global regex_pw
    if(re.fullmatch(regex_pw, password)):
        return True
    return False
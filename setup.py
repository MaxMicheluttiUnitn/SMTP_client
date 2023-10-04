from getpass import getpass

try:
    f = open(".env", "x") 
    mail = input("Please insert the Gmail compatible e-mail that you want to use: ")
    password = getpass(prompt="To use this application you need an APP PASSWORD for Gmail.\nIf you do not have one, you can generate it from your GOOGLE ACCOUNT.\nYour password will be encrypted and saved on this device and will only be used to send emails through this client.\nInsert the password: ")
    #print(mail, password)
    content = f"""MY_MAIL = \"{mail}\"
APP_PASSWORD = \"{password}\""""
    f.write(content)
    print("Setup completed, you can now use the mail client")
except:
    print(".env file already generated. Delete old file to restart the setup.")
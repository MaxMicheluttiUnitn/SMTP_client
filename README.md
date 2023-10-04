# SMTP_client

This is a SMTP client designed to send e-mails with Gmail in BCC to multiple users. This code was NOT developed in collaboration with Google, although Gmail servers are queried to send e-mails using SMTP.

You need Python 3.10.12 or a later version to run this code. Older Python versions may work, but there is no guarantee. You can check your python version by typing this in your terminal:

```
 >> python3 --version
 ```

## Install

First clone the repository with git:

```
>> git clone https://github.com/MaxMicheluttiUnitn/SMTP_client  
```   

Remember to install python dependencies:

``` 
>> pip install -r requirements.txt 
```

For **LINUX** users, install TKinter to load the GUI:

```
 >> apt-get install python3-tk  
 ```

Once everything is installed you can run the setup script:

```
 >> python3 setup.py 
 ```

Remember: to send emails from Gmail compatible accounts from third party applications you must use the **APP-PASSWORD** that you can generate from your Google account.

The setup procedure will require you to choose a password for the client that you will need to type everytime you start this application. This is done for your security: keeping all your passwords encrypted and protecting you from possible impersonation attacks.

## Use

To use the full GUI type in your terminal

```
 >> python3 main.py
 ```

To use the terminal version type

```
 >> python3 mail_script.py
 ```

The CSV file loaded by the application must be in the following format: receivers emails must be written in the first column of the file, one email for eaxch row

## Forgot your Password?

Simply delete the **.env** file and run the setup again. Everything will be exactly like your first time setting up the mail client.

```
 >> python3 setup.py 
 ```
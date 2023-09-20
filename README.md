# SMTP_client

This is a SMTP client designed to send emails in BCC to multiple users.  

## Install

First clone the repository with git

```
git clone https://github.com/MaxMicheluttiUnitn/SMTP_client  
```   

Remember to install python dependencies

``` 
pip install -r requirements.txt 
```

For **LINUX** users, install TKinter to load the GUI:

```
 apt-get install python3-tk  
 ```

Remember to create and fill the **.env** file as shown in **.env.example** with your email and password.  
To send emails from Google GMail accounts use the App-Password that you can generate from your GMail account.

## Use

To use the full GUI type in your terminal

```
 python3 main.py
 ```

To use the terminal version type

```
 python3 mail_script.py
 ```
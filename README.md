# SMTP_client

This is a SMTP client designed to send e-mails with Gmail in BCC to multiple users.

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

In alternative you can create and fill the **.env** file as shown in **.env.example** with your email and APP Password. To send emails from Gmail compatible accounts use the **APP-PASSWORD** that you can generate from your Google account.

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
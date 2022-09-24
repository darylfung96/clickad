# Getting Started

Tested on python 3.9

Run
```angular2html
pip install -r requirements.txt
```
To install the required packages


### Registering accounts
Before registering account, make sure that the script is pointing to a right file containing
accounts to register for Neobux. An example are
```angular2html
gabynixony@gmail.com:Rhfcjnf1234:moskowu@mail.ru
brockrusselu@gmail.com:Rhfcjnf1234:moskowu@mail.ru
shahharoldy@gmail.com:Rhfcjnf1234:moskowu@mail.ru
```
The format is USER_EMAIL:USER_PASSWORD:BACKUP_EMAIL 

**MAKE SURE TO CREATE A BACKUP FOR THE TEXT FILE BECAUSE REGISTRATION PROCESS WILL REMOVE THE ACCOUNT IT HAS REGISTERED**

Change the script in line 19 for register_accounts.py:
```angular2html
 19:	with open('data/DropMeFiles_3K5N5/order2808696.txt', 'r') as f:

---
replacing 
data/DropMeFiles_3K5N5/order2808696.txt
with the correct register account files

```

If you want to use ports, make sure you have **ports.txt** in the same directory as 
**register_accounts.py**. You can get ports.txt file from astroproxy, just their usual format.

If you don't want to use ports, uncomment the port usage and use only 
```angular2html
		neobux = NeoBux(username)
```

To register for accounts, run:
```angular2html
python register_accounts.py
```

This will run the registration process by registering an account in NeoBux, and then going to
Google Mail to receive the verification code and finalize the registration in NeoBux

---

### Clicking Ads in NeoBux
Ensure that the script is pointing to the right file that contains the account
for NeoBux, it's the same format just like registration text file.

If you want to use ports, make sure you have **ports.txt** in the same directory as 
**register_accounts.py**. You can get ports.txt file from astroproxy, just their usual format.


To start clicking, run
```angular2html
python click.py
```






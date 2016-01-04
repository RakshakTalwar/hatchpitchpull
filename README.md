## This assumes you are on Linux
## Make sure you have pip installed
[Instructions](https://pip.pypa.io/en/stable/installing/#using-os-package-managers) to install pip using an OS package manager

### Commands to install this package:  
prerequisites are automatically installed  
```sh
$ sudo chmod +x setup.sh  
$ sudo ./setup.sh  
```

### To configure authentication details:  
Create a file called: auth_info.txt  
Now type:
- The F6S API Key as the first line  

Save and close this file

Follow these [instructions](https://support.google.com/cloud/answer/6158849?hl=en&authuser=1#serviceaccounts) to generate the client secret JSON file.
Rename the downloaded JSON file to client_secret.json and save this file in the parent directory.  

### Running the program
Run the main.py file whenever you would like the program to run.  
Tip: It's advised to set a cronjob process on your Linux machine to run it periodically

### Accessing the SQLite DB
The sqlite db file is stored as db/HATCHscreening.db

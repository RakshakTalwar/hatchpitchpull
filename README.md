## This assumes you are on Linux
## Make sure you have pip installed
[Instructions](https://pip.pypa.io/en/stable/installing/#using-os-package-managers) to install pip using an OS package manager

### Commands to install prerequisites:  
```sh
$ sudo chmod +x setup.sh  
$ sudo ./setup.sh  
```

### Commands to install this package:  
```sh
$ sudo pip install -e ./
```

### To set in authentication details:  
Create a file called: auth_info.txt  
Now type:  
- The email address as the first line  
- The email address' password as the second line  
- The F6S API Key as the third line  

Save and close this file  

### Running the program
Run the hatchpitchpull/main.py file whenever you would like the program to run.  
Tip: It's advised to set a cronjob process on your Linux machine to run it periodically

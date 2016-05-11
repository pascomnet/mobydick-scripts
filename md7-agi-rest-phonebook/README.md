# Script fetches the caller name from the third party API 
1) Create the Dialplan script in mobydick web-ui and put the content of the file def_agi_rest_phonebook
2) Copy the php script agi_rest_phonebook.php to the mobydick appliance /etc/asterisk/agi/agi_rest_phonebook.php
3) Modify the content of the agi_rest_phonebook.php if needed. In this example provide valid REST_API_KEY
4) Change the owner of the php script 
  chown asterisk:asterisk agi_rest_phonebook.php
5) Change the access permissions of the php script  
  chmod 550 agi_rest_phonebook.php
6) Assign script...

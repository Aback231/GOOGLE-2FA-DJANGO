# GOOGLE 2FA DJANGO

Google 2FA code generator with time calculation and animation, local in browser.

Start the server:

`python manage.py runserver`

Navigate to:

`http://127.0.0.1:8000/app/2fa`

2FA secrets are stored locally inside Sqlite3 DB. Initially DB is empty, but can be populated by using the Add button.
Text pasted into Add Input field should be in following form:

`EMAIL`

`2FA KEY`

`EMAIL1`

`2FA KEY1`

...

...


![alt text](https://github.com/Aback231/GOOGLE-2FA-DJANGO/blob/main/WebUI.png?raw=true)

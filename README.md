# GOOGLE 2FA DJANGO

Google 2FA code generator with time calculation and animation, local in browser.

Start the server:

`python manage.py runserver`

Navigate to:

`http://127.0.0.1:8000/app/2fa`

2FA secrets are stored locally inside Sqlite3 DB. Initially DB is empty, but can be populated by using the Add button.
Text pasted into Add Input field should be in following form (email adn 2fa separated by one empty line):

`EMAIL`<br />
`2FA KEY`<br />
`EMAIL1`<br />
`2FA KEY1`<br />
...<br />
...


![alt text](https://github.com/Aback231/GOOGLE-2FA-DJANGO/blob/main/WebUI.png?raw=true)

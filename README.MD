# Programmeerija prooviülesanne (Python)
## Requirements
```
vsCode 1.78.2

python 3.11.3
node 18.16.0
npm 9.5.1
Django 4.2.2
django-cors-headers 4.1.0
djangorestframework 3.14.0
psycopg2 2.9.6
```

## Running from source code
1. GitHubi hoidla kloonida ja avada bash-terminal hoidlast kloonitud kaustas
2. Virtuaal keskkonda (edasi KK) loomine: `python -m venv venv` (KK aktiveerimine: `venv\Scripts\activate`)
3. requirements.txt. Installimiseks: `pip install -r requirements.txt` 
4. Backend rakenduse käivitamiseks: `python manage.py runserver`. Vaikimisi backend serveri aadress on https://127.0.0.1:8000
5. Frontend rakenduse käivitamiseks `cd my-frontend` ja `npm start`. aikimisi backend serveri aadress on https://127.0.0.1:3000 

avaleht - /
Osaühingu asutamise vorm - /create
Osaühingu andmete vaade - muutuv, nt /info/1
Osaühingu andmete muutmine - muutuv, nt /edit/24
abi - /help


## Admin paneel
Admin paneelis saab haalda tabelid graafilisel kujul (st haldurile pole vaja alati juurdepääsu baasile).

'backendpesa' + '/admin/', vaikimisi on http://127.0.0.1:8000/admin/

SuperUser loomiseks: `python manage.py createsuperuser`
Kui viskab errori, saab proovida `python manage.py migrate auth`

## Algandmete baasi tekitamine
TODO

## Kommentaarid
- my-frontend/.env - REACT_APP_API -  Backendi aadress, mida kasutab Frontend.
- GjangoAPI/settings.py - hetkel testimiseks pandud `CORS_ORIGIN_ALLOW_ALL = True` ja `CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']` - Tootmises ei soovitata. Selle asemel lisage domeenid, mis tuleks lisada lubatud loendisse


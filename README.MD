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
2. Virtuaal keskkonda (edasi KK) loomine:
- windows: `python -m venv venv` (KK aktiveerimine: `venv\Scripts\activate`)
- linux: `python3 -m venv venv` (KK aktiveerimine: `source venv/bin/activate`)
3. requirements.txt. Installimiseks: `pip install -r requirements.txt`.
- Kui vistab errori seotud psycopg2'ga, siis panna `psycopg2` asemel `psycopg2-binary` ja käivitada uuesti.
- installimine kasitsi:
```
pip install asgiref
pip install Django
pip install django-cors-headers
pip install djangorestframework
pip install psycopg2 või pip install psycopg2-binary
```
4. Backend rakenduse käivitamiseks: `python manage.py runserver`. Vaikimisi backend serveri aadress on https://127.0.0.1:8000
5. Frontend rakenduse käivitamiseks `cd my-frontend`, `npm install` ja `npm start`. Vaikimisi frontend serveri aadress on https://127.0.0.1:3000 
- kui npm pole veel installitud: `sudo apt install npm`

## URLS
1. 'frontendpesa' + ... (vaikimisi https://127.0.0.1:3000)
- avaleht - /
- Osaühingu asutamise vorm - /create
- Osaühingu andmete vaade - muutuv, nt /info/1
- Osaühingu osakapitali suurendamise vorm - muutuv, nt /edit/24
- Abi - /help
2.  'backendpesa' + ... (vaikimisi https://127.0.0.1:8000)
- adminpaneel - /admin


## Admin paneel
Admin paneelis saab haalda tabelid graafilisel kujul (st haldurile pole vaja alati juurdepääsu baasile).

'backendpesa' + '/admin/', vaikimisi on http://127.0.0.1:8000/admin/

SuperUser loomiseks: `python manage.py createsuperuser`
Kui viskab errori, saab proovida `python manage.py migrate auth`

## Algandmete baasi tekitamine
1. avada pg admin
2. Juhul, kui tabelid baasis pole veel loodud käivitada script `createdb.sql`.
3. SQL skript `population.sql`. Script kustutab koik info tabelitest, nullindab loendurid ja lisab testandmeid (kokku lisatakse 33 isikut, 12 osauhingu lisaandmeid ja 22 seoseid isik-osauhing). 

## DB
Hetkel on pandud tasuta ressursi andmed. See resurss võimaldas testimiseks postgressql baasi tekkitada ja kasutada seda.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2' #või 'django.db.backends.postgresql' või mida vaja kasutada
        'NAME': [database.name],
        'USER': [username],
        'PASSWORD': [password],
        'HOST': [host],
        'PORT': '5432' #default PostgreSQL port või port mida vaja kasutada
    }
}
```

1. Kustutada migratsioonifailid OsauhingAPP/migrations kaustas.
2. Uue migratsioonifaili loomiseks käivitage `python manage.py makemigrations`.
3. Projektimudelite andmebaasi migreerimiseks käivitage käsk `python manage.py migrate`. See toiming loob automaatselt
kõik vajalikud andmebaasitabelid vastavalt OsauhingAPP/models.py failile ja Django seadistustele.

## Kommentaarid
- my-frontend/.env - REACT_APP_API -  Backendi aadress, mida kasutab Frontend.
- GjangoAPI/settings.py - hetkel testimiseks pandud `CORS_ORIGIN_ALLOW_ALL = True` ja `CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']` - Tootmises ei soovitata. Selle asemel lisage domeenid, mis tuleks lisada lubatud loendisse
- Kasutatud css file asub my-frontend/src/styles


Uppgiftskravsregister
=====================

Setup
-----

Något i stil med detta::

    # installera nödvändinga dependencies
    pip install -r requirements.txt
    # hämta 2013-kartläggningen
    wget 'http://bolagsverket.se/polopoly_fs/1.10237!/Menu/general/column-content/file/kartlaggningsresultat.xlsx'
    # hämta 2012-kartläggningen
    wget 'http://bolagsverket.se/polopoly_fs/1.9828!/Menu/general/column-content/file/fullstandigt_resultat_kartlaggning.xlsx'
    # konvertera kartläggningsresultatet till JSON
    python excelimport.py kartlaggningsresultat.xlsx fullstandigt_resultat_kartlaggning.xlsx register/fixtures/initial_data.json
    # skapa postgres-databas
    createdb uppgiftskrav
    # grundladda användargrupper/myndigheter
    python ./manage.py migrate auth
    python ./manage.py loaddata register/fixtures/groups.json
    python ./manage.py createsuperuser
    # sätt upp datastruktur och grundladda data för själva appen
    python ./manage.py makemigrations register
    python ./manage.py migrate
    python ./manage.py loaddata register/fixtures/initial_data.json

Systemet kan sedan köras som en vanlig djangoapp (./manage.py runserver eller via WSGI), eller via foreman (som fås som del av Heroku toolbelt)::

    foreman start

Deploy till Heroku
------------------

 Liknande kommandon::

    git push master heroku

Om databasen måste resettas och grundladdas::
   
    heroku pg:reset DATABASE
    heroku run python manage.py migrate auth
    heroku run python ./manage.py migrate auth
    heroku run python ./manage.py loaddata register/fixtures/groups.json
    heroku run python ./manage.py createsuperuser
    heroku run python ./manage.py makemigrations register
    heroku run python ./manage.py migrate
    heroku run python ./manage.py loaddata register/fixtures/initial_data.json
    

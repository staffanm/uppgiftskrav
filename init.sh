#! /bin/sh
dropdb uppgiftskrav
createdb uppgiftskrav
rm -r register/migrations
echo "Database reset"
python ./manage.py migrate auth
python userimport.py initial_userdb.yml register/fixtures/groups.json
python ./manage.py loaddata register/fixtures/groups.json
python ./manage.py makemigrations register
python ./manage.py migrate
python excelimport.py kartlaggningsresultat.xlsx fullstandigt_resultat_kartlaggning.xlsx register/fixtures/initial_data.json
python ./manage.py loaddata register/fixtures/initial_data.json

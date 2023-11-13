python -m venv env
source env/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py initial
python manage.py runserver 0.0.0.0:8000
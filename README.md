# Software utilizzato:
- Python 3.8
- Django
- Pycharm

# Guida all'installazione:
- Clonare la repository o estrarla dallo zip in un percorso a propria scelta
- Aprire il progetto con Pycharm
- Creare un nuovo venv con interprete Python 3.8, utilizzando pipenv.
- Passare al terminale di Pycharm e installare Django:
- - `pipenv install Django`
- Installare le seguenti librerie:
- - `pipenv install django-bootstrap4`
- - `pipenv install django-crispy-forms`
- - `pipenv install Pillow`
- - `pipenv install pdfkit`
- Quindi procedere con la creazione del database con i seguenti comandi:
- - `python manage.py migrate`
- Per avviare il server, eseguire il seguente comando dal terminale di Pycharm:
- - `python manage.py runserver`
- Per creare un superuser, eseguire il seguente comando dal terminale di Pycharm:
- - `python manage.py createsuperuser`
- - Inserire username, email e password
- Per accedere al sito, aprire il browser e digitare:
- - `localhost:8000`
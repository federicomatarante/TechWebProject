import subprocess


def makemigrations():
    """
    Make migrations for all apps.
    """
    subprocess.call(['python3', './manage.py', 'makemigrations'])


def migrate():
    """
    Migrate all apps.
    """
    subprocess.call(['python3', './manage.py', 'migrate'])


def start():
    """
    Start the server.
    """
    subprocess.call(['python3', '-/manage.py', 'runserver'])


def main():
    """
    Main function.
    """
    makemigrations()
    #migrate()
    #start()


if __name__ == '__main__':
    main()

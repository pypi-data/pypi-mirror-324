from getpass import getpass

from typer import Typer

from ..lib.upload import upload

app = Typer()

@app.command()
def upload():
    """Upload sdist/wheels to PyPI."""
    username = input("Username: ")
    password = getpass("Password: ")
    upload(path=input("file: "), username=username, password=password)

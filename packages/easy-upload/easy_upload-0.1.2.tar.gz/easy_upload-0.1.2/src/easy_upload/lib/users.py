from getpass import getpass

from beaupy import select
from rich.console import Console

from ..lib.credentials import set_cred

def add_account(url: str):
    console = Console()
    console.print("Select Login Method: ")
    login_method = select([
        "Login with Token",
        "Login with Credential"
    ], cursor="🢧", cursor_style="cyan")
    if login_method == "Login with Token":
        username = "__token__"
        password = getpass("Enter Token: ")
    else:
        username = input("Username: ")
        password = getpass("Password: ")
    while True:
        q = input("Do you want to save your credentials? (y/n): ").lower()
        if q == "n":
            break
        elif q == "y":
            name = input("Enter Credential Label: ")
            set_cred(url, password, name + "," + username)
            break
    return username, password
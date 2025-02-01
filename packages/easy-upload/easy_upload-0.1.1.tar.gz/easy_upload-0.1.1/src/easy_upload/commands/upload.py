from getpass import getpass
import os
import re

import time
from typer import Typer
import typer
from beaupy import confirm, prompt, select, select_multiple
from rich.console import Console
from pyfiglet import Figlet
from ..lib.upload import upload_package as pypi_upload
from typing_extensions import Annotated
from rich.progress import track
from ..lib.repo import getTOML, get_repos, add_repo
from ..lib.credentials import get_credential, set_cred
from ..lib.users import add_account

app = Typer()

def find_files(base_directory):
    tar_gz_files = []
    whl_files = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.tar.gz'):
                tar_gz_files.append(os.path.join(root, file))
            elif file.endswith('.whl'):
                whl_files.append(os.path.join(root, file))

    return tar_gz_files, whl_files

@app.command()
def upload(dry_run: Annotated[bool, typer.Option(help="If this is specified, the actual upload will not take place.")] = False):
    """Upload sdist/wheels to PyPI."""
    f = Figlet(font='slant')
    console = Console()
    console.print("[bold blue]" + f.renderText("EASY_UPLOAD") + "[/bold blue]")
    console.print("easy_upload [bold green]v0.1.0[/bold green]\n")
    toml = getTOML()
    repos = get_repos(toml=toml)
    repos_list = []
    for repo in repos:
        repos_list.append(repo["name"] + " (" + repo["url"] + ")")
    repos_list.append("Add New Repository...")
    select_repository = select(repos_list, cursor="🢧", cursor_style="cyan")
    if not select_repository == "Add New Repository...":
        start_index = select_repository.find('(') + 1
        end_index = select_repository.find(')')
        url = select_repository[start_index:end_index].strip()
        
        start_index = select_repository.rfind('(')
    else:
        repo_name = input("Enter Repository Label: ")
        url = input("Enter Repository URL: ")
        add_repo(repo_name, url, toml)
    repository = url
    accounts = []
    t = toml.read()
    for c in t["credential"]:
        cred = get_credential(url, c["name"])
        if cred:
            accounts.append(c["name"].split(",")[0] + " (" + c["name"].split(",")[1] + ")")
    accounts.append("Add New Account...")
    console.print("Select Login Account: ")
    select_account = select(accounts, cursor="🢧", cursor_style="cyan")
    if select_account == "Add New Account...":
        username, password = add_account(url)
    else:
        act = re.sub(r'(\w+)\s*\(\s*(\w+)\s*\)', r'\1,\2', select_account)
        username = act.split(",")[1]
        password = get_credential(url, act)
    tar_gz_files, whl_files = find_files(os.getcwd())
    tar_gz_files.extend(whl_files)
    files = tar_gz_files
    console.print("The following wheel/tar.gz was found. Which one do you want to upload?")
    upload_files = select_multiple(files, tick_character='✔', ticked_indices=[], maximal_count=None)
    while True:
        answer = input("Are there any other files to upload? (y/n): ").lower()
        if answer == "n":
            break
        elif answer == "y":
            upload_files.append(input("Enter File Path: "))
        else:
            pass
    
    console.print("Uploading...")
    if not dry_run:
        pypi_upload(files=upload_files, repository_url=repository, username=username, password=password)
    else:
        for i in track(range(100)):
            time.sleep(0.01)
    console.print("Done!")
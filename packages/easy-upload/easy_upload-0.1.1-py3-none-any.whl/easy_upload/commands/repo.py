from getpass import getpass
import os


from typer import Typer
from beaupy import confirm, prompt, select, select_multiple
from rich.console import Console
from pyfiglet import Figlet
from ..lib.repo import add_repo, get_repos
from rich.table import Table

app = Typer(name="repositories")

@app.command("get")
def get_repositories():
    f = Figlet(font='slant')
    console = Console()
    console.print("[bold blue]" + f.renderText("EASY_UPLOAD") + "[/bold blue]")
    console.print("easy_upload [bold green]v0.1.0[/bold green]\n")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("URL")
    for repo in get_repos():
        table.add_row(
            repo.get("name"), repo.get("url")
        )
    console.print(table)

@app.command("add")
def ad_repository(name: str, url: str):
    f = Figlet(font='slant')
    console = Console()
    console.print("[bold blue]" + f.renderText("EASY_UPLOAD") + "[/bold blue]")
    console.print("easy_upload [bold green]v0.1.0[/bold green]\n")
    add_repo(name, url)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("URL")
    for repo in get_repos():
        table.add_row(
            repo.get("name"), repo.get("url")
        )
    console.print(table)
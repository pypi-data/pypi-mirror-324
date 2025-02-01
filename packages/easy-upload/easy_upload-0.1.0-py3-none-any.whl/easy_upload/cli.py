from typer import Typer

from .commands import upload, repo

app = Typer(name="easy_upload")
app.add_typer(upload.app)
app.add_typer(repo.app)
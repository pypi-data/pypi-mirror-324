from typer import Typer

from .commands import upload

app = Typer(name="easy_upload")
app.add_typer(upload.app)
from twine.commands.upload import upload as twine_upload
from twine.settings import Settings

def upload_package(files, repository_url, username, password): twine_upload(Settings(username=username, password=password, repository_url=repository_url), dists=files)

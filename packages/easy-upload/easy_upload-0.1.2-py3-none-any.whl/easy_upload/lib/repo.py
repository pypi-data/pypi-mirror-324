import os

from tomlkit.toml_file import TOMLFile

def getTOML():
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "easy_upload.toml")
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write('[[repository]]\nname="pypi"\nurl="https://upload.pypi.org/legacy/"\n[[repository]]\nname="testpypi"\nurl="https://test.pypi.org/legacy/"\n[[credential]]\ntest = ""')
    return TOMLFile(file_path)

def get_repos(toml=None):
    if not toml:
        toml = getTOML()
    doc = toml.read()
    return doc["repository"]

def add_repo(name: str, url: str, toml=None):
    if not toml:
        toml = getTOML()
    doc = toml.read()
    doc.get("repository").append({"name": name, "url": url})
    toml.write(doc)
    

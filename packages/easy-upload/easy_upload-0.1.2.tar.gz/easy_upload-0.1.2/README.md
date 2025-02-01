# easy_upload
User-friendly Twine wrapper.
## Features
- Automatically search/easily select whl/tar.gz from current directory
## Requirements
- keyring backends
    - Freedesktop Secret Service (requires secretstorage)
    - KDE4 & KDE5 KWallet (requires dbus)
## Install
easy-upload can be installed from PyPI.
```
# pip
pip install easy-upload

# pipx
pipx install easy-upload
```
## How To Use
You can start by running `easy_upload upload`. It is not recommended to run it in your home directory, for example, due to its specification.
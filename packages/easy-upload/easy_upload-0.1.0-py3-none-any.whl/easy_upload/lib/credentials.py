import keyring
import keyring.util

import os
from .repo import getTOML

def set_cred(url: str, secret: str = None, label: str = "__token__"):
    value_to_store = secret

    keyring.set_password(url, label, value_to_store)

    toml = getTOML()
    doc = toml.read()
    doc.get("credential").append({"name": label})
    toml.write(doc)

def get_credential(url: str, username: str):
    backend = keyring.get_keyring()
    return backend.get_password(url, username)
import base64
import hashlib
import os
import sys
from getpass import getpass

import httpx
from pkginfo import Wheel, SDist
from typer import Typer



def upload(path: str, url: str="https://upload.pypi.org/legacy", username: str="__token__", password: str=""): 
    with open(path, "rb") as f:
        file_data = f.read()
        md5_hash = hashlib.md5(file_data).digest()
        md5_digest = base64.urlsafe_b64encode(md5_hash).decode('utf-8').rstrip('=')
        sha256_hash = hashlib.sha256(file_data).hexdigest()
        blake2_hash = hashlib.blake2b(file_data).hexdigest()
        file_name = os.path.basename(path)
        if file_name.endswith(".whl"):
            pkg = Wheel(path)
            version_info = sys.version_info
            metadata = {
                "action": "file_upload",
                "protocol_version": 1,
                "filename": file_name,
                "md5_digest": md5_digest,
                "sha256_digest": sha256_hash,
                "blake2_256_digest": blake2_hash,
                "filetype": "bdist_wheel",
                "pyversion": f"cp{version_info.major}{version_info.minor}",
                "metadata_version": pkg.metadata_version,
                "name": pkg.name,
                "version": pkg.version,
                "attestations": []
            }
        elif file_name.endswith(".tar.gz"):
            pkg = SDist(path)
            metadata = {
                "action": "file_upload",
                "protocol_version": 1,
                "filename": file_name,
                "md5_digest": md5_digest,
                "sha256_digest": sha256_hash,
                "blake2_256_digest": blake2_hash,
                "filetype": "bdist_wheel",
                "pyversion": "source",
                "metadata_version": pkg.metadata_version,
                "name": pkg.name,
                "version": pkg.version,
                "attestations": []
            }
        with httpx.Client() as client:
            auth = httpx.BasicAuth(username=username, password=password)
            resp = client.post(url, data=metadata, headers={"Content-Type": "multipart/form-data"}, files = {'upload-file': file_data}, auth=auth)
            print(resp.status_code)
            print(resp.text)
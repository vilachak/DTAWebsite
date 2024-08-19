import os
from pathlib import Path
import tempfile
import shutil


def handle_uploaded_file(file_path, source):
    ext = False
    if ext:
        suffix = os.path.splitext(source.name)[1]
    else:
        suffix = source.name
    fileDirectory = "./media/" + file_path + "/"
    Path(fileDirectory).mkdir(parents=True, exist_ok=True)
    fd, filepath = tempfile.mkstemp(suffix=suffix, dir=fileDirectory)
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(source, dest)
    os.close(fd)
    return filepath

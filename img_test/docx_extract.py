import zipfile
import shutil
import os

DOCX_PREFIX = 'word/media/'

with zipfile.ZipFile('file2.docx') as zf:
    for name in zf.namelist():
        if DOCX_PREFIX not in name \
                or name.index(DOCX_PREFIX) != 0:
            continue
        source = zf.open(name)
        target = open(os.path.join('.', 'asdf-'+os.path.basename(name)), 'wb')
        with source, target:
            shutil.copyfileobj(source, target)

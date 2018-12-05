import fitz
import zipfile
import shutil
import os

def _prefix(file_path):
    return os.path.splitext(file_path)[0]

DOCX_MEDIA_DIR = 'word/media/'

def extract_all(file_paths):
    extracted = []
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path)
        if ext == '.pdf':
            extracted.extend(extract_from_pdf(file_path))
        elif ext == '.docx':
            extracted.extend(extract_from_docx(file_path))
    return extracted

def extract_from_docx(file_path):
    prefix = _prefix(file_path)
    outfiles = []
    with zipfile.ZipFile(file_path) as zf:
        for name in zf.namelist():
            if DOCX_MEDIA_DIR not in name \
                    or name.index(DOCX_MEDIA_DIR) != 0:
                continue
            source = zf.open(name)
            outfile = '{} - {}'.format(prefix, os.path.basename(name))
            target = open(outfile, 'wb')
            with source, target:
                shutil.copyfileobj(source, target)
            outfiles.append(outfile)
    return outfiles


def extract_from_pdf(file_path):
    prefix = _prefix(file_path)
    outfiles = []
    doc = fitz.open(file_path)
    try:
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    outfile = '{} - p{}-{}.png'.format(prefix, i, xref)
                    if pix.n < 5:       # this is GRAY or RGB
                        pix.writePNG(outfile)
                    else:               # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.writePNG(outfile)
                        pix1 = None
                    pix = None
                    outfiles.append(outfile)
                except:
                    print('      failed to export image {} from pdf {}'.format(outfile, file_path))
                    pass
    finally:
        doc.close()
    return outfiles

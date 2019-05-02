import importlib
from data.semesters import *

semesters = [
    SEMESTER_16FA,
    SEMESTER_17SP,
    SEMESTER_17FA,
    SEMESTER_18SP,
#    SEMESTER_18FA,
#    SEMESTER_19SP,
]

data = [
    { **d, 'semester': sem }
    for sem in semesters
    for d in importlib.import_module('.x' + sem.lower(), package=__package__).data
]

for d in data:
    d['authors'] = '; '.join(sorted(
        ', '.join(name.strip() for name in author.split(','))
        for author in d['authors'].split(';')
    ))
    if 'tags' in d:
        d['tags'] = ', '.join(sorted(tag.strip() for tag in d['tags'].split(',')))

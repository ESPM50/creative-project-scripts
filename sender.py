import tempfile
import os

from functional import seq
from boxsdk import DevelopmentClient

from zotero import *
from img_extract import extract_from_pdf, extract_from_docx, extract_all
import box
import similarity


BOX_URL_PREFIX = 'https://berkeley.app.box.com/folder/'


def send_data(pieces, box_input_folder_id, collection_name, semester_tag):
    kwargs = {}
    print('BOX', end=' ')
    kwargs['pieces'] = pieces
    kwargs['semester_tag'] = semester_tag
    kwargs['box_folder_id'] = box_input_folder_id
    kwargs['box_client'] = DevelopmentClient()
    coll = get_or_make_collection(collection_name)
    kwargs['coll_id'] = coll['key']

    kwargs.update(sort_box_folders(**kwargs))
    kwargs.update(meta_to_zot(**kwargs))
    kwargs.update(files_to_zot(**kwargs))



def parse_authors(authors_str):
    return seq(authors_str.split(';')) \
        .map(lambda last_first: tuple(x.strip() for x in last_first.split(','))) \
        .to_list()



def convert_data(row, semester_tag=None):
    template = zot.item_template('artwork')
    # {'itemType': 'artwork', 'title': '', 'creators': [{'creatorType': 'artist', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'artworkMedium': '', 'artworkSize': '', 'date': '', 'language': '', 'shortTitle': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'url': '', 'accessDate': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}

    template['title'] = row['title']
    template['creators'] = seq(parse_authors(row['authors'])) \
        .map(lambda last_first: {
            'creatorType': 'artist',
            'lastName': last_first[0],
            'firstName': last_first[1]
        }) \
        .to_list()

    if 'desc' in row:
        template['abstractNote'] = row['desc']
    if 'size' in row:
        template['artworkSize'] = row['size']
    if 'medium' in row:
        template['artworkMedium'] = row['medium']
    if 'tags' in row:
        template['tags'] = seq(row['tags'].split(',')) \
            .map(lambda tag: 'raw:' + tag.strip()) \
            .map(make_tag).to_list()

    if semester_tag:
        template['tags'].append(make_tag(semester_tag)) # add semester tag

    template['url'] = BOX_URL_PREFIX + row['box_id']
    return template



def folder_name(row):
    title = row['title'].strip()
    authors_str = row['authors'].strip()
    for ic in [ '/', '\\', '.', '..' ]:
        title = title.replace(ic, '_')
    authors_str = '; '.join(seq(parse_authors(authors_str))
        .map(lambda last_first: ', '.join(last_first)))
    return '{} by {}'.format(title, authors_str)



def file_name(name):
    for ic in [ '\\', '/', ':', '*', '"', '<', '>', '?', '|' ]:
        name = name.replace(ic, '_');
    return name



def sort_box_folders(pieces, box_folder_id, box_client, **kwargs):
    print('sorting box folders')
    folder = box_client.folder(box_folder_id)
    box_files = box.list_all_files(folder)
    subfolders_dict = { f.name: f for f in folder.get_items() if f._item_type == 'folder' }

    groups = { i: [] for i in range(len(pieces)) }
    ungrouped = []

    for box_file in box_files:
        def score(i):
            a = box_file.name.lower()
            b = pieces[i]['authors'].lower()
            return similarity.substrsim(a, b)[1]
        best_piece = max(range(len(pieces)), key=score)
        if score(best_piece) < 0.2:
            print('    NO GOOD PIECE FOUND FOR: ' + box_file.name)
            ungrouped.append(box_file)
        else:
            groups[best_piece].append(box_file)

    print()
    for i, fs in groups.items():
        piece = pieces[i]
        print('  ' + str(piece))
        for f in fs:
            print('    ' + f.name)
        print()

    # Move ungrouped files
    print('  moving ungrouped ({})'.format(len(ungrouped)))
    for f in ungrouped:
        f.move(folder)


    # Move grouped files
    print('  moving groups')
    new_pieces = []
    for i, group in groups.items():
        piece = pieces[i]
        if not group:
            print('    NO ITEMS FOUND FOR {}'.format(piece))
            continue # no items found

        subfolder_name = folder_name(piece)
        if subfolder_name in subfolders_dict:
            subfolder = subfolders_dict[subfolder_name]
        else:
            subfolder = folder.create_subfolder(subfolder_name)

        for f in group:
            f.move(subfolder)

        piece['box_id'] = subfolder.id
        new_pieces.append(piece)

    print('done sorting box folders')
    return { 'new_pieces': new_pieces }



def meta_to_zot(new_pieces, coll_id, semester_tag, **kwargs):
    print('creating item metadata in zotero')

    existing_titles = seq(zot.collection_items_top(coll_id)) \
        .map(lambda x: x['data']) \
        .filter(lambda x: 'parentItem' not in x) \
        .map(lambda x: x['title']) \
        .to_set()

    templates = seq(new_pieces) \
        .map(lambda x: convert_data(x, semester_tag=semester_tag)) \
        .filter(lambda x: x['title'] not in existing_titles) \
        .to_list()

    items_resp = zot.create_items(templates)

    if (items_resp['failed']):
        raise ValueError('Failed to create items: {}'.format(items_resp['failed']))

    succ = items_resp['successful']
    for item in succ.values():
        zot.addto_collection(coll_id, item)

    print('done, created {} items'.format(len(succ)))
    return {}



def files_to_zot(coll_id, box_client, **kwargs):
    print('moving files to zotero')

    items = [ x['data'] for x in zot.collection_items(coll_id) ]
    print('found {} items'.format(len(items)))

    attachments = {}
    parent_items = []
    for item in items:
        if 'parentItem' in item:
            parentId = item['parentItem']
            if parentId:
                attachments[parentId] = attachments.get(parentId, set())
                attachments[parentId].add(item['filename'])
                continue
        if 'url' not in item \
                or BOX_URL_PREFIX not in item['url'] \
                or item['url'].index(BOX_URL_PREFIX) != 0:
            print('  item has unknown url: {}'.format(item['key']))
            continue
        parent_items.append(item)

    for item in parent_items:
        folder_id = item['url'][len(BOX_URL_PREFIX):]
        folder = box_client.folder(folder_id)

        existing_attachments = attachments.get(item['key'], [])
        boxitems = [ x for x in folder.get_items() if x.name not in existing_attachments ]

        if not boxitems:
            print('  no new files to download for {}'.format(item['title']))
            continue

        print('  downloading {} files for {}'.format(len(boxitems), item['title']))
        with tempfile.TemporaryDirectory() as temp_dir:

            file_paths = [ os.path.join(temp_dir, file_name(boxitem.name)) for boxitem in boxitems ]
            for file_path, boxitem in zip(file_paths, boxitems):
                print('    downloading {}'.format(boxitem.name))
                with open(file_path, 'wb') as temp_file:
                    boxitem.download_to(temp_file)

            print('  extracting')
            extracted_paths = extract_all(file_paths)
            print('    extracted {}'.format(len(extracted_paths)))

            print('  uploading to zotero')
            all_paths = file_paths + extracted_paths
            while all_paths:
                paths_50 = all_paths[:50]
                all_paths = all_paths[50:]
            zot.attachment_simple(paths_50, parentid=item['key'])

    print('done moving to zotero')
    return {}

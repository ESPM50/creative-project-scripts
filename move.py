import tempfile
import os

from functional import seq
from boxsdk import DevelopmentClient

from zotero import *
from img_extract import extract_from_pdf, extract_from_docx, extract_all

BOX_URL_PREFIX = 'https://berkeley.app.box.com/folder/'

COLLECTION_NAME = 'fa16_0'

# https://docs.google.com/spreadsheets/d/1P4p-H_lgakBGMWgpgYMGh696gwPBjjfVTyd2USY16Og/edit#gid=139929664
data = [
    ('A Brief Visual History of San Francisco ', 'Morales, Daniela', 'culture and enviroment,maps,san francisco golden gate', '57524447421'),
    ('After (Im)possibilities: A Remix of History/Sameness', 'Harcourt, Rebecca;Shin, Yuju', 'culture,expansion,society,nature,environment', '57525074384'),
    ('Artistic Rendition of a Changing Landscape', 'Valdez, Madeleine', 'environmental history,urban development,bay area', '57524978420'),
    ('Changing landscape in the New World due to colonization', 'Kim, Laura;Patel, Kishan;Quin, John', 'colonization,change,nature,californian indian displacement', '57525052768'),
    ('Food and Footprints', 'Kim, Allison;Yeo, Ji Hun', 'carbon footprint,food,sustainability,personal impact,different diets,greenhouse gases,environmental sustainability', '57524402082'),
    ('Instrument and Sublime', 'Lee, Christian', 'chinese laborers,transcontinental railroad,exclusion from americanization and american history', '57524455169'),
    ('Water in California', 'Wu, Yi-Chi', 'water,development and exploitation,landscape change', '57524466275'),
]

def convert_data(row):
    title, authors_str, tags, box_id = row
    template = zot.item_template('artwork')
    template['title'] = title
    template['creators'] = seq(authors_str.split(';')) \
        .map(lambda last_first: last_first.split(', ')) \
        .map(lambda last_first: {
            'creatorType': 'artist',
            'lastName': last_first[0],
            'firstName': last_first[1] }) \
        .to_list()
    template['tags'] = seq(tags.split(',')) \
        .map(lambda tag: 'raw:' + tag) \
        .map(make_tag).to_list()

    template['tags'].append(make_tag('fa16')) # add semester tag

    template['url'] = BOX_URL_PREFIX + box_id
    return template

def meta_to_zot(coll_id, **kwargs):
    print('creating item metadata in zotero')

    templates = seq(data) \
        .map(convert_data) \
        .to_list()
    items_resp = zot.create_items(templates)

    if (items_resp['failed']):
        print('Failed to create items:', items_resp['failed'])

    succ = items_resp['successful']
    for item in succ.values():
        zot.addto_collection(coll_id, item)

    print('done, created {} items'.format(len(succ)))

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

        existing_attachments = attachments[item['key']]
        boxitems = [ x for x in folder.get_items() if x.name not in existing_attachments ]

        if not boxitems:
            print('  no new files to download for {}'.format(item['title']))
            continue

        print('  downloading {} files for {}'.format(len(boxitems), item['title']))
        with tempfile.TemporaryDirectory() as temp_dir:

            file_paths = [ os.path.join(temp_dir, boxitem.name) for boxitem in boxitems ]
            for file_path, boxitem in zip(file_paths, boxitems):
                print('    downloading {}'.format(boxitem.name))
                with open(file_path, 'wb') as temp_file:
                    boxitem.download_to(temp_file)

            print('  extracting')
            extracted_paths = extract_all(file_paths)
            print('    extracted {}'.format(len(extracted_paths)))

            print('  uploading to zotero')
            zot.attachment_simple(file_paths + extracted_paths, parentid=item['key'])

    print('done moving to zotero')




if __name__ == '__main__':
    kwargs = {}
    print('BOX', end=' ')
    kwargs['box_client'] = DevelopmentClient()
    coll = get_or_make_collection(COLLECTION_NAME)
    kwargs['coll_id'] = coll['key']

    if coll['meta']['numItems'] <= 0:
        meta_to_zot(**kwargs)
    files_to_zot(**kwargs)

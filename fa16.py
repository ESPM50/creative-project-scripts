import tempfile
import os

from zotero import *
from functional import seq
from boxsdk import DevelopmentClient

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
    template['url'] = BOX_URL_PREFIX + box_id
    return template

def meta_to_zot(coll_id, **kwargs):
    templates = seq(data) \
        .map(convert_data) \
        .to_list()
    items_resp = zot.create_items(templates)

    if (items_resp['failed']):
        print('Failed to create items:', items_resp['failed'])

    for item in items_resp['successful'].values():
        zot.addto_collection(coll_id, item)

def files_to_zot(coll_id, box_client, **kwargs):
    items = zot.collection_items(coll_id)
    for item in items:
        if 'url' not in item['data'] or \
                item['data']['url'].index(BOX_URL_PREFIX) != 0:
            print('item has unknown url:', item['key'])
            continue

        folder_id = item['data']['url'][len(BOX_URL_PREFIX):]
        folder = box_client.folder(folder_id)
        items = folder.get_items()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_fds, temp_file_names = zip(*[ tempfile.mkstemp(dir=temp_dir) for _ in items ])
            for temp_fd in temp_fds:
                os.close(temp_fd)

            for item, temp_file_name in zip(items, temp_file_names):
                with open(temp_file_name) as temp_file:
                    item.download_to(temp_file)

            print(temp_file_names)
            input()
            break
            # zot.attachment_simple(temp_file_names, parentid=item['key'])




if __name__ == '__main__':
    kwargs = {}
    kwargs['box_client'] = DevelopmentClient()
    kwargs['coll_id'] = get_or_make_collection(COLLECTION_NAME)['key']

    # meta_to_zot(**kwargs)
    files_to_zot(**kwargs)

import tempfile
import os

from functional import seq
from boxsdk import DevelopmentClient

from zotero import *
from img_extract import extract_from_pdf, extract_from_docx, extract_all
import box
import similarity

BOX_URL_PREFIX = 'https://berkeley.app.box.com/folder/'

COLLECTION_NAME = 'sp17_0'
SEMESTER_TAG = 'sp17'

# https://docs.google.com/spreadsheets/d/1P4p-H_lgakBGMWgpgYMGh696gwPBjjfVTyd2USY16Og/edit#gid=139929664
data = [
    ('442nd Regimental Combat Team', 'Johnson, Madeleine ', 'family searching for the american dream,ww2,442nd regimental combat team'),
    ('Acculturation of Chinese Immigrants in San Francisco', 'Wang, Alex;Wu, Guang', 'assimilation,acculturation,chinese immigrants,immigration,chinese-american'),
    ('An Ecosystem\'s Intervention for Pesky People', 'Nussbaum, Jasper;Schiff, Anna', 'human impact,socal mediterranean ecosystem,children\'s book,decline in environmental integrity,extent of human culpability,possible restorative actions'),
    ('Animal Agriculture', 'Carabuena, Sara Kate', 'animal agriculture,environmental impact,climate change'),
    ('Colonization in the Northeast', 'Montanez, Martha', 'fur trade,introduction to catholicism,trading among northeastern tribes'),
    ('Commodification of Nature in a Changing Environment', 'Naik, Nishali', 'natural resources,big business,pollution'),
    ('Images ', 'Mallit, Ben', 'asian american immigrants,ecology and california marine biology,worster\'s analytical framework'),
    ('Continuities and Change over time in the Social and Political Attitudes towards the Chinese over the 19th to 20th centuries', 'Huang, Angela', 'federal policies/social reactions,labor,immigration,'),
    ('Contrasting Realities ', 'Erin , Cain ', 'environmental justice,ecosystems,exploitation'),
    ('Deer to Me', 'Jung, Catherine', 'natural resources,assimilation and acculturation,family history'),
    ('Eastern Sunset', 'Hwang, Anna;Won, Jeanie;Wong, Eric', 'chinese immigration,eastern and western agriculture,cultural differences,agriculture,california,immigration'),
    ('Environmental Effects of the Meat Industry ', 'Wood, Melissa', 'meat industry,environmental pollution,methane emission'),
    ('Environmentally Mindful', 'Johnson, Marisa', 'environmental education,sustainability,propaganda'),
    ('Film Series: Water in California', 'Sanchez Alcaraz, Andy', 'water resource management,water drought ca,water use'),
    ('Four Pieces on Nature', 'Chen, Fei', 'music,fire usage,katrina'),
    ('Issei', 'Jow, Owen', 'japanese cultural identity,property rights,nursery industry'),
    ('leave only footprints', 'Pearson, Kate', 'human impact on environment,natural/manmade material,interaction/performance with nature'),
    ('Modeling the Path to Disaster', 'Kim, Yoona;Suresh, Sahana;Tang, Sarah', 'racially differentiated risk,hurricane katrina,landscape in new orleans,la'),
    ('Natural skin care ', 'Ajayi, Iyioluwa;Nguyen, Vy ', 'skin care products,healthcare,environment,beauty'),
    ('Nature and Civilization Collide ', 'Anderson , Julia ', 'california topography,erosion,manmade structures'),
    ('Net-Zero Application', 'Acuna, Michelle', 'affordable housing,environmental justice,green architecture'),
    ('Oxford Tract Resistance', 'Hernandez, Lauren;White, Angela ', 'student activism,community engagement,environmental education'),
    ('Personal history of Chinese American women ', 'zhan, shuya', 'chinese immigration,resistance,women\'s role'),
    ('Pesticides', 'Li, Jeffrey;Le, Sabrina;Zhong, Justin', 'naled,ddt,methyl bromine,methyl bromide'),
    ('Project Short Story', 'Fann, Amy;Chu, Brenton', 'bp oil spill,identity,preservation of natural resources,environmental preservation'),
    ('Ceiling to the Sand', 'Campos, Josh', 'systemic poverty,resource management,power'),
    ('Sketch series on the Ohlone People\'s natural resource use and interaction', 'Wagner, Emily', 'ohlone,natural resources,interaction with nature'),
    ('The Chinese Immigrant Story', 'Lin, Helen;Thai, Thanh Thanh. ', 'chinese immigrant experience,california gold rush,transcontinental railroad'),
    ('The conflict of man and nature', 'Turnbull, Chase', 'man and nature,nature as sacred,nature as a resource'),
    ('the ecological Indian and his land ', 'Babikian, Karnie', 'woodland indians pre contact,cultural appreciation,niche in nature/land'),
    ('The Faces of Hurricane Katrina', 'Mateo, Crystal', 'hurricane katrina,individual impact,environmental racism'),
    ('The Gold Rush', 'Kim, Ashley', 'gold rush,mining,immigrants'),
    ('Hey, CAreful with that WATER', 'Wu, Lisa', 'change in landscape and land use in california'),
    ('Transition of American Views on Natural Resources', 'Kim, Heidi;Li, Amy', 'views of nature,native americans,europeans'),
]

def convert_data(row):
    title, authors_str, tags, box_id = map(lambda x: x.strip(), row)
    template = zot.item_template('artwork')
    template['title'] = title
    template['creators'] = seq(authors_str.split(';')) \
        .map(lambda last_first: [ x.strip() for x in last_first.split(', ') ]) \
        .map(lambda last_first: {
            'creatorType': 'artist',
            'lastName': last_first[0],
            'firstName': last_first[1] }) \
        .to_list()
    template['tags'] = seq(tags.split(',')) \
        .map(lambda tag: 'raw:' + tag.strip()) \
        .map(make_tag).to_list()

    template['tags'].append(make_tag(SEMESTER_TAG)) # add semester tag

    template['url'] = BOX_URL_PREFIX + box_id
    return template

def folder_name(row):
    title, authors_str, _ = map(lambda s: s.strip(), row)
    for ic in [ '/', '\\', '.', '..' ]:
        title = title.replace(ic, '_')
    return '{} by {}'.format(title, authors_str)



def sort_box_folders(pieces, box_folder_id, box_client, **kwargs):
    print('sorting box folders')
    folder = box_client.folder(box_folder_id)
    subfolders_dict = { f.name: f for f in folder.get_items() if f._item_type == 'folder' }
    box_files = box.list_all_files(folder)

    groups = { k: [] for k in pieces }

    for box_file in box_files:
        def key(assign):
            a = box_file.name.lower()
            b = assign[1].lower()
            return similarity.substrsim(a, b)[1]
        best_piece = max(pieces, key=key)
        groups[best_piece].append(box_file)

    print()
    for k, fs in groups.items():
        print('  ' + str(k))
        for f in fs:
            print('    ' + f.name)
        print()

    print('  moving groups')

    new_pieces = []
    for piece, group in groups.items():
        if not group:
            continue # no items found

        subfolder_name = folder_name(piece)
        if subfolder_name in subfolders_dict:
            subfolder = subfolders_dict[subfolder_name]
        else:
            subfolder = folder.create_subfolder(subfolder_name)

        new_pieces.append(piece + (subfolder.id,))

        for f in group:
            f.move(subfolder)

    print('done sorting box folders')
    return new_pieces



def meta_to_zot(pieces, coll_id, **kwargs):
    print('creating item metadata in zotero')

    templates = seq(pieces) \
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

        existing_attachments = attachments.get(item['key'], [])
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
    kwargs['pieces'] = data
    kwargs['box_folder_id'] = '57860927765'
    kwargs['box_client'] = DevelopmentClient()
    coll = get_or_make_collection(COLLECTION_NAME)
    kwargs['coll_id'] = coll['key']

    kwargs['pieces'] = sort_box_folders(**kwargs)
    if coll['meta']['numItems'] <= 0:
        meta_to_zot(**kwargs)
    files_to_zot(**kwargs)

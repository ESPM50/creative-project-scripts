import os
import requests

from pyzotero import zotero

ZOTERO_LIBRARY_ID = '2250084'
ZOTERO_LIBRARY_TYPE = 'group'
ZOTERO_API_KEY = os.environ['ZOTERO_API_KEY']

zot = zotero.Zotero(ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE, ZOTERO_API_KEY)

def get_or_make_collection(name):
    top_collections = zot.collections_top()
    for collection in top_collections:
        if collection['data']['name'] == name:
            return collection

    result = zot.create_collections([
        { 'name': name }
    ])
    return result['successful']['0']

def make_tag(tag_str):
    return { 'tag': tag_str, 'type': 1 }

def get_zotero_file_url(item_key):
    return f'https://api.zotero.org/{ZOTERO_LIBRARY_TYPE}s/{ZOTERO_LIBRARY_ID}/items/{item_key}/file?v=3&key={ZOTERO_API_KEY}'

def get_zotero_file_stream(item_key):
    url = get_zotero_file_url(item_key)
    return requests.get(url, stream=True).raw

def get_zotero_item_url(item_key):
    return f'https://www.zotero.org/{ZOTERO_LIBRARY_TYPE}s/{ZOTERO_LIBRARY_ID}/items/{item_key}'

# if __name__ == '__main__':

#     template = zot.item_template('artwork')
#     template['creators'][0]['firstName'] = 'Monty'
#     template['creators'][0]['lastName'] = 'Cantsin'
#     template['title'] = 'Maris Kundzins: A Life'
#     resp = zot.create_items([ template ])
#     print(resp)

#     # items = zot.top(limit=5)

#     # for item in items:
#     #     print('Item Type: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))

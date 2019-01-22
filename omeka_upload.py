import requests
import json
import os

from zotero import *
import omeka


ITEM_SET_TITLE = 'ESPM 50 Creative Projects'

SEMESTERS = {
  'fa16': '2016 Fall',
  'sp17': '2017 Spring',
  'fa17': '2017 Fall',
  'sp18': '2018 Spring'
}

ITEM_SET_ALL = omeka.create_or_get_item_set(ITEM_SET_TITLE, 'All ' + ITEM_SET_TITLE)
ITEM_SET_IDS = {
  None: ITEM_SET_ALL['o:id']
}

for tag, semester in SEMESTERS.items():
  item_set = omeka.create_or_get_item_set(ITEM_SET_TITLE + ' - ' + semester,
      f'{ITEM_SET_TITLE} for the {semester} semester.')
  ITEM_SET_IDS[tag] = item_set['o:id']

def upload_zotero_item(item):
  data = item['data']

  title = data['title']
  creators_arr = data['creators']
  description = data['abstractNote']
  medium = data['artworkMedium']
  size = data['artworkSize']
  box_url = data['url']
  tags = data['tags']

  children = zot.children(item['key'])
  files = [
    (child['data']['filename'], get_zotero_file_stream(child['key']))
    for child in children
  ]

  creators = [
    creator['lastName'] + ', ' + creator['firstName']
    for creator in creators_arr
  ]

  item_sets = [ ITEM_SET_IDS[None] ]
  for tag in tags:
    x = tag['tag']
    if x in ITEM_SET_IDS:
      item_sets.append(ITEM_SET_IDS[x])

  omeka.create_item(title, description, creators, files, item_sets, medium, size)

# TODO don't create items if they already exist.

if '__main__' == __name__:
  items = zot.top(tag="fav")
  for item in items:
    print(f'Uploading item "{item["data"]["title"]}" ({item["key"]})')
    upload_zotero_item(item)


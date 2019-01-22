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
  date = data['dateAdded']

  box_url = data['url']
  zot_url = get_zotero_item_url(item['key'])
  urls = [
    ('Box Folder', box_url),
    ('Zotero Item', zot_url)
  ]

  tags = data['tags']

  children = zot.children(item['key'])
  # files = [
  #   (child['data']['filename'], get_zotero_file_stream(child['key']))
  #   for child in children
  # ]
  files = [
    (child['data']['filename'], get_zotero_file_url(child['key']))
    for child in children
    if not child['data']['filename'].endswith('docx') # TODO allow DOCX
    # application/vnd.openxmlformats-officedocument.wordprocessingml.document
    # https://omeka.org/forums-legacy/topic/xlsx-file-types-not-viewing-correctly/#post-100559
  ]
  print('\tChild files:')
  for x in files:
    print('\t\t', x[0])

  creators = [
    creator['lastName'] + ', ' + creator['firstName']
    for creator in creators_arr
  ]

  item_sets = [ ITEM_SET_IDS[None] ]
  for tag in tags:
    x = tag['tag']
    if x in ITEM_SET_IDS:
      item_sets.append(ITEM_SET_IDS[x])

  omeka.create_or_get_item(title, description,
      creators=creators, files=files, item_sets=item_sets, medium=medium,
      size=size, date=date, urls=urls)

# TODO don't create items if they already exist.

if '__main__' == __name__:
  items = zot.top(tag="fav")
  for item in items:
    print(f'Uploading item "{item["data"]["title"]}" ({item["key"]})')
    upload_zotero_item(item)
    print()

# item = zot.item('ARWR7JSN')
# upload_zotero_item(item)


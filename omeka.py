import requests
import json
import os

from functional import seq

OMEKA_KEY_IDENTITY = os.environ['OMEKA_KEY_IDENTITY']
OMEKA_KEY_CREDENTIAL = os.environ['OMEKA_KEY_CREDENTIAL']

OMEKA_BASE_URL = "http://communitiesandlandscapes.org/api"


def create_or_get_item_set(title, description):
  url = OMEKA_BASE_URL + '/item_sets'

  querystring = {
      'key_identity': OMEKA_KEY_IDENTITY,
      'key_credential': OMEKA_KEY_CREDENTIAL,
      'search': title
  }

  response = requests.get(url, params=querystring)
  if response.status_code // 100 != 2:
    raise Exception(response.text)

  match = seq(json.loads(response.text)) \
    .find(lambda x: x["dcterms:title"][0]["@value"] == title)
  if match: # item set already exists
    return match

  # otherwise, create the item set
  data = {
    "@type": [
      "o:ItemSet",
      "dctype:Collection"
    ],
    "o:resource_class": {
      "@id": "http://communitiesandlandscapes.org/api/resource_classes/23",
      "o:id": 23
    },
    "o:resource_template": {
      "@id": "http://communitiesandlandscapes.org/api/resource_templates/8",
      "o:id": 8
    },
    "dcterms:title": [
      {
        "type": "literal",
        "property_id": 1,
        "property_label": "Title",
        "is_public": True,
        "@value": title
      }
    ],
    "dcterms:description": [
      {
        "type": "literal",
        "property_id": 4,
        "property_label": "Description",
        "is_public": True,
        "@value": description
      }
    ]
  }

  response = requests.post(url, params=querystring, json=data)
  if response.status_code // 100 != 2:
    raise Exception(response.text)
  return json.loads(response.text)



def create_item(title, description, creators, files, item_sets, medium=None, size=None):
  url = OMEKA_BASE_URL + "/items"

  querystring = {
      'key_identity': OMEKA_KEY_IDENTITY,
      'key_credential': OMEKA_KEY_CREDENTIAL
  }

  data = {
    "@type": [
      "o:Item",
      "dctype:Collection"
    ],
    "o:resource_class": {
      "@id": "http://communitiesandlandscapes.org/api/resource_classes/90",
      "o:id": 23
    },
    "o:resource_template": {
      "@id": "http://communitiesandlandscapes.org/api/resource_templates/4",
      "o:id": 7
    },
    "o:item_set": [
      {
        "@id": "http://communitiesandlandscapes.org/api/item_sets/" + str(x),
        "o:id": x
      }
      for x in item_sets
    ],
    "dcterms:title": [
      {
        "type": "literal",
        "property_id": 1,
        "property_label": "Title",
        "is_public": True,
        "@value": title
      }
    ],
    "dcterms:description": [
      {
        "type": "literal",
        "property_id": 4,
        "property_label": "Description",
        "is_public": True,
        "@value": description or '<no description>'
      }
    ],
    "dcterms:subject": [
      {
        "type": "literal",
        "property_id": 3,
        "property_label": "Subject",
        "is_public": True,
        "@value": "ESPM 50 Creative Projects"
      }
    ],
    "dcterms:creator": [
      {
        "type": "literal",
        "property_id": 2,
        "property_label": "Creator",
        "is_public": True,
        "@value": creator
      }
      for creator in creators
    ],
    "dcterms:type": [
      {
        "type": "literal",
        "property_id": 8,
        "property_label": "Type",
        "is_public": True,
        "@value": "Artwork"
      }
    ],
    "dcterms:publisher": [
        {
            "type": "literal",
            "property_id": 5,
            "property_label": "Publisher",
            "is_public": True,
            "@value": "ESPM 50"
        }
    ],
    "dcterms:issued": [
      {
        "type": "literal",
        "property_id": 23,
        "property_label": "Date Issued",
        "is_public": True,
        "@value": "UPLOAD DATE/DATE ISSUED"
      }
    ],
    "dcterms:license": [
      {
        "type": "literal",
        "property_id": 49,
        "property_label": "License",
        "is_public": True,
        "@value": "Unknown"
      }
    ]
  }

  if medium:
    data['dcterms:medium'] = [
      {
        "type": "literal",
        "property_id": 26,
        "property_label": "Medium",
        "is_public": True,
        "@value": medium
      }
    ]
  if size:
    data['dcterms:extent'] = [
      {
        "type": "literal",
        "property_id": 25,
        "property_label": "Extent",
        "is_public": True,
        "@value": size
      }
    ]

  files_dict = { f'file[{i}]': f for i, f in enumerate(files) }

  data['o:media'] = [
      {
        "o:ingester": "upload",
        "file_index": i
      }
      for i in range(len(files))
  ]

  response = requests.post(url, params=querystring, data={'data': json.dumps(data)}, files=files_dict)
  if response.status_code // 100 != 2:
    raise Exception(response.text)
  return json.loads(response.text)

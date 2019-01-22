import re

from functional import seq
from zotero import *

KEYWORDS = {
  'Asian-American': [
    'asian-american identity', '442nd', 'japan', 'japanese', 'exclusion',
    'chinese', 'asian', 'issei'
  ],
  'Japanese-American': [
    'issei', 'japan', 'japanese', '442nd'
  ],
  'Chinese-American': [
    'chinese', 'exclusion'
  ],
  'Urbanism': [
    'city', 'urban', 'gentrification'
  ],
  'Environmentalism': [
    'environmentalism', 'nature', 'environment', 'animal', 'agriculture',
    'oil', 'ddt', 'ecology', 'erosion', 'carbon', 'marine', 'biology',
    'pollution', 'urban', 'pesticide', 'clean power', 'co2', 'yellowstone'
  ],
  'Resource Extraction': [
    'gold', 'mining', 'panning', 'hydraulic', 'drilling', 'oil',
    'fur trade', 'beaver', 'pelt'
  ],
  'Railroad': [
    'intercontinental', 'rail'
  ],
  'Natural Resource Management': [
    'natural', 'resource', 'oil', 'ddt', 'gas', 'water',
    'harvest', 'corn', 'bean', 'squash', 'fire'
  ],
  'Capitalism': [
    'capitalism', 'business', 'affordable', 'oil',
    'fur trade', 'urban', 'development', 'gentrification'
  ],
  ' Modes of Incorporation': [
    'acculturation', 'assimilation', 'incorporation'
  ],
  'Bay Area': ['bay area', 'ohlone', 'san francisco', 'golden gate', 'oakland'],
  # 'Central Valley': ['central valley', 'delta', 'san joaquin'],
  # 'California': ['california', 'la', 'ca'],
  'Family': ['family', 'american dream'],
  'Katrina': ['katrina', 'hurricane', 'levy'],
  'Culture': ['culture', 'music'],
  'Water': ['water', 'drought', 'hydro'],
  'Indians': [
    'indians', 'indian', 'native americans', 'woodland', 'corn', 'bean',
    'squash', 'yurok', 'klammath', 'ohlone'
  ],
  #'Yurok': ['yurok', 'klammath'],
  'Maps': ['map']
}

groups = {}
groups[None] = [] # ungrouped
for key in KEYWORDS.keys():
  groups[key] = []

for item in zot.top():
  title = item['data']['title'].lower()
  desc = item['data']['abstractNote'].lower()
  tags = item['data']['tags']
  key_found = False
  for key, keywords in KEYWORDS.items():
    for keyword in keywords:
      if re.search('\\b' + keyword, title) \
          or re.search('\\b' + keyword, desc) \
          or seq(tags).exists(lambda x: re.search('\\b' + keyword, x['tag'].lower())):
        groups[key].append(item)
        key_found = True
        break
  if not key_found:
    groups[None].append(item)

for key, items in groups.items():
  print(key)
  for item in items:
    print('\t', item['data']['title'], '::', item['data']['abstractNote'][:50])
  print('\n')

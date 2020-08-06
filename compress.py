##
## Combines all JSON files and compresses the data by removing
## certain fields that are not needed for querying. Some fixes
## are applied, e.g. trimming whitespace.
##

import json
from glob import glob


def read_json_file(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def write_json_file(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=2, sort_keys=True)


original_data = {}
for filename in glob('data/?.json'):
    original_data.update(read_json_file(filename))

compressed_data = {}
for k, v in original_data.items():
    v.pop('wordset_id', None)
    v.pop('editors', None)
    v.pop('contributors', None)

    v['word'] = v['word'].strip()
    for m in v.get('meanings', []):
        m.pop('id', None)
        m['def'] = m['def'].strip()

        if 'example' in m:
            m['example'] = m['example'].strip()

    compressed_data[k.lower()] = v

write_json_file('compressed_data.json', compressed_data)

from gi.repository import DModel, EosShard

import argparse
import os
import operator
import itertools
import json
import sys
import csv


def filter_out_internal(tags):
    '''Filter out internal tags.'''
    return [t for t in tags if not t.startswith('Ekn')]


def first_n_values(indexable, n, fillvalue=None):
    '''Get the first n values from indexable.'''
    return map(operator.itemgetter(0),
               itertools.zip_longest(indexable[:n], [None] * n, fillvalue=fillvalue))


def first_n_words(text, n):
    '''Get first n words from title or pad.'''
    return first_n_values(text.split(), n, fillvalue='')


def yield_entries(apps):
    for app in apps:
        domain = DModel.Engine.get_default().get_domain_for_app(app)

        shards = domain.get_shards()
        for shard in shards:
            records = shard.list_records()
            for record in records:
                blob = record.metadata

                if blob is None:
                    continue
                bytes = blob.load_contents()
                metadata = json.loads(bytes.get_data().decode())

                if metadata.get('contentType', None) == 'text/html':
                    record = [
                        os.path.join(app, record.get_hex_name()),
                        app,
                        *first_n_words(metadata.get('title', ''), 3),
                        *first_n_values(filter_out_internal(metadata.get('tags', [])), 1)
                    ]
                    yield record



def main():
    '''Parse arguments, dump apps.'''
    parser = argparse.ArgumentParser('App Dumper')
    parser.add_argument('app',
                        nargs='*',
                        type=str,
                        help='App IDs to dump')

    result = parser.parse_args()

    writer = csv.writer(sys.stdout)
    writer.writerow(['itemId', 'appId', 'titleWord1', 'titleWord2', 'titleWord3', 'tag1', 'tag2', 'tag3'])
    for entry in yield_entries(result.app):
        writer.writerow(entry)

if __name__ == "__main__":
    main()

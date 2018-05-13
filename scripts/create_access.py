from gi.repository import DModel, EosShard

import argparse
import time
import os
import operator
import itertools
import json
import random
import sys
import csv

def random_combination(iterable, r):
    '''Random selection from itertools.combinations(iterable, r)'''
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)

def main():
    '''Parse arguments, dump apps.'''
    parser = argparse.ArgumentParser('App Dumper')
    parser.add_argument('content',
                        type=str,
                        help='Content CSV file')
    parser.add_argument('access',
                        type=str,
                        help='Access CSV file')
    result = parser.parse_args()

    try:
        with open(result.access, 'r') as f:
            last_accesses = {
                r[0]: r[1] for r in itertools.islice(csv.reader(f), 1, None)
            }
    except IOError:
        last_accesses = {}

    with open(result.content, 'r') as f:
        known_content = [r for r in itertools.islice(csv.reader(f), 1, None)]

    for row in random_combination(known_content, 50):
        itemId, appId, w1, w2, w3, t1 = row
        print(appId, w1, w2, w3, t1, last_accesses.get(itemId, None))
        access_it = input('Access it? ')

        if access_it == 'y':
            timestamp = int(time.time())
            last_accesses[itemId] = timestamp
            print('Accessed at {}'.format(timestamp))

    with open(result.access, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['itemId', 'timestamp'])
        for itemId, timestamp in last_accesses.items():
            writer.writerow([itemId, timestamp])

if __name__ == "__main__":
    main()

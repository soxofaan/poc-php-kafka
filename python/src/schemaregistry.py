from pprint import pprint

import itertools
import requests

REGISTRY_URL = 'http://schemaregistry:8081/'


def query_registry(query):
    url = REGISTRY_URL + query
    response = requests.get(url)
    print('=== {c} GET {u}'.format(u=url, c=response.status_code))
    if response.status_code == 200:
        data = response.json()
        pprint(data)
        return data


def main():
    query_registry('config')

    subjects = query_registry('subjects')

    for subject in subjects:
        versions = query_registry('subjects/{s}/versions'.format(s=subject))

        for version in versions:
            query_registry('subjects/{s}/versions/{v}'.format(s=subject, v=version))

    for i in itertools.count(start=1):
        data = query_registry('schemas/ids/{i}'.format(i=i))
        if not data:
            break


if __name__ == '__main__':
    main()

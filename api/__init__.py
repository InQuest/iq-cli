from lib import client


def single(entity, entity_id):
    with client.get(f'/{entity}/single', params={'id': entity_id}) as r:
        r.raise_for_status()
        parsed_data = r.json()
        if 'data' not in parsed_data or not len(parsed_data['data']):
            return
        return parsed_data['data'][0]


def generate_search_criterion(column, value, logic='OR', operator='='):
    return {
        'column': column,
        'logic': logic,
        'options': [
            {
                'operator': operator,
                'value': value
            },
        ],
    }


def loop_search_requests(path, limit, aq=None, min_timestamp=None):
    batch = min(limit, 25)
    offset = 0
    total = 0
    while True:
        r = client.post(
            path,
            json={
                'minTimestamp': min_timestamp or 0,
                'skip': offset,
                'limit': batch,
                'aq': aq,
            },
        )
        r.raise_for_status()

        entries = r.json()['data']
        for entry in entries:
            if limit is not None and total >= limit:
                return

            total += 1
            yield entry

        # len(entries) < batch
        # means that there are no more search results on the server
        if len(entries) < batch or (limit is not None and total >= limit):
            return
        offset += batch


import api.file
import api.search
import api.session

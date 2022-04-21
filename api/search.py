import datetime
import time

from api import default_limit, generate_search_criterion, loop_search_requests, single
import simplejson as json


files_columns = {
    'hash': 'hash',
    'eventid': 'yara_details->signature_event_id',
    'signature_name': 'yara_details->signature_title',
    'signature_category': 'yara_details->signature_category',
}


def saved(id, limit=None):
    configuration_api_entity = single('user-data', id)
    if not configuration_api_entity or not configuration_api_entity['type'].startswith('SEARCH_'):
        raise Exception(f'Saved configuration [id:{id}] is not a valid search configuration.')

    configuration = json.loads(configuration_api_entity['value'])

    if 'static' == configuration['api']['parameters']['type']:
        min_datetime = configuration['api']['parameters']['min']
        max_datetime = configuration['api']['parameters']['max']
    elif 'dynamic' == configuration['api']['parameters']['type']:
        min_datetime = datetime.datetime.utcfromtimestamp(
            time.time() - configuration['api']['parameters']['interval']
        ).strftime('%Y-%m-%d %H:%M:%S')
        max_datetime = None
    else:
        raise Exception(
            f'Unexpected time interval type in saved search [id:{id}]: {configuration["api"]["parameters"]["type"]}'
        )

    if limit is None:
        if 'limit' in configuration['api']:
            limit = configuration['api']['limit']
        else:
            limit = default_limit

    yield from loop_search_requests(
        path='/' + configuration['api']['path'],
        limit=limit,
        aq=configuration['api']['aq'],
        min_timestamp=min_datetime,
        max_timestamp=max_datetime,
    )


def files(
        limit=default_limit,
        file_hash=None,
        eventid=None,
        signature_name=None,
        signature_category=None
):
    aq = {
        'logic': 'AND',
        'criterions': [],
    }

    if file_hash is not None:
        aq['criterions'].append(generate_search_criterion(
            files_columns['hash'],
            file_hash,
        ))

    if eventid is not None:
        aq['criterions'].append(generate_search_criterion(
            files_columns['eventid'],
            eventid,
        ))

    if signature_name is not None:
        aq['criterions'].append(generate_search_criterion(
            files_columns['signature_name'],
            signature_name,
        ))

    if signature_category is not None:
        aq['criterions'].append(generate_search_criterion(
            files_columns['signature_category'],
            signature_category,
        ))

    yield from loop_search_requests(path='/files', limit=limit, aq=aq)

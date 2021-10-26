from api import generate_search_criterion, loop_search_requests

columns = {
    'hash': 'hash',
    'eventid': 'yara_details->signature_event_id',
    'signature_name': 'yara_details->signature_title',
    'signature_category': 'yara_details->signature_category',
}


def files(
        file_hash=None,
        limit=None,
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
            columns['hash'],
            file_hash,
        ))

    if eventid is not None:
        aq['criterions'].append(generate_search_criterion(
            columns['eventid'],
            eventid,
        ))

    if signature_name is not None:
        aq['criterions'].append(generate_search_criterion(
            columns['signature_name'],
            signature_name,
        ))

    if signature_category is not None:
        aq['criterions'].append(generate_search_criterion(
            columns['signature_category'],
            signature_category,
        ))

    yield from loop_search_requests('/files', aq, limit=limit)

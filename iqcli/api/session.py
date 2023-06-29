import iqcli.api

def export(session_id):
    return iqcli.api.single(entity='session', entity_id=session_id)

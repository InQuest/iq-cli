import api


def export(session_id):
    return api.single(entity='session', entity_id=session_id)

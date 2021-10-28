import api


def one(session_id):
    return api.one(entity='session', entity_id=session_id)

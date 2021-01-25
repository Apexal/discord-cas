import json


def hget_json(db, hash, key):
    raw = db.hget(hash, key)
    return json.loads(raw) if raw else None
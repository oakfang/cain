__author__ = 'oakfang'

from bson.objectid import ObjectId
import re

NOT_HEX = '[^a-f0-9]'


def is_hex_encoded(string):
    return not re.search(NOT_HEX, string.lower())


def to_object_id(oid):
    if isinstance(oid, (int, long)):
        oid = hex(oid)[2:]
    if isinstance(oid, (str, unicode)):
        oid = oid.lower()
        if is_hex_encoded(oid):
            oid = ObjectId(oid)
        else:
            oid = ObjectId(oid.encode('hex'))
    if isinstance(oid, ObjectId):
        return oid
    raise TypeError("object id is either a number, a string or an ObjectId")
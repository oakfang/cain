__author__ = 'oakfang'


class Exported(object):
    def __init__(self, object_type, required=False, default=None):
        self._type = object_type
        self._default = default
        self._required = required
        self._name = None

    def set_name(self, name):
        self._name = name

    def __get__(self, instance, owner=None):
        return getattr(instance, "__"+self._name)

    def __set__(self, instance, value):
        collection = instance.collection
        _id = instance._id
        collection.update({"_id": _id}, {"$set": {self._name: value}})
        setattr(instance, "__"+self._name, value)
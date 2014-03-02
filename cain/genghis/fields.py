__author__ = 'oakfang'


class Exported(object):
    def __init__(self, object_type, required=False, default=None):
        self._type = object_type
        self._default = default
        self._required = required
        self._name = None

    def set_name(self, name):
        self._name = name

    def __le__(self, other):
        return {self._name: {"$lte": other}}

    def __lt__(self, other):
        return {self._name: {"$lt": other}}

    def __gt__(self, other):
        return {self._name: {"$gt": other}}

    def __ge__(self, other):
        return {self._name: {"$gte": other}}

    def __eq__(self, other):
        return {self._name: other}

    def __ne__(self, other):
        return {self._name: {"$ne": other}}

    def in_(self, array):
        return {self._name: {"$in": array}}

    def nin_(self, array):
        return {self._name: {"$nin": array}}

    def like(self, regex):
        return {self._name: {"$regex": regex}}

    def exists(self, does_exist=True):
        return {self._name: {"$exists": does_exist}}

    def has(self, *items):
        return {self._name: {"$all": items}}

    def count(self, cnt):
        return {self._name: {"$size": cnt}}

    def __get__(self, instance, owner=None):
        if owner:
            return self
        return getattr(instance, "__"+self._name)

    def __set__(self, instance, value):
        collection = instance.collection
        _id = instance._id
        collection.update({"_id": _id}, {"$set": {self._name: value}})
        setattr(instance, "__"+self._name, value)


def or_(*clauses):
    return {"$or": clauses}


def and_(*clauses):
    return {"$or": clauses}


def nor_(*clauses):
    return {"$nor": clauses}


def not_(clause):
    return {"$not": clause}
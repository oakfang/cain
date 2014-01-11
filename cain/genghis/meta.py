__author__ = 'oakfang'

from fields import Exported
from utils import to_object_id


class GenghisMeta(type):
    def __new__(cls, name, bases, attributes_dict):
        if "__collection__" not in attributes_dict:
            cls.__collection__ = name.lower()
        else:
            attributes_dict["__collection__"] = attributes_dict["__collection__"].lower()
        cls._fields = dict(filter(lambda tpl: isinstance(tpl[1], Exported), attributes_dict.iteritems()))
        for key, exported in cls._fields.iteritems():
            exported.set_name(key)
        cls._genghis_app = None
        return super(GenghisMeta, cls).__new__(cls, name, bases, attributes_dict)

    def register(cls, genghis_app):
        cls._genghis_app = genghis_app

    def delete(cls, *instances):
        for instance in instances:
            cls._genghis_app[cls.__collection__].remove(instance._id)

    @property
    def collection(self):
        return self._genghis_app[self.__collection__]

    def init(cls, _id, **kwargs):
        _id = to_object_id(_id)
        kwargs['_id'] = _id
        return super(GenghisMeta, cls).__call__(**kwargs)

    def __call__(self, **kwargs):
        if "_id" in kwargs:
            del kwargs["_id"]
        for key, value in kwargs.iteritems():
            if key not in self._fields:
                raise KeyError("Property not defined")
            if not isinstance(value, self._fields[key]._type):
                raise TypeError("Expected {}, got {}", self._fields[key]._type, type(value))
        for key in [f for f in self._fields if self._fields[f]._default is not None]:
            if key not in kwargs:
                kwargs[key] = self._fields[key]._default
        for key in [key for key in self._fields if self._fields[key]._required and key not in kwargs]:
            raise KeyError("Property {} is required", key)

        oid = self._genghis_app[self.__collection__].insert(kwargs)
        kwargs["_id"] = oid
        return super(GenghisMeta, self).__call__(**kwargs)
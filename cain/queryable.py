__author__ = 'oakfang'


class Queryable(object):
    """
    Base Queryable object
    """
    @classmethod
    def __validate__(cls):
        """
        Override to determine if code can query.
        """
        return True

    @classmethod
    def __query__(cls, *args, **kwargs):
        """
        Override to return the filtered object.
        """
        return None

    @classmethod
    def get(cls, *args, **kwargs):
        assert cls.__validate__(), "Connection can't be validated."
        return cls.__query__(*args, **kwargs)


class ElixirQueryable(Queryable):
    """
    Queryable for the elixir framework.
    """
    @classmethod
    def __validate__(cls):
        return hasattr(cls, "query")

    @classmethod
    def __query__(cls, *args, **kwargs):
        q = getattr(cls, "query")
        for arg in args:
            q = q.filter(arg)
        for key, value in kwargs.iteritems():
            q = q.filter_by(**{key: value})
        return q


class SelfContained(type):
    """
    Iterable metaclass for iterable classes.
    """
    def __init__(cls, *args, **kwargs):
        super(SelfContained, cls).__init__(*args, **kwargs)
        cls.__backend = []
        
    def __iter__(self):
        return iter(self.__backend)
        
    def __call__(self,*args, **kwargs):
        i = super(SelfContained, self).__call__(*args, **kwargs)
        self.__backend.append(i)
        return i
        
    def delete(cls, instance):
        if not isinstance(instance, cls):
            raise TypeError("Can't delete what doesn't belong")
        cls.__backend.remove(instance)


class BaseQueryable(Queryable):
    """
    Queryable iterable-s
    """
    __metaclass__ = SelfContained

    @classmethod
    def __query__(cls, *args, **kwargs):
        return filter(lambda x: all(hasattr(x, key) and getattr(x, key) == value for key, value in kwargs.iteritems()),
                      cls)


class MongolQueryable(Queryable):
    @classmethod
    def __query__(cls, *args, **kwargs):
        from genghis.utils import to_object_id
        if '_id' in kwargs:
            kwargs['_id'] = to_object_id(kwargs['_id'])
        return MongolQuery(cls, cls.collection.find(kwargs))


class MongolQuery(object):
    def __init__(self, cls, query):
        self._cls = cls
        self._query = query

    def __getitem__(self, item):
        json = self._query[item]
        _id = json['_id']
        del json['_id']
        return self._cls.init(_id, **json)

    def __iter__(self):
        return self

    def next(self):
        json = self._query.next()
        _id = json['_id']
        del json['_id']
        return self._cls.init(_id, **json)

    def __proxy(self, attribute):
        from pymongo.cursor import Cursor

        def _wrapper(*args, **kwargs):
            r = attribute(*args, **kwargs)
            if isinstance(r, Cursor):
                return self.__class__(self._cls, r)
            return r
        return _wrapper

    def __getattr__(self, item):
        attribute = getattr(self._query, item)
        if not callable(attribute):
            return attribute
        return self.__proxy(attribute)
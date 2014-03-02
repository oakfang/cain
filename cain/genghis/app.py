__author__ = 'oakfang'

import pymongo
import flask
from meta import GenghisMeta, to_object_id
from cain.jsonable import Jsonable, jsonify
from cain.queryable import Queryable


def basic_restful_api(request, mongol, oid=None):
    method = request.method
    if method == 'GET':
        if oid is None:
            form = {}
            for arg in request.args:
                form[arg] = request.args[arg]
            return jsonify(list(mongol.get(**form)))
        return jsonify(mongol.get(_id=oid)[0] if mongol.get(_id=oid) else None)
    if method == 'PUT':
        m = mongol.get(id=oid)[0]
        for arg in request.form:
            setattr(m, arg, request.form[arg])
        return jsonify(m)
    if method == 'POST':
        form = {}
        for arg in request.form:
            form[arg] = request.form[arg]
        return jsonify(mongol(**form))
    if method == 'DELETE':
        d = mongol.get(id=oid)
        mongol.delete(d)
        return ''
    raise ValueError('Method {} Unsupported'.format(method))


class GenghisApplication(object):
    def __init__(self, name, host, port=27017):
        self._client = pymongo.MongoClient(host, port)
        self._db = self._client[name]
        self._flask = flask.Flask(name)

    def __getitem__(self, collection):
        return self._db[collection]

    def __enter__(self):
        return self

    def close(self):
        self._client.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def route(self, *args, **kwargs):
        return self._flask.route(*args, **kwargs)

    def run(self, *args, **kwargs):
        self._flask.run(*args, **kwargs)

    def register(self, mongol):
        mongol.register(self)
        self.route('/{mongol}'.format(mongol=mongol.__collection__), methods=['POST', 'GET'])(
            self.route('/{mongol}/<oid>'.format(mongol=mongol.__collection__), methods=['GET', 'PUT', 'DELETE'])(
                lambda oid=None: basic_restful_api(flask.request, mongol, oid)
            ))
        return mongol


class Mongol(Jsonable, Queryable):
    __metaclass__ = GenghisMeta

    def __init__(self, **kwargs):
        self.__mongo_id = kwargs['_id']
        del kwargs['_id']
        for attribute, value in kwargs.iteritems():
            setattr(self, "__"+attribute, value)

    @property
    def _id(self):
        return to_object_id(self.__mongo_id)

    @property
    def id(self):
        return self._id.binary.encode('hex')

    @classmethod
    def __query__(cls, *args, **kwargs):
        for arg in args:
            kwargs.update(arg)
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
        def _wrapper(*args, **kwargs):
            r = attribute(*args, **kwargs)
            if isinstance(r, pymongo.cursor.Cursor):
                return self.__class__(self._cls, r)
            return r
        return _wrapper

    def __getattr__(self, item):
        attribute = getattr(self._query, item)
        if not callable(attribute):
            return attribute
        return self.__proxy(attribute)
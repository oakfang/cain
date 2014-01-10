__author__ = 'oakfang'

from cain.restable import RestfulApplication
from cain.restable import DELETERestfulMethod, GETRestfulProperty, PUTRestfulMethod, POSTRestfulFunction, flushersetter
import pytest


app = RestfulApplication("http://localhost:5000")


class Dummy(object):
    def __init__(self, dummy_id):
        self.dummy_id = dummy_id
        self._backend = app.flusher(self, '/dummy/<dummy_id>')

    def commit(self):
        self._backend.flush()

    @app.query('/dummy')
    def query(**kwargs):
        return kwargs

    @staticmethod
    def __rest__(jsn):
        return Dummy(jsn["id"])

    @app.get('/dummy/<dummy_id>', cache=False)
    def name(self, jsn):
        return jsn["name"]

    @name.putter
    @flushersetter('_backend', 'name')
    def set_name(self, name):
        return name

    @app.post('/dummy')
    def new(name):
        return {'name': name}

    @app.delete('/dummy/<dummy_id>')
    def delete(self):
        return True


class RestfulDummy(object):
    def __init__(self, dummy_id):
        self.dummy_id = dummy_id

    @staticmethod
    def __rest__(jsn):
        return Dummy(jsn["id"])
    
    def _name(self, jsn):
        return jsn["name"]

    def _set_name(self, name):
        return {'name': name}

    def _new(name):
        return {'name': name}

    def _delete(self):
        return True

    name = GETRestfulProperty(_name, '/dummy/<dummy_id>', 'http://localhost:5000')

    set_name = PUTRestfulMethod(_set_name, '/dummy/<dummy_id>', 'http://localhost:5000')

    new = POSTRestfulFunction(_new, '/dummy', 'http://localhost:5000')

    delete = DELETERestfulMethod(_delete, '/dummy/<dummy_id>', 'http://localhost:5000')


def test_dummy_get():
    d = Dummy(0)
    assert d.name == "Test1"


def test_dummy_put():
    d = Dummy(1)
    d.name = 'poof'
    d.commit()
    assert d.name == "poof"


def test_dummy_post():
    d = Dummy.new("lolz")
    n = Dummy(d.dummy_id)
    assert d.name == n.name == "lolz"


def test_dummy_delete():
    d = Dummy.new("moomoo")
    d.delete()
    with pytest.raises(TypeError):
        assert d.name


def test_dummy_query():
    ds = Dummy.query(name="Test1")
    assert len(list(ds)) == 1


def test_rdummy_get():
    d = RestfulDummy(0)
    assert d.name == "Test1"


def test_rdummy_put():
    d = RestfulDummy(2)
    changes = d.set_name("poof")
    assert changes['name'] == "poof"


def test_rdummy_post():
    d = RestfulDummy.new("lolz")
    n = RestfulDummy(d.dummy_id)
    assert d.name == n.name == "lolz"


def test_rdummy_delete():
    d = RestfulDummy.new("moomoo")
    d.delete()
    with pytest.raises(TypeError):
        assert d.name
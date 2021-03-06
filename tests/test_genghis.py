__author__ = 'oakfang'

from cain.genghis.app import GenghisApplication, Mongol
from cain.genghis.fields import Exported
import pytest


app = GenghisApplication("GenghisTest", "localhost")


@app.register
class TestMongol(Mongol):
    __collection__ = 'mongols'
    mood = Exported(str)
    name = Exported(str, required=True)
    age = Exported(int, default=0)
    nicknames = Exported(list)


def test_required():
    with pytest.raises(KeyError):
        TestMongol()


def test_unexpected():
    with pytest.raises(KeyError):
        TestMongol(roar=6)


def test_wrong_type():
    with pytest.raises(TypeError):
        TestMongol(name=7)


def test_normal_creation_and_deletion():
    m = TestMongol(name="oakfang", age=20, mood="crazy!")
    assert m.name == "oakfang"
    assert m.age == 20
    assert m.mood == "crazy!"


def test_finding():
    TestMongol.collection.remove({})
    TestMongol(name="poof", age=20, mood="lazy!")
    TestMongol(name="foo", age=50, mood="lazy!")
    TestMongol(name="bar")
    assert TestMongol.get(age=50).count() == 1
    assert TestMongol.get(mood="lazy!").count() == 2
    assert TestMongol.get().count() == 3


def test_advanced_finding():
    TestMongol.collection.remove({})
    TestMongol(name="poof", age=20, mood="lazy!")
    TestMongol(name="foo", age=50, mood="lazy!")
    TestMongol(name="bar")
    TestMongol(name="rook", age=14, mood="lazy ass")
    TestMongol(name="mike", age=10, nicknames=["mikmik", "foobar"])
    assert TestMongol.get(TestMongol.age > 15).count() == 2
    assert TestMongol.get(TestMongol.name.like(".*oo.*")).count() == 3
    assert TestMongol.get(TestMongol.mood.exists(False)).count() == 2
    assert TestMongol.get(TestMongol.nicknames.has("foobar")).count() == 1
    assert TestMongol.get(TestMongol.nicknames.count(1)).count() == 0


def teardown_module(module):
    TestMongol.collection.remove({})


def setup_module(module):
    TestMongol.collection.remove({})


if __name__ == "__main__":
    TestMongol.collection.remove({})
    TestMongol(name="poof", age=20, mood="lazy!")
    TestMongol(name="foo", age=50, mood="lazy!")
    TestMongol(name="bar")
    app.run(port=5001, debug=True)
__author__ = 'oakfang'

import flask
from cain.jsonable import Jsonable, jsonify
from cain.queryable import BaseQueryable


class Dummy(Jsonable, BaseQueryable):
    __jattrs__ = ['id', 'name']

    def __init__(self, did, name):
        self.id = did
        self.name = name

    def update(self, attrs_dict):
        for attr, val in attrs_dict.iteritems():
            setattr(self, attr, val)

    def __repr__(self):
        return "<Dummy {name} [{id}]>".format(name=self.name, id=self.id)


app = flask.Flask(__name__)


def clean_form(form, **fixes):
    dict_form = dict(form)
    for key, func in fixes.iteritems():
        dict_form[key] = func(dict_form[key])
    return dict_form


@app.route('/dummy', methods=['POST', 'GET'])
@app.route('/dummy/<int:dummy_id>', methods=['GET', 'PUT', 'DELETE'])
def get_dummy(dummy_id=None):
    method = flask.request.method
    if method == 'GET':
        if dummy_id is None:
            form = clean_form(flask.request.args, name=lambda lst: lst[0])
            print Dummy._backend
            return jsonify(Dummy.get(**form))
        return jsonify(Dummy.get(id=dummy_id)[0] if Dummy.get(id=dummy_id) else None)
    if method == 'PUT':
        form = clean_form(flask.request.form, name=lambda lst: lst[0])
        Dummy.get(id=dummy_id)[0].update(form)
        return jsonify(Dummy.get(id=dummy_id)[0])
    if method == 'POST':
        dummy_name = clean_form(flask.request.form, name=lambda lst: lst[0])['name']
        dummy_id = max(Dummy.get(), key=lambda d: d.id).id + 1
        return jsonify(Dummy(dummy_id, dummy_name))
    if method == 'DELETE':
        Dummy.get(id=dummy_id)[0].delete()
        return ''
    raise ValueError('Method {} Unsupported'.format(method))


if __name__ == "__main__":
    Dummy(0, "Test1")
    Dummy(1, "Test2")
    Dummy(2, "Test3")
    app.run(debug=True)

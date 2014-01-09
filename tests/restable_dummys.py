__author__ = 'oakfang'

import flask
from cain.jsonable import Jsonable, jsonify


class Dummy(Jsonable):
    __jattrs__ = ['id', 'name']

    def __init__(self, did, name):
        self.id = did
        self.name = name

    def update(self, attrs_dict):
        for attr, val in attrs_dict.iteritems():
            setattr(self, attr, val)


app = flask.Flask(__name__)

DUMMYS = [Dummy(0, "Test1"),
          Dummy(1, "Test2"),
          Dummy(2, "Test3")]

def get_from_dummys(id):
    filtered = filter(lambda x: x.id == id, DUMMYS)
    return None if not filtered else filtered[0]


def clean_form(form, **fixes):
    dict_form = dict(form)
    for key, func in fixes.iteritems():
        dict_form[key] = func(dict_form[key])
    return dict_form


@app.route('/dummy', methods=['POST'])
@app.route('/dummy/<int:dummy_id>', methods=['GET', 'PUT', 'DELETE'])
def get_dummy(dummy_id=None):
    method = flask.request.method
    if method == 'GET':
        return jsonify(get_from_dummys(dummy_id))
    if method == 'PUT':
        form = clean_form(flask.request.form, name=lambda lst: lst[0])
        get_from_dummys(dummy_id).update(form)
        return jsonify(get_from_dummys(dummy_id))
    if method == 'POST':
        dummy_name = clean_form(flask.request.form, name=lambda lst: lst[0])['name']
        dummy_id = max(DUMMYS, key=lambda d: d.id).id + 1
        DUMMYS.append(Dummy(dummy_id, dummy_name))
        return jsonify(get_from_dummys(dummy_id))
    if method == 'DELETE':
        DUMMYS.remove(get_from_dummys(dummy_id))
        return ''
    raise ValueError('Method {} Unsupported'.format(method))


if __name__ == "__main__":
    app.run(debug=True)
__author__ = 'oakfang'

import json
import flask

app = flask.Flask(__name__)

DUMMYS = [{u"name": u"Test1", u"id": 0},
          {u"name": u"Test2", u"id": 1},
          {u"name": u"Test3", u"id": 2}]

def get_from_dummys(id):
    filtered = filter(lambda x: x['id'] == id, DUMMYS)
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
        return json.dumps(get_from_dummys(dummy_id))
    if method == 'PUT':
        form = clean_form(flask.request.form, name=lambda lst: lst[0])
        get_from_dummys(dummy_id).update(form)
        return json.dumps(get_from_dummys(dummy_id))
    if method == 'POST':
        dummy = clean_form(flask.request.form, name=lambda lst: lst[0])
        dummy[u"id"] = max(DUMMYS, key=lambda d: d[u"id"])[u"id"] + 1
        DUMMYS.append(dummy)
        return json.dumps(get_from_dummys(dummy[u"id"]))
    if method == 'DELETE':
        DUMMYS.remove(get_from_dummys(dummy_id))
        return ''
    raise ValueError('Method {} Unsupported'.format(method))


if __name__ == "__main__":
    app.run(debug=True)